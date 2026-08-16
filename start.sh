#!/bin/bash
pip install -r requirements.txt
python migrate.py || echo "Migración falló o tablas ya existen"
gunicorn app:app