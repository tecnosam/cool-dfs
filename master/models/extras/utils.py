import sqlalchemy.exc

from ... import db

from master.exceptions import *


def push_instance(instance):
    try:

        db.session.add(instance)
        db.session.commit()

        return instance
    except sqlalchemy.exc.IntegrityError as e:
        # raise e
        raise DuplicateKeyException()


def edit_instance(instance, kwargs: dict, preprocessors: dict):
    try:
        if instance is None:
            raise NoSuchInstance("The requested record was not found")

        for key in kwargs:
            if key in preprocessors:
                processor = preprocessors[key]
                val = kwargs[key]
                setattr(instance, key, processor(val))

        db.session.commit()
        return instance

    except sqlalchemy.exc.IntegrityError:
        raise DuplicateKeyException()
    except NoSuchInstance as e:
        raise e
    except Exception as e:
        raise e


def delete_instance(instance):
    try:

        if instance is None:
            raise NoSuchInstance("The requested record was not found")

        db.session.delete(instance)
        db.session.commit()

        return instance

    except sqlalchemy.exc.IntegrityError:
        raise DuplicateKeyException()

    except NoSuchInstance as e:
        raise e

    except Exception as e:
        raise e
