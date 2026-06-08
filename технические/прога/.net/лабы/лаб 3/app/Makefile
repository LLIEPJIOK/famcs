.PHONY: run
run:
	dotnet run

.PHONY: migrate
migrate:
	docker-compose up -d --force-recreate --build --remove-orphans
	dotnet ef database update