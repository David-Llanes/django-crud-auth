#!/usr/bin/env bash
# exit on error
set -o errexit

# No tenemos que ejecutar estos comandos ya que Render se encargará de hacerlo.
# poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate