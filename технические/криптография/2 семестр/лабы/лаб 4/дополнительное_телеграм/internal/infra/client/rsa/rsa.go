package rsa

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"log/slog"
	"net/http"
	"time"

	"cm_lab4_tg/internal/config"
	"cm_lab4_tg/internal/domain"
)

type RSA struct {
	client *http.Client
	URL    string
}

func New(cfg *config.RSA) *RSA {
	return &RSA{
		client: &http.Client{
			Timeout: 60 * time.Second,
		},
		URL: cfg.URL,
	}
}

func (rsa *RSA) GenerateKeys(ctx context.Context, bits int) (*domain.Keys, error) {
	data := struct {
		Bits int `json:"bits"`
	}{
		Bits: bits,
	}

	raw, err := json.Marshal(data)
	if err != nil {
		return nil, fmt.Errorf("error marshaling RSA keys: %w", err)
	}

	req, err := http.NewRequestWithContext(
		ctx,
		http.MethodPost,
		rsa.URL+"/generate_keys",
		bytes.NewReader(raw),
	)
	if err != nil {
		return nil, fmt.Errorf("failed to create http request: %w", err)
	}

	resp, err := rsa.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to send http request: %w", err)
	}

	defer func() {
		if err := resp.Body.Close(); err != nil {
			log.Printf("failed to close response body")
		}
	}()

	if resp.StatusCode != http.StatusOK {
		return nil, NewErrUnexpectedStatusCode(resp.StatusCode)
	}

	var keys domain.Keys

	if err := json.NewDecoder(resp.Body).Decode(&keys); err != nil {
		slog.Error("failed to close response body", slog.Any("error", err))
	}

	return &keys, nil
}

func (rsa *RSA) Encrypt(ctx context.Context, data *domain.Encryption) (string, error) {
	encrypt := struct {
		E       string `json:"e"`
		N       string `json:"n"`
		Message string `json:"message"`
	}{
		E:       data.Key.E,
		N:       data.Key.N,
		Message: data.Message,
	}

	rawEncrypt, err := json.Marshal(encrypt)
	if err != nil {
		return "", fmt.Errorf("failed to encode http request: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, rsa.URL+"/encrypt", bytes.NewReader(rawEncrypt))
	if err != nil {
		return "", fmt.Errorf("failed to create http request: %w", err)
	}

	resp, err := rsa.client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to send http request: %w", err)
	}

	defer func() {
		if err := resp.Body.Close(); err != nil {
			slog.Error("failed to close response body", slog.Any("error", err))
		}
	}()

	if resp.StatusCode != http.StatusOK {
		return "", NewErrUnexpectedStatusCode(resp.StatusCode)
	}

	cipher := struct {
		Cipher string `json:"cipher"`
	}{}

	if err := json.NewDecoder(resp.Body).Decode(&cipher); err != nil {
		return "", fmt.Errorf("failed to decode response body: %w", err)
	}

	return cipher.Cipher, nil
}

func (rsa *RSA) Decrypt(ctx context.Context, key *domain.PrivateKey, cipher string) (string, error) {
	decrypt := struct {
		D      string `json:"d"`
		N      string `json:"n"`
		P      string `json:"p"`
		Q      string `json:"q"`
		Cipher string `json:"cipher"`
	}{
		D:      key.D,
		N:      key.N,
		P:      key.P,
		Q:      key.Q,
		Cipher: cipher,
	}

	rawDecrypt, err := json.Marshal(decrypt)
	if err != nil {
		return "", fmt.Errorf("failed to encode http request: %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, rsa.URL+"/decrypt", bytes.NewReader(rawDecrypt))
	if err != nil {
		return "", fmt.Errorf("failed to create http request: %w", err)
	}

	resp, err := rsa.client.Do(req)
	if err != nil {
		return "", fmt.Errorf("failed to send http request: %w", err)
	}

	defer func() {
		if err := resp.Body.Close(); err != nil {
			slog.Error("failed to close response body", slog.Any("error", err))
		}
	}()

	if resp.StatusCode != http.StatusOK {
		return "", NewErrUnexpectedStatusCode(resp.StatusCode)
	}

	msg := struct {
		Message string `json:"decrypted"`
	}{}

	if err := json.NewDecoder(resp.Body).Decode(&msg); err != nil {
		return "", fmt.Errorf("failed to decode response body: %w", err)
	}

	return msg.Message, nil
}
