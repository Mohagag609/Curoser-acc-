acc_modern — Django 5 + HTMX + Tailwind v4 (RTL)

Quickstart (local):

1) Python venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -U pip
   pip install -r requirements.txt

2) Env
   cp .env.example .env

3) DB
   python manage.py migrate
   python manage.py createsuperuser

4) Tailwind (watch)
   npm install
   npm run dev

5) Run
   python manage.py runserver 0.0.0.0:8000

Render deploy (notes):
- Set env: DEBUG=False, SECRET_KEY, DATABASE_URL=postgres://…
- Add build: pip install -r requirements.txt && python manage.py collectstatic --noinput
- Start command: gunicorn acc_modern.wsgi:application
