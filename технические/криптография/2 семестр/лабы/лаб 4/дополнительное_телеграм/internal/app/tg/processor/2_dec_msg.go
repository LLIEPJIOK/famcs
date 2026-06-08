package processor

import (
	"cm_lab4_tg/internal/infra/repo"
	"context"
	"errors"
	"fmt"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type DecryptMessage struct {
	channels Channels
	client   Client
	repo     Repo
}

func NewDecryptMessage(channels Channels, client Client, repo Repo) *DecryptMessage {
	return &DecryptMessage{
		channels: channels,
		client:   client,
		repo:     repo,
	}
}

func (h *DecryptMessage) Handle(ctx context.Context, state *State) *fsm.Result[*State] {
	keys, err := h.repo.GetKeys(ctx, state.ChatID)
	if err != nil {
		if errors.As(err, &repo.ErrNotFound{}) {
			ans := "Нет секретного ключа. Для генерации используйте команду /gen"

			msg := tgbotapi.NewMessage(state.ChatID, ans)
			msg.ParseMode = tgbotapi.ModeMarkdown
			h.channels.TelegramResp() <- msg

			return &fsm.Result[*State]{
				IsAutoTransition: false,
				Result:           state,
			}
		}
	}

	initial, err := h.client.Decrypt(ctx, keys.PrivateKey, state.Message)
	if err != nil {
		state.ShowError = "не удалось расшифровать"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to decrypt: %w", err),
		}
	}

	ans := "Расшифрованное сообщение: " + initial

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		Result:           state,
	}
}
