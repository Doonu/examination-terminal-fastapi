#!/bin/bash

set -e

MODE=${1:-dev}

if [ "$MODE" = "prod" ]; then
  docker-compose -f docker-compose.prod.yml up -d db web || { echo "Ошибка при запуске базы данных"; exit 1; }

  echo "Применение миграций в продакшн-окружении..."

  current_revision=$(docker-compose -f docker-compose.prod.yml exec web alembic current | grep 'head' || true)

  if [ -z "$current_revision" ]; then
    echo "Применение миграций..."
  docker-compose -f docker-compose.prod.yml exec web alembic upgrade head || { echo "Ошибка при применении миграций"; exit 1; }
  else
    echo "Миграции не требуются, база данных на последней версии."
  fi

  docker-compose -f docker-compose.prod.yml up -d
else
  export ENV=dev
  export $(grep -v '^#' .env.dev | xargs)
  docker-compose up -d db || { echo "Ошибка при запуске базы данных"; exit 1; }

  current_revision=$(alembic current | grep 'head' || true)

  if [ -z "$current_revision" ]; then
    echo "Применение миграций..."
    alembic upgrade head || { echo "Ошибка при применении миграций"; exit 1; }
  else
    echo "Миграции не требуются, база данных на последней версии."
  fi

  cleanup() {
    echo "Остановка контейнеров..."
    docker-compose down db
  }

  trap cleanup EXIT

  uvicorn main:app --host localhost --port 8000 || { echo "Ошибка при запуске Uvicorn"; exit 1; }
fi
