package processor

import (
	"github.com/LLIEPJIOK/go-common/fsm"
)

const (
	callback fsm.State = "callback"
	command  fsm.State = "command"

	start fsm.State = "start"

	help fsm.State = "help"

	gen     fsm.State = "gen"
	genBits fsm.State = "gen_bits"

	enc    fsm.State = "enc"
	encKey fsm.State = "enc_key"
	encMsg fsm.State = "enc_msg"

	dec    fsm.State = "dec"
	decMsg fsm.State = "dec_msg"

	fail fsm.State = "fail"
)

type State struct {
	FSMState  fsm.State
	ChatID    int64
	MessageID int
	Message   string
	Object    any
	ShowError string
}
