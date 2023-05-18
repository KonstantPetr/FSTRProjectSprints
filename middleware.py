from sqlalchemy.exc import DatabaseError, InvalidRequestError

from db.database import SessionLocal as db
from db.models import Users, Coords, Levels, Images, PerevalAdded, PerevalImage


def identify_parameters(item):
    pereval = PerevalAdded(
        beauty_title=item.beauty_title,
        title=item.title,
        other_titles=item.other_titles,
        connect=item.connect,
        status=item.status
    )
    user = Users(
        email=item.created_by[0].email,
        phone=item.created_by[0].phone,
        fam=item.created_by[0].fam,
        name=item.created_by[0].name,
        otc=item.created_by[0].otc
    )
    coords = Coords(
        latitude=item.coord_id[0].latitude,
        longitude=item.coord_id[0].longitude,
        height=item.coord_id[0].height
    )
    levels = Levels(
        winter=item.levels_id[0].winter,
        summer=item.levels_id[0].summer,
        autumn=item.levels_id[0].autumn,
        spring=item.levels_id[0].spring
    )
    images = Images(
        title=item.image_id[0].title,
        image=item.image_id[0].image
    )
    return [pereval, user, coords, levels, images]


def pereval_to_db(item):
    item_parameters = identify_parameters(item)
    try:
        for parameter in item_parameters:
            db.add(parameter)
        db.commit()
    except DatabaseError:
        return 'db_error'
    else:
        return item_parameters[0]


def get_single_pereval(item_id):
    try:
        pereval = db.query(PerevalAdded).filter(PerevalAdded.id == item_id).all()
    except DatabaseError:
        return 'db_error'
    except InvalidRequestError:
        return 'invalid_id'
    else:
        return pereval


def patch_single_pereval(item, item_id):
    item_parameters = identify_parameters(item)
    pereval = db.find_by_id(item_id)
    if item:
        if pereval.status != 'new':
            return 'not_new'
        user = db.query(Users).filter(Users.id == pereval.created_by).all()
        item_parameters[1].email = user.email
        item_parameters[1].phone = user.phone
        item_parameters[1].fam = user.fam
        try:
            pereval_image = db.query(PerevalImage).filter(PerevalImage.pereval_id == pereval.id).all()
            coords = db.query(Coords).filter(Coords.id == pereval.coord_id).all()
            levels = db.query(Levels).filter(Levels.id == pereval.levels_id).all()
            images = db.query(Images).filter(Images.id == pereval_image.image_id).all()
            db.update(item_parameters[0], pereval.id)
            db.update(item_parameters[1], user.id)
            db.update(item_parameters[2], coords.id)
            db.update(item_parameters[3], levels.id)
            db.update(item_parameters[4], images.id)
            db.commit()
        except DatabaseError:
            return 'db_error'
        else:
            return 'ok'
    else:
        return 'invalid_id'


def get_pereval_by_email(email):
    try:
        perevals = db.query(PerevalAdded).filter(PerevalAdded.created_by.email == email).all()
    except DatabaseError:
        return 'db_error'
    except InvalidRequestError:
        return 'invalid_email'
    else:
        return perevals
