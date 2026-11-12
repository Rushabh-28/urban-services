# 🏙️ Urban Services

A web app where customers can find and book home services (AC repair, salon, spa and more), and service providers can list and manage the services they offer.

Built with **Django**, **Bootstrap** and **PostgreSQL / SQLite**.

## 👀 Live demo (no install needed)

Static preview of the main pages, hosted on GitHub Pages:

**https://YOUR-USERNAME.github.io/urban-services/**

Pages in the preview: Home · About Us · Contact · Terms · Payment · Thank-you.
Login, registration and booking need the full Django app (see "Run locally" below).

> You can also open any file inside the [`docs/`](docs/) folder to see the HTML.

## ✨ Features

- Customer and service-provider registration and login
- Customer dashboard and home page listing available services
- Service providers can add, edit, view and delete their services
- Booking flow with invoice and PDF download
- Welcome email on registration
- Django admin panel for managing categories, services and users

## 🧰 Tech stack

| Area | Tools |
|------|-------|
| Backend | Python, Django 5 |
| Database | SQLite (default) or PostgreSQL |
| Frontend | HTML, CSS, Bootstrap, Argon Dashboard theme |
| Other | django-crispy-forms, Pillow, ReportLab (PDF invoices) |

## 🚀 Run locally

```bash
git clone https://github.com/YOUR-USERNAME/urban-services.git
cd urban-services

python -m venv venv
venv\Scripts\activate            # Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/user/home/ (admin panel: `/admin/`).

### Optional settings

Copy `env.example` and set the values as environment variables. Without them the app uses SQLite and prints emails to the console, so no setup is required.

To use PostgreSQL set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

## 📁 Project structure

```
urban-services/
├── us/          # project settings and main urls
├── user/        # accounts, items, bookings, invoices
├── service/     # service categories and listings
├── templates/   # Django HTML templates
├── static/      # CSS, images, JS
├── docs/        # static HTML demo for GitHub Pages
└── tools/build_demo.py   # regenerates docs/ from the templates
```

## 🌐 Updating the live demo

After changing a template, regenerate the static pages and push:

```bash
python tools/build_demo.py
git add docs
git commit -m "Update demo"
git push
```

## 📄 License

Free to use for learning. Add a LICENSE file if you want to set specific terms.
