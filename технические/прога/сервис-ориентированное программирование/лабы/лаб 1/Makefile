ifneq (,$(wildcard .env))
	include .env
	export $(shell sed 's/=.*//' .env)
endif

file=coverage.count.tmp
GO_MODULE=lab3

.PHONY: migrate
migrate:
	go run ./cmd/migration/main.go up || cd ..

.PHONY: run
run:
	go run ./cmd/lab3/main.go

.PHONY: lint
lint:
	@echo "lint started"
	@golangci-lint run
	@echo "lint finished"

.PHONY: test
test:
	go test ./... -cover -race

.PHONY: .sqlc
.sqlc:
	sqlc vet -f ./sqlc/sqlc.yaml
	sqlc generate -f ./sqlc/sqlc.yaml
	sqlc diff -f ./sqlc/sqlc.yaml

.PHONY: cover
cover:
	go tool cover -html coverage.out -o coverage.html
	open coverage.html

.PHONY: generate_proto
generate_proto:
	@if ! command -v 'easyp' &> /dev/null; then \
		echo "Please install easyp!"; exit 1; \
	fi;
	mkdir -p pkg
	@easyp generate
