## Express Frontend for Flask Backend

### Setup

```bash
cd devops/express_frontend
create .env
npm install
npm start
```

### Environment

- `PORT`: Express frontend port (default `3000`)
- `FLASK_SUBMIT_URL`: Flask endpoint URL for todo submission  
  Example: `http://127.0.0.1:5000/submittodoitem`

### Routes

- `GET /` -> renders form UI
- `POST /submit` -> sends form payload to Flask backend URL from env
