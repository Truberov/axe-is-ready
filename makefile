all:
	@echo "make env	- create env file"
	@echo "make up	- Run apps from docker compose"
	@exit 0

env:
	@if [ -f .env ]; then \
		echo ".env file already exists. Skipping creation."; \
	else \
		echo "Creating .env file from .env_example..."; \
		cp .env_example .env; \
		echo ".env file created successfully."; \
	fi

up:
	@echo "Starting docker-compose..."
	@docker compose -f docker-compose.yml up -d --build
	@echo "Docker-compose started successfully."