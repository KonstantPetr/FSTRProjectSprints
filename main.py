from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def index():
    return {'key': 'Starting sprint'}


@app.get('/submitData')
def submit_data():
    return {'key': 'Starting sprint'}
