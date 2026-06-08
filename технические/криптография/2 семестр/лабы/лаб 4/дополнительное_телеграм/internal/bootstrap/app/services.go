package app

import (
	"context"
	"log/slog"
	"sync"

	tgapi "cm_lab4_tg/internal/app/tg/api"
	"cm_lab4_tg/internal/app/tg/processor"
	"cm_lab4_tg/internal/infra/client/rsa"
	"cm_lab4_tg/internal/infra/repo"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type runService = func(ctx context.Context, stop context.CancelFunc, wg *sync.WaitGroup)

func (a *App) services() []runService {
	return []runService{
		a.runBot,
		a.runProcessor,
	}
}

func (a *App) runBot(ctx context.Context, stop context.CancelFunc, wg *sync.WaitGroup) {
	defer wg.Done()
	defer stop()
	defer slog.Info("bot stopped")

	api, err := tgbotapi.NewBotAPI(a.cfg.Bot.APIToken)
	if err != nil {
		slog.Error("failed to create bot api", slog.Any("err", err))

		return
	}

	api.Debug = true

	slog.Info("bot started", slog.Any("username", api.Self.UserName))

	tgBot, err := tgapi.New(api, a.channels)
	if err != nil {
		slog.Error("failed to create bot", slog.Any("err", err))

		return
	}

	if err := tgBot.Run(ctx); err != nil {
		slog.Error("failed to run bot", slog.Any("err", err))
	}
}

func (a *App) runProcessor(ctx context.Context, stop context.CancelFunc, wg *sync.WaitGroup) {
	defer wg.Done()
	defer stop()
	defer slog.Info("processor stopped")

	client := rsa.New(&a.cfg.RSA)
	r := repo.New()
	proc := processor.New(client, a.channels, r)

	if err := proc.Run(ctx); err != nil {
		slog.Error("failed to run processor", slog.Any("err", err))
	}
}
