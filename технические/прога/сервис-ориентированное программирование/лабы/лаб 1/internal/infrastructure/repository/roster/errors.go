package roster

import "fmt"

type ErrNotFound struct {
	ID string
}

func NewErrNotFound(id string) error {
	return ErrNotFound{
		ID: id,
	}
}

func (e ErrNotFound) Error() string {
	return fmt.Sprintf("player with id %q not found", e.ID)
}
