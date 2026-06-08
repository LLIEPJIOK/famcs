package processor

import (
	"context"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

const staterAnswer = `*Привет! Я бот, реализующий алгоритм RSA*

📌 Доступные команды:  
- /gen – сгенерировать ключи
- /enc – зашифровать сообщение
- /dec – расшифровать сообщение
`

type Starter struct {
	channels Channels
}

func NewStater(channels Channels) *Starter {
	return &Starter{
		channels: channels,
	}
}

func (h *Starter) Handle(ctx context.Context, state *State) *fsm.Result[*State] {
	msg := tgbotapi.NewMessage(state.ChatID, staterAnswer)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		Result:           state,
	}
}
