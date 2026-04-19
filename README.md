# Song Recommender

A retro-styled music recommendation app powered by Last.fm.
Pick a genre and get a random top track recommendation.

## Setup

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Get a free Last.fm API key:
   - Go to https://www.last.fm/api/account/create
   - Fill in the form (App name: anything, e.g. "MySongApp")
   - Copy the **API key** and paste it into your `.env` file

## Run

```
python main.py
```

Then open: **http://127.0.0.1:5000**

## Test

```
python -m pytest tests/
```
