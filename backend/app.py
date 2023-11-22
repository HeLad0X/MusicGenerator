from fastapi import FastAPI, Depends, Request, Form, status, File, Response
from starlette.responses import RedirectResponse, FileResponse
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')
from rnn_model.create_dataset import start_midi_file_download
from rnn_model.rnn import run_rnn
from rnn_model.preprocess import begin_preprocess

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


@app.post('/start_preprocessing')
async def preprocess_data(db:Session = Depends(get_db), project_id:str = Form(...)):
    
    try:
        begin_preprocess(int(project_id))
    except Exception as e:
        return {'error':f'{e}'}

    return None


@app.post('/run-rnn')
async def run_rnn_model(db:Session = Depends(get_db), project_id:str = Form(...)):
    run_rnn(project_id=int(project_id))