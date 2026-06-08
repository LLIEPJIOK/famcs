package roster

import (
	"context"
	"errors"
	"fmt"

	"github.com/LLIEPJIOK/lab1/internal/domain"
	"github.com/georgysavva/scany/v2/pgxscan"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"
)

type Repository struct {
	db *pgxpool.Pool
}

func New(db *pgxpool.Pool) *Repository {
	return &Repository{
		db: db,
	}
}

const AddPlayerQuery = `
INSERT INTO
	rosters (
		player_id,
		jersey,
		first_name,
		second_name,
		position,
		birthday,
		weight,
		height,
		birth_city,
		birth_state
	)
VALUES
	(
		$1, $2, $3, $4, $5,
		$6, $7, $8, $9, $10
	);
`

func (r *Repository) AddPlayer(ctx context.Context, player *domain.Player) error {
	repoPlayer := domainToRepoPlayer(player)

	_, err := r.db.Exec(ctx, AddPlayerQuery,
		repoPlayer.PlayerID,
		repoPlayer.Jersey,
		repoPlayer.FirstName,
		repoPlayer.SecondName,
		repoPlayer.Position,
		repoPlayer.Birthday,
		repoPlayer.Weight,
		repoPlayer.Height,
		repoPlayer.BirthCity,
		repoPlayer.BirthState,
	)
	if err != nil {
		return fmt.Errorf("failed to add player: %w", err)
	}

	return nil
}

const GetPlayerQuery = `
SELECT
	player_id,
	jersey,
	first_name,
	second_name,
	position,
	birthday,
	weight,
	height,
	birth_city,
	birth_state
FROM
	rosters
WHERE
	player_id = $1
LIMIT
	1;
`

func (r *Repository) GetPlayer(ctx context.Context, id string) (*domain.Player, error) {
	var repoPlayer Player

	err := pgxscan.Get(ctx, r.db, &repoPlayer, GetPlayerQuery, id)
	if errors.Is(err, pgx.ErrNoRows) {
		return nil, NewErrNotFound(id)
	}

	if err != nil {
		return nil, fmt.Errorf("failed to get player: %w", err)
	}

	return repoToDomainPlayer(&repoPlayer), nil
}

const GetPlayersQuery = `
SELECT
	player_id,
	jersey,
	first_name,
	second_name,
	position,
	birthday,
	weight,
	height,
	birth_city,
	birth_state
FROM
	rosters;
`

func (r *Repository) GetPlayers(ctx context.Context) ([]*domain.Player, error) {
	var repoPlayers []Player

	err := pgxscan.Select(ctx, r.db, &repoPlayers, GetPlayersQuery)
	if err != nil {
		return nil, fmt.Errorf("failed to get players: %w", err)
	}

	players := make([]*domain.Player, 0, len(repoPlayers))
	for _, repoPlayer := range repoPlayers {
		players = append(players, repoToDomainPlayer(&repoPlayer))
	}

	return players, nil
}

const UpdatePlayerQuery = `
UPDATE rosters
SET
	jersey = COALESCE(NULLIF($2, 0), jersey),
	first_name = COALESCE(NULLIF($3, ''), first_name),
	second_name = COALESCE(NULLIF($4, ''), second_name),
	position = COALESCE(NULLIF($5, ''), position),
	birthday = COALESCE($6, birthday),
	weight = COALESCE($7, weight),
	height = COALESCE($8, height),
	birth_city = COALESCE($9, birth_city),
	birth_state = COALESCE($10, birth_state)
WHERE
	player_id = $1;
`

func (r *Repository) UpdatePlayer(ctx context.Context, player *domain.Player) error {
	repoPlayer := domainToRepoPlayer(player)

	_, err := r.db.Exec(ctx, UpdatePlayerQuery,
		repoPlayer.PlayerID,
		repoPlayer.Jersey,
		repoPlayer.FirstName,
		repoPlayer.SecondName,
		repoPlayer.Position,
		repoPlayer.Birthday,
		repoPlayer.Weight,
		repoPlayer.Height,
		repoPlayer.BirthCity,
		repoPlayer.BirthState,
	)
	if err != nil {
		return fmt.Errorf("failed to update player: %w", err)
	}

	return nil
}

const DeletePlayerQuery = `
DELETE FROM rosters
WHERE
	player_id = $1;
`

func (r *Repository) DeletePlayer(ctx context.Context, id string) error {
	_, err := r.db.Exec(ctx, DeletePlayerQuery, id)
	if err != nil {
		return fmt.Errorf("failed to delete player: %w", err)
	}

	return nil
}
