```bash
alembic init -t async migrations
alembic revision --autogenerate -m "message text"
alembic upgrade head
```

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```
