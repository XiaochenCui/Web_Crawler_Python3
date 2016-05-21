import datetime

from mongoengine import *


def connect_mongodb():
    connect('movie')


def remove_data():
    connect_mongodb()
    Movie.drop_collection()
    Url.drop_collection()


class Movie(Document):
    index = IntField(required=True, default=0)
    name = StringField(max_length=100, required=True)
    score_history = DictField()
    score = FloatField()
    release_date = DictField()
    release_year = IntField()
    producing_countries = ListField(StringField())
    starring = ListField(StringField())
    director = ListField(StringField())
    screenwriter = ListField(StringField())
    init_date = DateTimeField(default=datetime.datetime.utcnow())
    update_date = DateTimeField(default=datetime.datetime.utcnow())
    meta = {
        'indexes' : [
            'index'
        ]
    }

    def update(self):
        self.save()


class Url(Document):
    url = URLField(required=True)
    access = BooleanField(default=False)
    init_date = DateTimeField(default=datetime.datetime.utcnow())
    update_date = DateTimeField(default=datetime.datetime.utcnow())
    meta = {
        'indexes': [
            'url'
        ]
    }

    def update(self, access=False):
        self.update_date = datetime.datetime.utcnow()
        self.access = access
        self.save()

    @classmethod
    def add_url(cls, url_string):
        url = Url.objects(url=url_string).first()
        if not url:
            url = Url(url=url_string)
            url.save()
        else:
            url.update()

class UrlMap(Document):
    url = ReferenceField('Url',reverse_delete_rule=CASCADE)
    url_to = ListField(URLField())
    meta = {
        'indexes': [
            'url'
        ]
    }
