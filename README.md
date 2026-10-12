# MongoDB Aggregation Pipeline UI

A small web tool for running **MongoDB aggregation pipelines** from the browser
and exploring the results. Type a pipeline as JSON, hit **Execute**, and view
the output as formatted JSON or as an interactive, collapsible tree.

Built with **React** (frontend) and **FastAPI + PyMongo** (backend).

## Features

- Run any aggregation pipeline (`$match`, `$project`, `$group`, `$sort`, …) against a collection
- Toggle between a plain JSON view and an interactive tree view (`react-json-tree`)
- MongoDB `ObjectId`s are converted to strings so results render cleanly
- Includes a loader script and 100 sample [openEHR](https://www.openehr.org/) documents to try it with

## Tech stack

| Layer | Tools |
|---|---|
| Frontend | React 18, Axios, react-json-tree, react-switch |
| Backend | Python, FastAPI, PyMongo, Uvicorn |
| Database | MongoDB |

## Getting started

### Prerequisites

- Node.js 18+
- Python 3.10+
- MongoDB running locally on `mongodb://localhost:27017`

### 1. Clone

```bash
git clone https://github.com/Kumarsujay03/mongodb-ui.git
cd mongodb-ui
```

### 2. Load the sample data (optional)

```bash
pip install pymongo fastapi uvicorn
python pythonscript.py
```

This inserts `100docs.json` into the `docs` database, `collection` collection.

### 3. Start the backend

```bash
python main.py
```

The API runs on `http://localhost:8000`.

### 4. Start the frontend

```bash
npm install
npm start
```

Open `http://localhost:3000`.

## Example pipelines

Count documents by category:

```json
[{ "$group": { "_id": "$versions.data.category.value", "count": { "$sum": 1 } } }]
```

Show only creation times, newest first:

```json
[
  { "$project": { "time_created": 1 } },
  { "$sort": { "time_created.value": -1 } },
  { "$limit": 10 }
]
```

## API

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/docs/` | Run a pipeline. Body: `{ "pipeline": [ ... ] }` |
| `POST` | `/aggregate/` | Same as `/docs/` |
| `GET` | `/test-pipeline/` | Runs a fixed sample `$project` pipeline |

## Project structure

```text
mongodb-ui/
├── main.py           # FastAPI backend (pipeline execution)
├── pythonscript.py   # Loads 100docs.json into MongoDB
├── 100docs.json      # Sample openEHR documents
├── src/App.js        # React UI
└── public/
```

## Notes

This is a local development tool. The API accepts arbitrary pipelines and
allows all CORS origins, so don't expose it to the internet as-is.
