from sqlalchemy.exc import DatabaseError

from db.database import SessionLocal as db
from db.models import Users, Coords, Levels, Images, PerevalAdded


def pereval_to_db(item):
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

    try:
        db.add(pereval, user, coords, levels, images)
        db.commit()
    except DatabaseError:
        return 'db_error'
    else:
        return pereval.id
