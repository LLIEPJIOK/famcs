package config_test

import (
	"os"
	"testing"
	"time"

	"github.com/LLIEPJIOK/lab1/internal/config"
	"github.com/stretchr/testify/assert"
)

func TestLoad_Success(t *testing.T) {
	assert.NoError(t, os.Setenv("DATABASE_HOST", "localhost"))
	assert.NoError(t, os.Setenv("DATABASE_PORT", "5432"))
	assert.NoError(t, os.Setenv("DATABASE_USER", "user"))
	assert.NoError(t, os.Setenv("DATABASE_PASSWORD", "password"))
	assert.NoError(t, os.Setenv("DATABASE_NAME", "name"))
	assert.NoError(t, os.Setenv("DATABASE_SSL_MODE", "disable"))

	os.Unsetenv("APP_TERMINATE_TIMEOUT")
	os.Unsetenv("APP_SHUTDOWN_TIMEOUT")
	os.Unsetenv("APP_PORT")

	config, err := config.Load()
	assert.NoError(t, err, "expected no error loading configuration")

	assert.Equal(t, 5*time.Second, config.App.TerminateTimeout, "unexpected App.TerminateTimeout")
	assert.Equal(t, 2*time.Second, config.App.ShutdownTimeout, "unexpected App.ShutdownTimeout")
	assert.Equal(t, 8080, config.App.Port, "unexpected App.Port")
	assert.Equal(
		t,
		"host=localhost port=5432 user=user password=password dbname=name sslmode=disable",
		config.Database.DSN,
		"unexpected Database.DSN",
	)
}

func TestLoad_MissingRequired(t *testing.T) {
	os.Unsetenv("DATABASE_HOST")
	os.Unsetenv("DATABASE_PORT")
	os.Unsetenv("DATABASE_USER")
	os.Unsetenv("DATABASE_PASSWORD")
	os.Unsetenv("DATABASE_NAME")
	os.Unsetenv("DATABASE_SSL_MODE")

	_, err := config.Load()
	assert.Error(t, err, "expected error due to missing required environment variables")
}
