## Flask + MongoDB Atlas App

#### \*See Screenshots of the app in the ss folder

### Run

```bash
cd flask_mongo
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
export MONGO_URI="your_mongodb_atlas_connection_string"
export MONGO_DB_NAME="your_db_name"        # optional, default: test
export MONGO_COLLECTION="your_collection"  # optional, default: submissions
python app.py
```

### Routes

- `GET /api` -> returns JSON list from `backend/data.json`
- `GET /` -> form page
- `POST /` -> inserts into MongoDB Atlas, redirects to `/success` on success
- `GET /success` -> "Data submitted successfully"
- `GET /submissions` -> displays all submitted names and emails from MongoDB
