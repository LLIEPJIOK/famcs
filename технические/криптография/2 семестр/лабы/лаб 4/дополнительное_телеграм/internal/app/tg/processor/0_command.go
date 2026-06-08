package processor

import (
	"context"

	"github.com/LLIEPJIOK/go-common/fsm"
)

type Commander struct {
}

func NewCommander() *Commander {
	return &Commander{}
}

func (h *Commander) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	switch state.Message {
	case "/start":
		return &fsm.Result[*State]{
			NextState:        start,
			IsAutoTransition: true,
			Result:           state,
		}

	case "/help":
		return &fsm.Result[*State]{
			NextState:        help,
			IsAutoTransition: true,
			Result:           state,
		}

	case "/gen":
		return &fsm.Result[*State]{
			NextState:        gen,
			IsAutoTransition: true,
			Result:           state,
		}

	case "/enc":
		return &fsm.Result[*State]{
			NextState:        enc,
			IsAutoTransition: true,
			Result:           state,
		}

	case "/dec":
		return &fsm.Result[*State]{
			NextState:        dec,
			IsAutoTransition: true,
			Result:           state,
		}

	default:
		state.ShowError = "неопознанная команда"

		return &fsm.Result[*State]{
			NextState:        fail,
			IsAutoTransition: true,
			Result:           state,
		}
	}
}
