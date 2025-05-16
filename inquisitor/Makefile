up:
	docker-compose up -d 


down:
	docker-compose  down

db:
	docker exec backend python3 manage.py loaddata build-tools/test_users.json

fclean: down
	docker rmi $$(docker images -a -q) &2>/dev/null
	docker network rm $$(docker network ls -q) &2>/dev/null
	docker volume rm $$(docker volume ls -q | grep -v "ollama") &2>/dev/null

clean_cache: fclean
	docker system prune -a

clear_volume: down
	docker volume rm $$(docker volume ls -q | grep -v "ollama") &2>/dev/null

logs:
	docker-compose logs -f

network:
	docker network inspect inquisitor_testnet

shell-attacker:
	docker exec -it Attacker zsh

shell-client:
	docker exec -it FTP_Client bash

shell-server:
	docker exec -it FTP_Server bash
