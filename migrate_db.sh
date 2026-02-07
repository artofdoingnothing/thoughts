#!/bin/bash
pip install alembic sqlalchemy psycopg2-binary
export PYTHONPATH=$PYTHONPATH:$(pwd)
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
