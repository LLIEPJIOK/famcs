package domain

import (
	"encoding/base64"
	"encoding/json"
	"fmt"
)

type Keys struct {
	PublicKey  *PublicKey  `json:"public_key"`
	PrivateKey *PrivateKey `json:"private_key"`
}

type PublicKey struct {
	E string `json:"e"`
	N string `json:"n"`
}

func (k *PublicKey) Key() (string, error) {
	b, err := json.Marshal(k)
	if err != nil {
		return "", fmt.Errorf("failed to marshal: %w", err)
	}

	return base64.RawStdEncoding.EncodeToString(b), nil
}

type PrivateKey struct {
	D string `json:"d"`
	N string `json:"n"`
	P string `json:"p"`
	Q string `json:"q"`
}

func (k *PrivateKey) Key() (string, error) {
	b, err := json.Marshal(k)
	if err != nil {
		return "", fmt.Errorf("failed to marshal: %w", err)
	}

	return base64.RawStdEncoding.EncodeToString(b), nil
}
