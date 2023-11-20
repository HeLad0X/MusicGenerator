from fastapi import FastAPI, Depends, Request, Form, status, File, Response
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')
from rnn_model.create_dataset import start_midi_file_download
from rnn_model.rnn import run_rnn

from sqlalchemy.orm import Session

import model
from database import SessionLocal, engine
import os

model.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get('/')
async def home(request: Request, db:Session = Depends(get_db)):
    return {'hello':'world'}


@app.get('/download-data')
async def download_midi_data(request: Request, db:Session = Depends(get_db)):
    start_midi_file_download()

@app.post('/upload-files')
async def download_midi_data():
    return {'hello':'world'}

@app.get('/run-rnn')
async def run_rnn_model():
    file = run_rnn()
    if os.path.exists(file):
        print('Exists')
        return FileResponse(file,media_type="application/octet-stream",filename='res.mid')
    else :
        print('Doesn"t exist')
        return {'file:':'No file found'}