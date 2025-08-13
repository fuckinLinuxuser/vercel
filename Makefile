prod-up-detached:
	docker compose -f prod/docker-compose.yml up --build -d
	
prod-up:
	docker compose -f prod/docker-compose.yml up --build

prod-down:
	docker compose -f prod/docker-compose.yml down

dev-up-detached:
	docker compose -f develop/docker-compose.yml up --build -d

dev-up:
	docker compose -f develop/docker-compose.yml up --build 

dev-down:
	docker compose -f develop/docker-compose.yml down
