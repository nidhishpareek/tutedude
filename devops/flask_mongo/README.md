## Flask + SQLite App

#### \*See Screenshots of the app in the ss folder

SQLite is embedded: no database server to run. The file is created on first start at `DB_PATH`.

### Run

```bash
cd flask_mongo
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
export DB_PATH="$PWD/data/app.db"   # optional, this is the default
python app.py
```

### Routes

- `GET /health` -> `{"status": "ok"}` (load balancer health check)
- `GET /api` -> returns JSON list from `backend/data.json`
- `GET /` -> form page
- `POST /` -> inserts into the `submissions` table, redirects to `/success` on success
- `GET /success` -> "Data submitted successfully"
- `GET /submissions` -> displays all submitted names and emails
- `GET /todo` -> To-Do form with Item Name and Item Description
- `POST /submittodoitem` -> inserts into the `todo_items` table (called by the Express frontend)
- `GET /todoitems` -> lists stored to-do items, newest first
