package app

import (
	"context"
	"log/slog"
	"sync"

	"github.com/LLIEPJIOK/lab1/internal/bootstrap/registry"
)

type runService = func(ctx context.Context, stop context.CancelFunc, wg *sync.WaitGroup)

func (a *App) services() []runService {
	return []runService{
		a.runGRPCService,
	}
}

func (a *App) runGRPCService(ctx context.Context, stop context.CancelFunc, wg *sync.WaitGroup) {
	defer wg.Done()
	defer stop()
	defer slog.Info("GRPC service stopped")

	if err := registry.RunHTTPServer(ctx, a.cfg, a.repo); err != nil {
		slog.Error("Failed to run GRPC server")
	}
}
