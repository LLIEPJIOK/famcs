package main

import (
	"log/slog"

	"github.com/LLIEPJIOK/eigenvalues/internal/application/eigenvalues"
)

func main() {
	if err := eigenvalues.Start(); err != nil {
		slog.Error("eigenvalues.Start()", slog.Any("error", err))
	}
}
