package processor

import (
	"cm_lab4_tg/internal/domain"
	"context"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type Encryptor struct {
	channels Channels
}

func NewEncryptor(channels Channels) *Encryptor {
	return &Encryptor{
		channels: channels,
	}
}

func (h *Encryptor) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	ans := `Введите открытый ключ`

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	state.Object = &domain.Encryption{}

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		NextState:        encKey,
		Result:           state,
	}
}
