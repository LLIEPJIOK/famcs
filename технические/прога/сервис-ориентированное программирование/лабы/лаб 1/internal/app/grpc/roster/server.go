package roster

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/LLIEPJIOK/lab1/internal/domain"
	repo "github.com/LLIEPJIOK/lab1/internal/infrastructure/repository/roster"
	"github.com/gorilla/mux"
)

// Repository defines the methods our HTTP handlers will use.
type Repository interface {
	AddPlayer(ctx context.Context, player *domain.Player) error
	GetPlayer(ctx context.Context, id string) (*domain.Player, error)
	GetPlayers(ctx context.Context) ([]*domain.Player, error)
	UpdatePlayer(ctx context.Context, player *domain.Player) error
	DeletePlayer(ctx context.Context, id string) error
}

// Server holds dependencies for the HTTP service.
type Server struct {
	repo Repository
}

// NewServer constructs a new Server with the given repo.
func NewServer(r Repository) *Server {
	return &Server{repo: r}
}

// RegisterRoutes attaches routes to the given router.
func (s *Server) RegisterRoutes(r *mux.Router) {
	r.HandleFunc("/v1/players", s.handleListPlayers).Methods(http.MethodGet)
	r.HandleFunc("/v1/players/{id}", s.handleGetPlayer).Methods(http.MethodGet)
	r.HandleFunc("/v1/players", s.handleAddPlayer).Methods(http.MethodPost)
	r.HandleFunc("/v1/players/{id}", s.handleUpdatePlayer).Methods(http.MethodPut)
	r.HandleFunc("/v1/players/{id}", s.handleDeletePlayer).Methods(http.MethodDelete)
}

// JSONError writes a JSON-formatted error message.
func JSONError(w http.ResponseWriter, status int, err error) {
	fmt.Println(err)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(map[string]string{"error": err.Error()})
}

// handleAddPlayer processes POST /players
func (s *Server) handleAddPlayer(w http.ResponseWriter, r *http.Request) {
	var dto struct {
		Player *domain.Player `json:"player"`
	}
	if err := json.NewDecoder(r.Body).Decode(&dto); err != nil {
		JSONError(w, http.StatusBadRequest, err)
		return
	}

	if err := validate(dto.Player); err != nil {
		JSONError(w, http.StatusBadRequest, err)
		return
	}
	if err := s.repo.AddPlayer(r.Context(), dto.Player); err != nil {
		JSONError(w, http.StatusInternalServerError, err)
		return
	}
	w.WriteHeader(http.StatusCreated)
}

// handleGetPlayer processes GET /players/{id}
func (s *Server) handleGetPlayer(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	player, err := s.repo.GetPlayer(r.Context(), id)
	if err != nil {
		var notFound repo.ErrNotFound
		if errors.As(err, &notFound) {
			JSONError(w, http.StatusNotFound, err)
		} else {
			JSONError(w, http.StatusInternalServerError, err)
		}
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(player)
}

// handleListPlayers processes GET /players
func (s *Server) handleListPlayers(w http.ResponseWriter, r *http.Request) {
	players, err := s.repo.GetPlayers(r.Context())
	if err != nil {
		JSONError(w, http.StatusInternalServerError, err)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]interface{}{"players": players})
}

// handleUpdatePlayer processes PUT /players/{id}
func (s *Server) handleUpdatePlayer(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	var dto struct {
		Player *domain.Player `json:"player"`
	}
	if err := json.NewDecoder(r.Body).Decode(&dto); err != nil {
		JSONError(w, http.StatusBadRequest, err)
		return
	}
	if dto.Player.ID != id {
		JSONError(w, http.StatusBadRequest, errors.New("path id and body id mismatch"))
		return
	}
	if err := validate(dto.Player); err != nil {
		JSONError(w, http.StatusBadRequest, err)
		return
	}
	if err := s.repo.UpdatePlayer(r.Context(), dto.Player); err != nil {
		JSONError(w, http.StatusInternalServerError, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// handleDeletePlayer processes DELETE /players/{id}
func (s *Server) handleDeletePlayer(w http.ResponseWriter, r *http.Request) {
	id := mux.Vars(r)["id"]
	if err := s.repo.DeletePlayer(r.Context(), id); err != nil {
		JSONError(w, http.StatusInternalServerError, err)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ValidationError aggregates multiple validation errors.
type ValidationError struct {
	Errors []string `json:"errors"`
}

// Error implements the error interface.
func (v *ValidationError) Error() string {
	return "validation failed: " + strings.Join(v.Errors, ", ")
}

// Add appends a new error message.
func (v *ValidationError) Add(msg string) {
	v.Errors = append(v.Errors, msg)
}

// validate mirrors gRPC validation logic for domain.Player.
func validate(p *domain.Player) error {
	var verr ValidationError

	if len(p.ID) == 0 {
		verr.Add("player id cannot be empty")
	}
	if p.Jersey == 0 {
		verr.Add("player jersey cannot be empty")
	} else if p.Jersey < 0 {
		verr.Add("player jersey should be positive")
	}
	if len(p.FirstName) == 0 {
		verr.Add("player first name cannot be empty")
	}
	if len(p.SecondName) == 0 {
		verr.Add("player second name cannot be empty")
	}
	if len(p.Position) == 0 {
		verr.Add("player position cannot be empty")
	}
	if p.Height.Valid && p.Height.Value <= 0 {
		verr.Add("player height should be positive")
	}
	if p.Weight.Valid && p.Weight.Value <= 0 {
		verr.Add("player weight should be positive")
	}
	// Birthday is optional; if year zero, skip.
	if p.Birthday.Valid {
		if p.Birthday.Value.After(time.Now()) {
			verr.Add("player birthday cannot be in the future")
		}
	}
	// BirthCity and BirthState are optional, no extra checks.

	if len(verr.Errors) > 0 {
		return &verr
	}
	return nil
}
