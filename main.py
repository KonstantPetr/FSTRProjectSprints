from fastapi import FastAPI, Response, Query
from pydantic import ValidationError

from db.schemas import PerevalAdded
from middleware import pereval_to_db, get_single_pereval, patch_single_pereval

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


@app.get('/submitData/{item_id}')
def get_item(item_id: int, response: Response):
    pereval = get_single_pereval(item_id)
    if pereval == 'db_error':
        response.status_code = 500
        return {'message': 'Нет соединения с базой данных', 'id': 'null'}
    elif pereval == 'invalid_id':
        response.status_code = 404
        return {'message': 'В базе данных нет такой записи', 'id': item_id}
    else:
        response.status_code = 200
        return pereval


@app.patch('/submitData/{item_id}')
def patch_item(item: PerevalAdded, item_id: int, response: Response):
    pereval = PerevalAdded.parse_raw(item)
    state = {'db_error': [0, 'Нет соединения с базой данных'],
             'invalid_id': [0, 'В базе данных нет такой записи'],
             'not_new': [0, 'Статус записи не "новая"'],
             'ok': [1, 'Запись успешно отредактирована']}
    try:
        patching = patch_single_pereval(pereval, item_id)
    except ValidationError:
        response.status_code = 0
        return {'message': 'Не все поля заполнены правильно'}
    else:
        code = state[patching][0]
        msg = state[patching][1]
        response.status_code = code
        return {'message': msg}


@app.get('/submitData/?user__email={email}')
def get_items_by_email(email: str, response: Response):
    ...
