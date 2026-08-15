#!/bin/bash
python migrate.py || echo "Migración falló o tablas ya existen"
gunicorn app:app