"""
.. module:: models
    :synopsis: Database ORM
"""

from google.appengine.ext import db


class Track(db.Model):
    """Model for individual musician with his melody"""
    author = db.UserProperty()
    name = db.StringProperty()
    music_string = db.StringProperty()
    music_filename = db.StringProperty()


def user_key(user_name='default_themes'):
    """Constructs a datastore key for a Results entity with user_name."""
    return db.Key.from_path('Track', user_name)
