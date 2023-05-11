from fastapi import FastAPI, Response
from pydantic import ValidationError

from db.schemas import PerevalAdded
from middleware import pereval_to_db

app = FastAPI()


@app.get('/')
def index():
    return {'key': 'Starting sprint'}


@app.post('/submitData')
def submit_data(item: PerevalAdded, response: Response):
    pereval = PerevalAdded.parse_raw(item)
    try:
        pereval_id = pereval_to_db(pereval)
    except ValidationError:
        response.status_code = 400
        return {'message': 'Не все поля заполнены правильно', 'id': 'null'}
    else:
        if pereval_id == 'db_error':
            response.status_code = 500
            return {'message': 'Нет соединения с базой данных', 'id': 'null'}
        elif type(pereval_id) == int:
            response.status_code = 200
            return {'message': 'Отправлено успешно', 'id': pereval_id}
