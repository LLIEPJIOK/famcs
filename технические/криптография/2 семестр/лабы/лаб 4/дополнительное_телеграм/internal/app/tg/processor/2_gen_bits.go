package processor

import (
	"context"
	"fmt"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"log/slog"
	"strconv"
)

type GeneratorBits struct {
	channels Channels
	client   Client
	repo     Repo
}

func NewGeneratorBits(channels Channels, client Client, repo Repo) *GeneratorBits {
	return &GeneratorBits{
		channels: channels,
		client:   client,
		repo:     repo,
	}
}

func (h *GeneratorBits) Handle(ctx context.Context, state *State) *fsm.Result[*State] {
	bits, err := strconv.Atoi(state.Message)
	if err != nil || bits <= 0 {
		ans := `Количество должно быть натуральным числом!`

		msg := tgbotapi.NewMessage(state.ChatID, ans)
		msg.ParseMode = tgbotapi.ModeMarkdown
		h.channels.TelegramResp() <- msg

		return &fsm.Result[*State]{
			IsAutoTransition: false,
			NextState:        genBits,
			Result:           state,
		}
	}

	keys, err := h.client.GenerateKeys(ctx, bits)
	if err != nil {
		state.ShowError = "ошибка генерации ключей"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to generate keys: %w", err),
		}
	}

	err = h.repo.SetKeys(ctx, state.ChatID, keys)
	if err != nil {
		slog.Error("failed to save keys", slog.Any(
			"chat_id",
			state.ChatID,
		), slog.Any("error", err))
	}

	publicToken, err := keys.PublicKey.Key()
	if err != nil {
		state.ShowError = "ошибка генерации ключа"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to generate key: %w", err),
		}
	}

	privateToken, err := keys.PrivateKey.Key()
	if err != nil {
		state.ShowError = "ошибка генерации ключа"

		return &fsm.Result[*State]{
			IsAutoTransition: true,
			NextState:        fail,
			Result:           state,
			Error:            fmt.Errorf("failed to generate key: %w", err),
		}
	}
	ans := fmt.Sprintf(
		"Открытый ключ: %v\nЛичный ключ: <tg-spoiler>%v</tg-spoiler>",
		publicToken,
		privateToken,
	)

	msg := tgbotapi.NewMessage(state.ChatID, ans)
	msg.ParseMode = tgbotapi.ModeHTML
	h.channels.TelegramResp() <- msg

	return &fsm.Result[*State]{
		IsAutoTransition: false,
		Result:           state,
	}
}
