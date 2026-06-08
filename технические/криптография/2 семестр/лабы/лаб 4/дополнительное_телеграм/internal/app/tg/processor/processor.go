package processor

import (
	"context"
	"log/slog"
	"sync"

	"cm_lab4_tg/internal/domain"
	"github.com/LLIEPJIOK/go-common/fsm"
	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

const numWorkers = 10

type Client interface {
	GenerateKeys(ctx context.Context, bits int) (*domain.Keys, error)
	Encrypt(ctx context.Context, data *domain.Encryption) (string, error)
	Decrypt(ctx context.Context, key *domain.PrivateKey, cipher string) (string, error)
}

type Repo interface {
	SetKeys(ctx context.Context, chatID int64, keys *domain.Keys) error
	GetKeys(ctx context.Context, chatID int64) (*domain.Keys, error)
}

type Channels interface {
	TelegramReq() chan domain.TelegramRequest
	TelegramResp() chan tgbotapi.Chattable
}

type Cache interface {
	GetListLinks(
		ctx context.Context,
		chatID int64,
		tag string,
	) (string, error)
	SetListLinks(
		ctx context.Context,
		chatID int64,
		tag string,
		list string,
	) error
	InvalidateListLinks(ctx context.Context, chatID int64) error
}

type Processor struct {
	fsm      *fsm.FSM[*State]
	client   Client
	channels Channels
	mu       sync.RWMutex
	states   map[int64]*State
}

func New(client Client, channels Channels, repo Repo) *Processor {
	fsmBuilder := fsm.NewBuilder[*State]()
	fsmBuilder.
		AddState(callback, NewCallbacker(channels)).
		AddState(command, NewCommander()).
		AddState(start, NewStater(channels)).
		AddState(help, NewHelper(channels)).
		AddState(gen, NewGenerator(channels)).
		AddState(genBits, NewGeneratorBits(channels, client, repo)).
		AddState(enc, NewEncryptor(channels)).
		AddState(encKey, NewEncryptorKey(channels)).
		AddState(encMsg, NewEncryptorMessage(channels, client)).
		AddState(dec, NewDecrypt(channels)).
		AddState(decMsg, NewDecryptMessage(channels, client, repo)).
		AddState(fail, NewFailer(channels)).
		AddTransition(callback, fail).
		AddTransition(command, start).
		AddTransition(command, help).
		AddTransition(command, gen).
		AddTransition(command, enc).
		AddTransition(command, dec).
		AddTransition(command, fail).
		AddTransition(gen, genBits).
		AddTransition(genBits, fail).
		AddTransition(enc, encKey).
		AddTransition(encKey, fail).
		AddTransition(encMsg, fail).
		AddTransition(dec, decMsg).
		AddTransition(decMsg, fail)

	return &Processor{
		client:   client,
		channels: channels,
		fsm:      fsmBuilder.Build(),
		mu:       sync.RWMutex{},
		states:   make(map[int64]*State),
	}
}

func (p *Processor) GetState(chatID int64) (*State, bool) {
	p.mu.RLock()
	defer p.mu.RUnlock()

	state, ok := p.states[chatID]

	return state, ok
}

func (p *Processor) SetState(chatID int64, state *State) {
	p.mu.Lock()
	defer p.mu.Unlock()

	p.states[chatID] = state
}

func (p *Processor) Run(ctx context.Context) error {
	workCh := make(chan *State, numWorkers)
	defer close(workCh)

	for range numWorkers {
		go p.worker(ctx, workCh)
	}

	for {
		select {
		case <-ctx.Done():
			return nil

		case req := <-p.channels.TelegramReq():
			switch req.Type {
			case domain.Message:
				slog.Info("getting message", slog.Any("message", req.Message))

				state, ok := p.GetState(req.ChatID)
				if !ok || state.FSMState.String() == "" {
					workCh <- &State{
						FSMState:  fail,
						ChatID:    req.ChatID,
						ShowError: "неопознанная команда",
					}

					continue
				}

				state.Message = req.Message
				state.MessageID = 0
				workCh <- state

			case domain.Command:
				slog.Info("getting command", slog.Any("command", req.Message))

				workCh <- &State{
					FSMState: command,
					ChatID:   req.ChatID,
					Message:  req.Message,
				}

			case domain.Callback:
				slog.Info("getting callback", slog.Any("callback", req.Message))

				state, ok := p.GetState(req.ChatID)
				if !ok || state.FSMState != callback {
					workCh <- &State{
						FSMState:  fail,
						ChatID:    req.ChatID,
						MessageID: req.MessageID,
						ShowError: "неопознанная команда",
					}

					continue
				}

				state.Message = req.Message
				state.MessageID = req.MessageID
				workCh <- state

			default:
				slog.Warn("unknown request type", slog.Any("type", req.Type))
				continue
			}
		}
	}
}
