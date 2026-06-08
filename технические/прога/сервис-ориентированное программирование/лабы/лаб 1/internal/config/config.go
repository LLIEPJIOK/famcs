package config

import (
	"fmt"
	"time"

	"github.com/caarlos0/env/v11"
)

type Config struct {
	App      App      `envPrefix:"APP_"`
	Database Database `envPrefix:"DATABASE_"`
}

type App struct {
	TerminateTimeout time.Duration `env:"TERMINATE_TIMEOUT" envDefault:"5s"`
	ShutdownTimeout  time.Duration `env:"SHUTDOWN_TIMEOUT"  envDefault:"2s"`
	Port             int           `env:"PORT"              envDefault:"8080"`
}

type Database struct {
	DSN      string
	Host     string `env:"HOST,required"`
	Port     string `env:"PORT,required"`
	User     string `env:"USER,required"`
	Password string `env:"PASSWORD,required"`
	Name     string `env:"NAME,required"`
	SSLMode  string `env:"SSL_MODE,required"`
}

func Load() (*Config, error) {
	config := &Config{}

	if err := env.Parse(config); err != nil {
		return nil, fmt.Errorf("failed to parse env: %w", err)
	}

	config.Database.DSN = fmt.Sprintf(
		"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
		config.Database.Host,
		config.Database.Port,
		config.Database.User,
		config.Database.Password,
		config.Database.Name,
		config.Database.SSLMode,
	)

	return config, nil
}
