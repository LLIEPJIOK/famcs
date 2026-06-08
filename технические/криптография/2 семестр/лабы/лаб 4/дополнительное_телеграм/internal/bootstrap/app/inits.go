package app

import (
	"context"
)

type InitFunc func(ctx context.Context) error

func (a *App) inits() []InitFunc {
	return []InitFunc{}
}
