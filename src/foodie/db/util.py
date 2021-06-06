import logging
from contextlib import contextmanager
from functools import wraps

from sqlalchemy import orm
from .base import SessionLocal


logger = logging.getLogger(__name__)


Session = orm.scoped_session(SessionLocal)


@contextmanager
def session_scope(bind=None):
    """
    Provide a transactional scope around a series of operations.
    Ensures that the session is commited and closed.
    Exceptions raised within the 'with' block using this contextmanager
    should be handled in the with block itself.
    They will not be caught by the 'except' here.
    """
    try:
        if bind:
            yield Session(bind=bind)
        else:
            yield Session()
        Session.commit()
    except Exception:
        # Only the exceptions raised by session.commit above are caught here
        Session.rollback()
        raise
    finally:
        Session.remove()


def with_db_session(func):
    """
    Wraps the function in a transaction, any errors thrown in the function
    are intercepted so the tx can be rolled back.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        with session_scope() as session:
            try:
                result = func(*args, **kwargs, session=session)
                session.commit()
                return result
            except Exception as exception:
                logger.exception(exception)
                session.rollback()
                raise

    return wrapped
