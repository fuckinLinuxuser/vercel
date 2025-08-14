prod-up-detached:
	@sudo bash ./pid_check.sh && \
	docker compose -f prod/docker-compose.yml up --build -d
	
prod-up:
	@sudo bash ./pid_check.sh && \
	docker compose -f prod/docker-compose.yml up --build

prod-down:
	docker compose -f prod/docker-compose.yml down

dev-up-detached:
	@sudo bash ./pid_check.sh && \
	docker compose -f develop/docker-compose.yml up --build -d

dev-up:
	@sudo bash ./pid_check.sh && \
	docker compose -f develop/docker-compose.yml up --build 

dev-down:
	@docker compose -f develop/docker-compose.yml down
