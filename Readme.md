# Setup

## PIP
`pip install -r requirements.txt`

## DB

`docker compose up --build -d`
Ensure the DB is spun-up after this cmd.

## ENV config

copy `.env.example` to `.env` and fill in the details

## Server

Either: `fastapi dev main.py`, or a **FastAPI** config in the IDE

# Sources

## DB

The db is filled manually, do this before running the server

## Docs

Place all relevant docs in `/docs`

## Web

The URL to query is contained in `.env`

# Navigation

The homepage provides links to all three services <br><br>

You can query either: `DB, Docs or Web`