package main

import (
	"context"
	"database/sql"
	"flag"
	"log/slog"
	"os"

	"github.com/LLIEPJIOK/lab1/internal/config"
	"github.com/pressly/goose/v3"

	_ "github.com/lib/pq"
)

const (
	OkCode = iota
	ErrorConfigLoad
	ErrorConnectDatabase
	ErrorMigrate
)

func main() {
	var cmd string

	flag.StringVar(&cmd, "command", "up", "Migration command")
	flag.Parse()

	cfg, err := config.Load()
	if err != nil {
		os.Exit(ErrorConfigLoad)
	}

	os.Exit(migrate(cfg, cmd))
}

func migrate(cfg *config.Config, cmd string) (code int) {
	db, err := sql.Open("postgres", cfg.Database.DSN)
	if err != nil {
		slog.Error("Error connect to database", slog.Any("error", err))

		return ErrorConnectDatabase
	}

	if err := db.Ping(); err != nil {
		slog.Error("Error ping database", slog.Any("error", err))

		return ErrorConnectDatabase
	}

	defer func() {
		if err := db.Close(); err != nil {
			slog.Error("Error close %s database", slog.Any("error", err))
		}
	}()

	if err = goose.RunContext(context.Background(), cmd, db, "./migrations"); err != nil {
		slog.Error("Error migrate %s database", slog.Any("error", err))

		return ErrorMigrate
	}

	return OkCode
}
