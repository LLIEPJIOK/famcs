package app

import (
	"context"
	"log/slog"
	"os/signal"
	"sync"
	"syscall"

	"cm_lab4_tg/internal/config"
	"cm_lab4_tg/internal/domain"
)

type App struct {
	cfg      *config.Config
	channels *domain.Channels
}

func New(cfg *config.Config) *App {
	return &App{
		cfg:      cfg,
		channels: domain.NewChannels(),
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
