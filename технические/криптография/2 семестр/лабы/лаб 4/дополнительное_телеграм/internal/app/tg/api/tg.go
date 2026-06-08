package api

import (
	"cm_lab4_tg/internal/domain"
	"context"
	"fmt"
	"log/slog"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

const (
	initialOffset  = 0
	timeoutSeconds = 60
)

type API interface {
	Request(c tgbotapi.Chattable) (*tgbotapi.APIResponse, error)
	GetUpdatesChan(config tgbotapi.UpdateConfig) tgbotapi.UpdatesChannel
	Send(c tgbotapi.Chattable) (tgbotapi.Message, error)
}

type Channels interface {
	TelegramReq() chan domain.TelegramRequest
	TelegramResp() chan tgbotapi.Chattable
}

type Bot struct {
	api      API
	channels Channels
}

func New(api API, channels Channels) (*Bot, error) {
	bot := &Bot{
		api:      api,
		channels: channels,
	}

	if err := bot.setCommands(); err != nil {
		return nil, fmt.Errorf("bot.setCommands(): %w", err)
	}

	return bot, nil
}

func (b *Bot) Run(ctx context.Context) error {
	u := tgbotapi.NewUpdate(initialOffset)
	u.Timeout = timeoutSeconds
	updates := b.api.GetUpdatesChan(u)

	for {
		select {
		case <-ctx.Done():
			return nil

		case update := <-updates:
			switch {
			case update.Message != nil:
				b.channels.TelegramReq() <- domain.TelegramRequest{
					ChatID:  update.Message.Chat.ID,
					Message: update.Message.Text,
					Type:    b.getMessageType(update.Message),
				}

			case update.CallbackQuery != nil:
				b.channels.TelegramReq() <- domain.TelegramRequest{
					ChatID:    update.CallbackQuery.Message.Chat.ID,
					MessageID: update.CallbackQuery.Message.MessageID,
					Message:   update.CallbackQuery.Data,
					Type:      domain.Callback,
				}
			}

		case resp := <-b.channels.TelegramResp():
			_, err := b.api.Send(resp)
			if err != nil {
				slog.Error("bot.Start()", slog.Any("error", err))
			}
		}
	}
}

func (b *Bot) setCommands() error {
	commands := tgbotapi.NewSetMyCommands(
		tgbotapi.BotCommand{
			Command:     "start",
			Description: "Приветственное сообщение",
		},
		tgbotapi.BotCommand{
			Command:     "help",
			Description: "Вывод списка доступных команд",
		},
		tgbotapi.BotCommand{
			Command:     "gen",
			Description: "Сгенерировать ключи",
		},
		tgbotapi.BotCommand{
			Command:     "enc",
			Description: "Зашифровать сообщение",
		},
		tgbotapi.BotCommand{
			Command:     "dec",
			Description: "Расшифровать сообщение",
		},
	)

	if _, err := b.api.Request(commands); err != nil {
		return fmt.Errorf("failed to set commands: %w", err)
	}

	return nil
}

func (b *Bot) getMessageType(msg *tgbotapi.Message) domain.TgReqType {
	if msg.IsCommand() {
		return domain.Command
	}

	return domain.Message
}
