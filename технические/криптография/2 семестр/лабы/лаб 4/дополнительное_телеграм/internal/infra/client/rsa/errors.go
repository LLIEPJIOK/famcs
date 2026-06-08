package rsa

import "fmt"

type ErrUnexpectedStatusCode struct {
	Code int
}

func NewErrUnexpectedStatusCode(code int) *ErrUnexpectedStatusCode {
	return &ErrUnexpectedStatusCode{
		Code: code,
	}
}

func (err *ErrUnexpectedStatusCode) Error() string {
	return fmt.Sprintf("unexpected status code: %d", err.Code)
}
