package registry

import (
	"context"
	"fmt"
	"log"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/LLIEPJIOK/lab1/internal/app/grpc/roster"
	"github.com/LLIEPJIOK/lab1/internal/config"
	"github.com/LLIEPJIOK/lab1/internal/domain"
	"github.com/gorilla/mux"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const (
	MB      = 1 << 20
	fixsize = 10

	connectionTimeout    = 60 * time.Second
	maxConcurrentStreams = 1000
)

type Repository interface {
	AddPlayer(ctx context.Context, player *domain.Player) error
	GetPlayer(ctx context.Context, id string) (*domain.Player, error)
	GetPlayers(ctx context.Context) ([]*domain.Player, error)
	UpdatePlayer(ctx context.Context, player *domain.Player) error
	DeletePlayer(ctx context.Context, id string) error
}

// RunHTTPServer sets up and starts the HTTP roster service with graceful shutdown.
func RunHTTPServer(ctx context.Context, cfg *config.Config, repo Repository) error {
	srv := roster.NewServer(repo)
	router := mux.NewRouter()
	srv.RegisterRoutes(router)

	httpServer := &http.Server{
		Addr:    fmt.Sprintf(":%d", cfg.App.Port),
		Handler: router,
	}

	// Start server
	go func() {
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("HTTP server ListenAndServe: %v", err)
		}
	}()

	// Listen for interrupt or terminate signals
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)

	select {
	case <-ctx.Done():
	case <-stop:
	}

	// Shutdown with timeout
	ctxShut, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	return httpServer.Shutdown(ctxShut)
}

func closer(ctx context.Context, server *grpc.Server) error {
	<-ctx.Done()

	server.GracefulStop()

	return nil
}

func Panic(
	ctx context.Context,
	req any,
	_ *grpc.UnaryServerInfo,
	handler grpc.UnaryHandler,
) (resp any, err error) {
	defer func() {
		if rec := recover(); rec != nil {
			slog.Error("Panic", slog.Any("error", rec))

			err = status.Errorf(codes.Internal, "panic: %v", rec)
		}
	}()

	resp, err = handler(ctx, req)

	return resp, err
}
