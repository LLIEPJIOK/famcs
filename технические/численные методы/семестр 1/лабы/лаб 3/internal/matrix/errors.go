package matrix

type ErrMatrix struct {
	msg string
}

func NewErrMatrix(msg string) error {
	return ErrMatrix{
		msg: msg,
	}
}

func (e ErrMatrix) Error() string {
	return e.msg
}
