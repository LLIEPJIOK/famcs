package domain

import "time"

type Player struct {
	ID         string          `json:"playerId"             db:"id"`
	Jersey     int32           `json:"jersey"               db:"jersey"`
	FirstName  string          `json:"firstName"            db:"first_name"`
	SecondName string          `json:"secondName"           db:"second_name"`
	Position   string          `json:"position"             db:"position"`
	Birthday   Null[time.Time] `json:"birthday,omitempty"   db:"birthday"`
	Weight     Null[int32]     `json:"weight,omitempty"     db:"weight"`
	Height     Null[int32]     `json:"height,omitempty"     db:"height"`
	BirthCity  Null[string]    `json:"birthCity,omitempty"  db:"birth_city"`
	BirthState Null[string]    `json:"birthState,omitempty" db:"birth_state"`
}
