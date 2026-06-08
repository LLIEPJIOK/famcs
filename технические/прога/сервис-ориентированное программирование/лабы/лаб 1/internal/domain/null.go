package domain

import "encoding/json"

type Null[T any] struct {
	Value T
	Valid bool
}

func (n *Null[T]) UnmarshalJSON(data []byte) error {
	if string(data) == "null" {
		n.Valid = false

		return nil
	}

	var value T
	if err := json.Unmarshal(data, &value); err != nil {
		return err
	}

	n.Value = value
	n.Valid = true

	return nil
}

func (n Null[T]) MarshalJSON() ([]byte, error) {
	if !n.Valid {
		return []byte("null"), nil
	}

	return json.Marshal(n.Value)
}
