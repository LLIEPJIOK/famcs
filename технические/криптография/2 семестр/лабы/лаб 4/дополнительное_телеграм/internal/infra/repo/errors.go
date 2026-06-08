package repo

type ErrNotFound struct {
}

func NewErrNotFound() error {
	return ErrNotFound{}
}

func (e ErrNotFound) Error() string {
	return "not found"
}
