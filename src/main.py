import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def resolve_root():
    return f"Host: {os.environ.get('HOSTNAME')}"

@app.get("/foo")
def resolve_foo():
    return f"Host: {os.environ.get('HOSTNAME')} FOO"

@app.get("/bar")
def resolve_bar():
    return f"Host: {os.environ.get('HOSTNAME')} BAR"
