# ============================================
# CONFIGURATION
# ============================================
IMAGE_NAME = ligadonbassa:1.0.0
APP_CONTAINER = ligadonbassa-container
DB_CONTAINER = ligadonbassa-db
NETWORK = web
DOMAIN = ligadonbassa.ru

# ============================================
# DOCKER COMMANDS
# ============================================

# Создать образ приложения
create:
	docker build -t $(IMAGE_NAME) .

# Удалить образ приложения
deli:
	docker rmi $(IMAGE_NAME)

# Запустить приложение с Traefik
runapp:
	docker run -d \
    --network $(NETWORK) \
    --restart unless-stopped \
    --env-file .env.docker \
    --name $(APP_CONTAINER) \
    --label "traefik.enable=true" \
    --label "traefik.http.routers.$(APP_CONTAINER).rule=Host(\`$(DOMAIN)\`)" \
    --label "traefik.http.routers.$(APP_CONTAINER).entrypoints=websecure" \
    --label "traefik.http.routers.$(APP_CONTAINER).tls.certresolver=letsencrypt" \
    --label "traefik.http.routers.$(APP_CONTAINER).service=$(APP_CONTAINER)-service" \
    --label "traefik.http.services.$(APP_CONTAINER)-service.loadbalancer.server.port=8000" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.rule=Host(\`$(DOMAIN)\`) && PathPrefix(\`/api\`)" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.entrypoints=websecure" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.tls.certresolver=letsencrypt" \
  	$(IMAGE_NAME)

# Запустить базу данных
rundb:
	docker run -d \
    --name $(DB_CONTAINER) \
    --network $(NETWORK) \
    --restart unless-stopped \
    --env-file .env.docker \
    --volume pg_ligadonbassa_data:/var/lib/postgresql/data \
    postgres:17


# Показать логи приложения
logs:
	docker logs $(APP_CONTAINER)

# Проверить текущую миграцию
current:
	docker exec $(APP_CONTAINER) alembic current

# Выполнить миграции
migrate:
	docker exec $(APP_CONTAINER) alembic upgrade head

# Удалить приложение
delapp:
	docker rm -f $(APP_CONTAINER)


# ============================================
# TRAEFIK COMMANDS
# ============================================

# Запустить Traefik
runtraefik:
	cd ~/traefik/ && docker compose -f docker-compose.yml up -d

# Остановить Traefik
stoptraefik:
	cd ~/traefik/ && docker compose -f docker-compose.yml down

# Перезапустить Traefik
restarttraefik: stoptraefik runtraefik

# Показать логи Traefik
logstraefik:
	docker logs traefik

# Проверить конфигурацию Traefik
checktraefik:
	curl -s http://localhost:8080/api/rawdata | jq . 2>/dev/null || echo "Traefik dashboard недоступен"

# ============================================
# UTILITY COMMANDS
# ============================================

# Проверить контейнеры
ps:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Проверить сеть
networks:
	docker network inspect $(NETWORK)

# Проверить SSL сертификат
checkssl:
	@echo "Проверка SSL для $(DOMAIN)..."
	@echo | openssl s_client -connect $(DOMAIN):443 -servername $(DOMAIN) 2>/dev/null | openssl x509 -noout -dates || echo "SSL не настроен"


# Показать help
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "=== Основные команды ==="
	@echo "make create        - Собрать образ приложения"
	@echo "make runapp        - Запустить приложение с Traefik"
	@echo "make rundb         - Запустить PostgreSQL"
	@echo "make runall        - Запустить всё"
	@echo ""
	@echo "=== Traefik ==="
	@echo "make runtraefik    - Запустить Traefik"
	@echo "make stoptraefik   - Остановить Traefik"
	@echo "make logstraefik   - Показать логи Traefik"
	@echo "make restarttraefik   - Перезапустить Traefik"
	@echo ""
	@echo "=== Утилиты ==="
	@echo "make ps            - Показать контейнеры"
	@echo "make logs          - Показать логи приложения"
	@echo "make migrate       - Выполнить миграции БД"
	@echo "make checkssl      - Проверить SSL сертификат"

