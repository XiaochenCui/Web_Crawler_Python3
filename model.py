import datetime

from mongoengine import *


def connect_mongodb():
    db = connect('movie')
    return db


def remove_data():
    db = connect_mongodb()
    db.drop_database('movie')


class Movie(Document):
    index = IntField(required=True, default=0, unique=True)
    name = StringField(max_length=300, required=True)
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
    url = URLField(required=True, unique=True)
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
        if not Url.objects(url=url_string):
            url = cls(url=url_string)
            url.save()


class BadUrl(Document):
    url = URLField(required=True, unique=True)
    init_date = DateTimeField(default=datetime.datetime.utcnow())
    update_date = DateTimeField(default=datetime.datetime.utcnow())
    meta = {
        'indexes': [
            'url'
        ]
    }

    @classmethod
    def add(cls, url):
        bad_url = cls.objects(url=url).first()
        if not bad_url:
            bad_url = cls(url=url)
            bad_url.save()


class UrlMap(Document):
    url = ReferenceField('Url',reverse_delete_rule=CASCADE)
    url_to = ListField(URLField())
    meta = {
        'indexes': [
            'url'
        ]
    }


class Proxy(Document):
    url = StringField(required=True, unique=True)
    position = StringField()
    speed = IntField()
    last_check = DateTimeField()
    init_date = DateTimeField(default=datetime.datetime.utcnow())
    update_date = DateTimeField(default=datetime.datetime.utcnow())

    def update(self):
        self.update_date = datetime.datetime.utcnow()
        self.save()

    @classmethod
    def add_url(cls, url_string):
        if not Proxy.objects(url=url_string):
            url = Url(url=url_string)
            url.save()
