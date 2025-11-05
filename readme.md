---

## 🪷 `README.md`

```markdown
# 🌸 Orchid Cosmetics — Django Web App

Orchid Cosmetics is a Django web application.

---

## 📂 Project Structure

```

.
├── .github/
│   └── workflows/
│       └── tests.yml
├── src/
│   ├── manage.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── mywebapp/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   └── app/
│       ├── views.py
│       └── tests.py
├── .gitignore
├── .dockerignore
└── README.md

````

> 🗂️ All Django-related code lives inside the `src/` folder.

---

## ⚙️ 1. Setup for Local Development

### 1.1 Clone the repository

```bash
git clone https://github.com/yourusername/orchid.git
cd orchid/src
````

### 1.2 Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # On macOS/Linux
# OR
venv\Scripts\activate           # On Windows
```

### 1.3 Install dependencies

```bash
pip install -r requirements.txt
```

### 1.4 Apply migrations and run the server

```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 2. Running Tests

To run the included tests:

```bash
python manage.py test
```

GitHub Actions is configured to automatically run tests on every push and pull request.

---

## 🐋 3. Run with Docker

### 3.1 Build the Docker image

Make sure you’re in the `src/` directory (where the `Dockerfile` is):

```bash
docker build -t orchid .
```

### 3.2 Run the container

```bash
docker run -p 8000:8000 orchid
```

Then visit:
👉 [http://localhost:8000](http://localhost:8000)

---

## 🔧 4. Useful Commands

| Command                            | Description          |
| ---------------------------------- | -------------------- |
| `python manage.py runserver`       | Run local server     |
| `python manage.py test`            | Run tests            |
| `python manage.py createsuperuser` | Create admin user    |
| `docker build -t orchid .`         | Build Docker image   |
| `docker run -p 8000:8000 orchid`   | Run Docker container |

---

## 🧾 5. GitHub Actions

The workflow at `.github/workflows/tests.yml` automatically:

* Sets up Python
* Installs dependencies
* Runs Django tests

You can view test results in the **Actions** tab on GitHub.

---

## 💡 6. Notes

* The app uses **SQLite** by default (local file `db.sqlite3`).
* To use a different database (e.g. PostgreSQL), update `DATABASES` in `mywebapp/settings.py`.
* Make sure to keep your `.env` secrets or credentials out of version control.

---

## 🧰 7. Requirements

* Python 3.12+
* Docker (optional)
* Git

---
