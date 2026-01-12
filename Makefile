.PHONY: up down build test

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

test:
	curl http://localhost:3000/
	curl http://localhost:3000/health
	curl "http://localhost:3000/artist/marina-sena"
	curl "http://localhost:3000/cifra?url=https://www.cifraclub.com.br/marina-sena/lua-cheia/#"