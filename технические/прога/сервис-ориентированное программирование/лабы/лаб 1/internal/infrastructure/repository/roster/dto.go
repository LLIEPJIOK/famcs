package roster

import (
	"time"

	"github.com/LLIEPJIOK/lab1/internal/domain"
	"github.com/jackc/pgx/v5/pgtype"
)

type Player struct {
	PlayerID   string      `db:"player_id"`
	Jersey     int32       `db:"jersey"`
	FirstName  string      `db:"first_name"`
	SecondName string      `db:"second_name"`
	Position   string      `db:"position"`
	Birthday   pgtype.Date `db:"birthday"`
	Weight     pgtype.Int4 `db:"weight"`
	Height     pgtype.Int4 `db:"height"`
	BirthCity  pgtype.Text `db:"birth_city"`
	BirthState pgtype.Text `db:"birth_state"`
}

func domainToRepoPlayer(player *domain.Player) *Player {
	return &Player{
		PlayerID:   player.ID,
		Jersey:     player.Jersey,
		FirstName:  player.FirstName,
		SecondName: player.SecondName,
		Position:   player.Position,
		Birthday:   pgtype.Date{Time: player.Birthday.Value, Valid: player.Birthday.Valid},
		Weight:     pgtype.Int4{Int32: player.Weight.Value, Valid: player.Weight.Valid},
		Height:     pgtype.Int4{Int32: player.Height.Value, Valid: player.Height.Valid},
		BirthCity:  pgtype.Text{String: player.BirthCity.Value, Valid: player.BirthCity.Valid},
		BirthState: pgtype.Text{String: player.BirthState.Value, Valid: player.BirthState.Valid},
	}
}

func repoToDomainPlayer(player *Player) *domain.Player {
	return &domain.Player{
		ID:         player.PlayerID,
		Jersey:     player.Jersey,
		FirstName:  player.FirstName,
		SecondName: player.SecondName,
		Position:   player.Position,
		Birthday: domain.Null[time.Time]{
			Value: player.Birthday.Time,
			Valid: player.Birthday.Valid,
		},
		Weight: domain.Null[int32]{Value: player.Weight.Int32, Valid: player.Weight.Valid},
		Height: domain.Null[int32]{Value: player.Height.Int32, Valid: player.Height.Valid},
		BirthCity: domain.Null[string]{
			Value: player.BirthCity.String,
			Valid: player.BirthCity.Valid,
		},
		BirthState: domain.Null[string]{
			Value: player.BirthState.String,
			Valid: player.BirthState.Valid,
		},
	}
}
