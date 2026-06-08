package processor

import (
	"context"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Generator struct {
	channels Channels
}

func NewGenerator(channels Channels) *Generator {
	return &Generator{
		channels: channels,
	}
}

func (h *Generator) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	ans := `Введите количество битов для модуля`

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		NextState:        genBits,
		Result:           state,
	}
}
