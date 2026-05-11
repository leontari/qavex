from __future__ import annotations


def test_db_insert(db_session): ...


# Интеграционный тест БД с реальным template_app.core.database
# В tests/integration/test_db/test_db.py — чтобы убедиться, что DATABASE_URL читается из env и engine создаётся корректно.


# Интеграционный тест Alembic (опционально, но круто)
# Запуск alembic upgrade head в CI/Docker против тестовой БД.
