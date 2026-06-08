package repo

import (
	"cm_lab4_tg/internal/domain"
	"context"
	"sync"
)

type Repo struct {
	mu   *sync.RWMutex
	keys map[int64]*domain.Keys
}

func New() *Repo {
	return &Repo{
		mu:   &sync.RWMutex{},
		keys: make(map[int64]*domain.Keys),
	}
}

func (r *Repo) SetKeys(_ context.Context, chatID int64, keys *domain.Keys) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.keys[chatID] = keys

	return nil
}

func (r *Repo) GetKeys(_ context.Context, chatID int64) (*domain.Keys, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	keys, ok := r.keys[chatID]
	if !ok {
		return nil, NewErrNotFound()
	}

	return keys, nil
}
