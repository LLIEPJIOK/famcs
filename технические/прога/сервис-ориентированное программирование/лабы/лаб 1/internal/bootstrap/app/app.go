package app

import (
	"context"
	"log/slog"
	"os/signal"
	"sync"
	"syscall"

	"github.com/LLIEPJIOK/lab1/internal/config"
	"github.com/LLIEPJIOK/lab1/internal/domain"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Repository interface {
	AddPlayer(ctx context.Context, player *domain.Player) error
	GetPlayer(ctx context.Context, id string) (*domain.Player, error)
	GetPlayers(ctx context.Context) ([]*domain.Player, error)
	UpdatePlayer(ctx context.Context, player *domain.Player) error
	DeletePlayer(ctx context.Context, id string) error
}

type App struct {
	cfg  *config.Config
	db   *pgxpool.Pool
	repo Repository
}

func New(cfg *config.Config) *App {
	return &App{
		cfg: cfg,
	}
}

func (a *App) Run(ctx context.Context) error {
	ctx, stop := signal.NotifyContext(ctx, syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	for _, init := range a.inits() {
		if err := init(ctx); err != nil {
			return err
		}
	}

	var wg sync.WaitGroup

	slog.Info("Starting application")
	slog.Debug("Debug level enabled")

	for _, service := range a.services() {
		wg.Add(1)

		go service(ctx, stop, &wg)
	}

	stoppedChan := make(chan struct{})

	go func() {
		wg.Wait()

		stoppedChan <- struct{}{}
	}()

	return a.closer(ctx, a.cfg, stoppedChan)
}
