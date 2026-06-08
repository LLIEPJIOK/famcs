package processor

import (
	"cm_lab4_tg/internal/domain"
	"context"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"log/slog"
)

type EncryptorKey struct {
	channels Channels
}

func NewEncryptorKey(channels Channels) *EncryptorKey {
	return &EncryptorKey{
		channels: channels,
	}
}

func (h *EncryptorKey) Handle(_ context.Context, state *State) *fsm.Result[*State] {
	data, ok := state.Object.(*domain.Encryption)
	if !ok {
		slog.Error(
			"invalid object type",
			slog.Any("type", fmt.Sprintf("%T", state.Object)),
			slog.Any("handler", "EncryptorKey"),
		)

		return &fsm.Result[*State]{
			NextState:        fail,
			IsAutoTransition: true,
			Result:           state,
		}
	}

	pk, err := h.pkFromBase64(state.Message)
	if err != nil {
		state.ShowError = "не удалось прочитать ключ"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to read key: %w", err),
		}
	}

	data.Key = pk

	ans := `Введите сообщение`

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeMarkdown
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		NextState:        encMsg,
		Result:           state,
	}
}

func (h *EncryptorKey) pkFromBase64(key string) (*domain.PublicKey, error) {
	b, err := base64.RawStdEncoding.DecodeString(key)
	if err != nil {
		return nil, fmt.Errorf("failed to decode base64: %w", err)
	}

	var pk domain.PublicKey

	err = json.Unmarshal(b, &pk)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal: %w", err)
	}

	return &pk, nil
}
