package processor

import (
	"cm_lab4_tg/internal/domain"
	"context"
	"fmt"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"log/slog"
	"strings"
)

type EncryptorMessage struct {
	channels Channels
	client   Client
}

func NewEncryptorMessage(channels Channels, client Client) *EncryptorMessage {
	return &EncryptorMessage{
		channels: channels,
		client:   client,
	}
}

func (h *EncryptorMessage) Handle(ctx context.Context, state *State) *fsm.Result[*State] {
	data, ok := state.Object.(*domain.Encryption)
	if !ok {
		slog.Error(
			"invalid object type",
			slog.Any("type", fmt.Sprintf("%T", state.Object)),
			slog.Any("handler", "EncryptorExponent"),
		)

		return &fsm.Result[*State]{
			NextState:        fail,
			IsAutoTransition: true,
			Result:           state,
		}
	}

	data.Message = strings.TrimSpace(state.Message)
	state.Object = data

	cipher, err := h.client.Encrypt(ctx, data)
	if err != nil {
		state.ShowError = "не удалось зашифровать"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to encrypt: %w", err),
		}
	}

	ans := "Зашифрованное сообщение: " + cipher

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		Result:           state,
	}
}
