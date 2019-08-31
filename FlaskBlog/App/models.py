import datetime

from .exts import db


class Category(db.Model):

    __tablename__='category'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20))
    other_name=db.Column(db.String(30))
    father=db.Column(db.Integer)
    keyword = db.Column(db.String(100))
    info = db.Column(db.String(255))
    is_delete = db.Column(db.Boolean,default=True)
    article = db.relationship('Article', backref='category', lazy=True)



class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    info = db.Column(db.String(255))
    text = db.Column(db.String(20000))
    read_num = db.Column(db.Integer,default=0)
    praise_num = db.Column(db.Integer,default=0)
    label = db.Column(db.String(100))
    ispublic = db.Column(db.Boolean,default=True)
    categoryid = db.Column(db.Integer,db.ForeignKey(Category.id))
    date = db.Column(db.Date,default=datetime.datetime.now())
    comments = db.relationship('Comments', backref='comments', lazy=True)

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    toname =db.Column(db.String(20))
    info = db.Column(db.String(255))
    father = db.Column(db.Integer,default=0)    #共同的父亲节点
    # fatherid = db.Column(db.Integer, default=0)   #某个的父亲
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    articleid = db.Column(db.Integer, db.ForeignKey(Article.id))
