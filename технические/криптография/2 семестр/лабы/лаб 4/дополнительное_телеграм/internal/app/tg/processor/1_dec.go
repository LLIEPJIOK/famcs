package processor

import (
	"context"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Decrypt struct {
	channels Channels
}

func NewDecrypt(channels Channels) *Decrypt {
	return &Decrypt{
		channels: channels,
	}
}

func (h *Decrypt) Handle(ctx context.Context, state *State) *fsm.Result[*State] {
	ans := `Введите текст для расшифровки`

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		NextState:        decMsg,
		Result:           state,
	}
}
