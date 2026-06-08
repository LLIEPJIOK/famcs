package app

import (
	"context"
	"fmt"

	repo "github.com/LLIEPJIOK/lab1/internal/infrastructure/repository/roster"
	"github.com/jackc/pgx/v5/pgxpool"
)

type InitFunc func(ctx context.Context) error

func (a *App) inits() []InitFunc {
	return []InitFunc{
		a.initDB,
		a.initRepo,
	}
}

func (a *App) initDB(ctx context.Context) error {
	db, err := pgxpool.New(ctx, a.cfg.Database.DSN)
	if err != nil {
		return fmt.Errorf("failed to create db: %w", err)
	}

	if err := db.Ping(ctx); err != nil {
		return fmt.Errorf("failed to ping db: %w", err)
	}

	a.db = db

	return nil
}

func (a *App) initRepo(_ context.Context) error {
	a.repo = repo.New(a.db)

	return nil
}
