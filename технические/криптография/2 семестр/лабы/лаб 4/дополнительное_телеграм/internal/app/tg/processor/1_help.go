package processor

import (
	"context"

	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

const helperAnswer = `📌 Доступные команды:  
- /gen – сгенерировать ключи
- /enc – зашифровать сообщение
- /dec – расшифровать сообщение
`

type Helper struct {
	channels Channels
}

func NewHelper(channels Channels) *Helper {
	return &Helper{
		channels: channels,
	}
}

func (h *Helper) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	msg := tgbotapi.NewMessage(state.ChatID, helperAnswer)
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		Result:           state,
	}
}
