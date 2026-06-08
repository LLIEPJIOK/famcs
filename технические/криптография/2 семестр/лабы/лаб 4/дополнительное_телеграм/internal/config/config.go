package config

import (
	"fmt"
	"github.com/caarlos0/env/v11"
	"time"
)

type Config struct {
	App App `envPrefix:"APP_"`
	Bot Bot `envPrefix:"BOT_"`
	RSA RSA `envPrefix:"RSA_"`
}

type App struct {
	Env              string        `env:"ENV"               envDefault:"local"`
	TerminateTimeout time.Duration `env:"TERMINATE_TIMEOUT" envDefault:"5s"`
	ShutdownTimeout  time.Duration `env:"SHUTDOWN_TIMEOUT"  envDefault:"2s"`
}

type Bot struct {
	APIToken string `env:"API_TOKEN,required"`
}

type RSA struct {
	URL string `env:"URL" envDefault:"http://localhost:8000"`
}

func Load() (*Config, error) {
	config := &Config{}

	if err := env.Parse(config); err != nil {
		return nil, fmt.Errorf("failed to parse env: %w", err)
	}

	return config, nil
}
