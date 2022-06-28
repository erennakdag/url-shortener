from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from typing import Optional
from csv import DictReader, DictWriter
from random import randrange

CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
FIELDNAMES = ['homeUrl', 'destination']
app = FastAPI()

@app.get('/', response_class=FileResponse)
def index():
    return 'index.html'

@app.get('/add_url')
def add_url(link: Optional[str] = None):
    if link:
        rand_chars = ''.join([CHARS[randrange(0, len(CHARS))] for _ in range(10)])
        with open('urls.csv', 'r') as f:
            reader = DictReader(f)
            for row in reader:
                if row['destination'] == link:
                    return f'Your short url is: http://127.0.0.1:8000/go_to?to={row["homeUrl"]}'
        with open('urls.csv', 'a') as f:
            writer = DictWriter(f, fieldnames=FIELDNAMES)
            resp = {
                    FIELDNAMES[0]: rand_chars,
                    FIELDNAMES[1]: link
                }
            writer.writerow(resp)
        return f'Your short url is: http://127.0.0.1:8000/go_to?to={rand_chars}'
    return {"test": "unseccessful"}

@app.get('/go_to', response_class=RedirectResponse)
def to_short_url(to: str):
    with open('urls.csv', 'r') as f:
        reader = DictReader(f)
        for row in reader:
            if row['homeUrl'] == to:
                return RedirectResponse(row['destination'])
