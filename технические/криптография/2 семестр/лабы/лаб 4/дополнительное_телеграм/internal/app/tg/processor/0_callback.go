package processor

import (
	"context"

	"github.com/LLIEPJIOK/go-common/fsm"
)

type Callbacker struct {
	channels Channels
}

func NewCallbacker(channels Channels) *Callbacker {
	return &Callbacker{
		channels: channels,
	}
}

func (h *Callbacker) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	switch {
	default:
		state.ShowError = "неопознанная команда"

		return &fsm.Result[*State]{
			NextState:        fail,
			IsAutoTransition: true,
			Result:           state,
		}
	}
}
