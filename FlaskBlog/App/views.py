import random

from flask import Blueprint, render_template, request, jsonify, url_for, redirect

from App.exts import cache
from .models import *
blog = Blueprint('blog',__name__)
admin = Blueprint('admin',__name__)

"""
开始admin博客管理页面

"""

# 管理首页
@admin.route('/admin/',methods=['GET','POST'])
def amdin_index():
    return render_template('admin/index.html')

#登陆界面，不检测
@admin.route('/login/')
def admin_login():
    return render_template('admin/login.html')


#查找父类标签有多少个子标签文章+自身个数
def father_num(cate,num):
    if cate.father=='0':
        ca_fas = Category.query.filter(Category.father>0)
        for ca_fa in ca_fas:
            if int(ca_fa.father) == cate.id:
                num +=len(Article.query.filter(Article.categoryid==ca_fa.id).all())
        return num
    else:
        return num

# 栏目管理get:获取页面或数据，post：对标签来说，存在则更新，不存在则添加，不重复
@admin.route('/category/',methods=['GET','POST'])
def amdin_category():
    if request.method == "GET":
        data=[]
        father_cates = Category.query.filter(Category.father==0).all()
        cates = Category.query.filter(Category.is_delete==True)
        for cate in cates:
            num = len(Article.query.filter(Article.categoryid==cate.id).all())
            num=father_num(cate,num)
            data.append({'cate':cate,'num':num})

        return render_template('admin/category.html',father_cates=father_cates,data=data)
    if request.method == "POST":
        name = request.form.get('name')
        alias = request.form.get('alias')
        fid = request.form.get('fid')
        keywords = request.form.get('keywords')
        describe = request.form.get('describe')
        try:
            fid = int(fid)
            cate=Category.query.filter(Category.name==name).first()
            flag = True
            if not cate:    #存在则更新，不存在则添加
                cate = Category()
                flag = False
            cate.name = name
            cate.other_name = alias
            cate.keyword = keywords
            cate.info = describe
            cate.father=0
            if not flag:
                db.session.add(cate)
            cate.father = fid
            db.session.commit()
            return redirect(url_for('admin.amdin_index'))
        except:
            db.session.rollback()
            db.session.flush()
            return redirect(url_for('admin.amdin_index'))


#标签更新页面显示：传入id，得到相关信息
@admin.route('/upcategory/<int:id>/')
def up_category(id):
    if request.method == "GET":
        cate = Category.query.get(id)
        fid = cate.father
        name = Category.query.get(fid)
        if not name:
            name={} #父节点被删除，找不到返回无
            name['id']=0
            name['name']='无'
        father_cates = Category.query.filter(Category.father == 0).all()
        return render_template('admin/update-category.html',cate=cate,father_cates=father_cates,name=name)

#删除标签请求，并重定向到首页，避免表单重复提交
@admin.route('/delcategory/<int:id>/')
def del_category(id):
    if request.method == "GET":
        cate = Category.query.get(id)
        cate.is_delete = False
        db.session.commit()

        return redirect(url_for('admin.amdin_index'))


# 文章管理：get：所有文章信息，标签名字，评论数量显示,     分页显示
#       post：一个id单个文章删除，多个id批量删除，为理解分开写
@admin.route('/article/<int:page>/',methods=['GET','POST'])
def amdin_article(page):
    if request.method =="GET":
        date = []

        articles = Article.query.paginate(page,3,False)

        for i in range(len(articles.items)):
            num = len(Comments.query.filter(Comments.articleid == articles.items[i].id).all())
            if articles.items[i].categoryid:
                name=Category.query.get(articles.items[i].categoryid).name
            else:
                name=' '
            date.append({'article':articles.items[i],'name':name,'num':num})
        # 评论数
        return render_template('admin/article.html',date=date,articles=articles)
    if request.method == "POST":

        id = request.form.getlist('id')
        if len(id)==1:
            for i in id:
                art = Article.query.get(int(i))
                db.session.delete(art)
                db.session.commit()
                return redirect(url_for('admin.amdin_article',page=1))  #单删除进入第一页
        else:
            for i in range(len(id)):
                art = Article.query.get(int(id[i]))
                db.session.delete(art)
                db.session.commit()
            return redirect(url_for('admin.amdin_index'))   #多删除进入首页



#文章的增加：get：渲染页面并给出标签选择信息，post:修改文章所有内容，并返回文章默认显示页面
@admin.route('/addarticle/',methods=['GET','POST'])
def amdin_addarticle():
    if request.method=='GET':
        cates = Category.query.filter()
        return render_template('admin/add-article.html',cates=cates)
    if request.method=="POST":
        title = request.form.get('title')
        content =request.form.get('content')
        describe =request.form.get('describe')
        category =request.form.get('category')
        tags =request.form.get('tags')
        artcle = Article()
        artcle.name = title
        artcle.text=content
        artcle.info=describe
        artcle.label=tags
        artcle.categoryid = category
        db.session.add(artcle)
        db.session.commit()
        return redirect(url_for('admin.amdin_article',page=1))


#修改文章内容：get:给定某篇文章的信息，post:修改文章信息，和添加类似分开区分
@admin.route('/uparticle/<int:id>/',methods=['GET','POST'])
def amdin_uparticle(id):
    if request.method == 'GET':
        article = Article.query.get(id)
        cates = Category.query.filter(Category.is_delete==True)
        return render_template('admin/update-article.html',article=article,cates=cates)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        describe = request.form.get('describe')
        category = request.form.get('category')
        tags = request.form.get('tags')
        artcle = Article.query.get(id)
        artcle.name = title
        artcle.text = content
        artcle.info = describe
        artcle.label = tags
        artcle.categoryid = category
        db.session.commit()
        return redirect(url_for('admin.amdin_article',page=1))

#公告，无功能
@admin.route('/notice/')
def admin_notice():
    return render_template('admin/notice.html')


#评论：get：数据渲染页面信息，显示所属文章，    分页显示
# post：删除评论，若父节点丢失，则第一个子节点替换
@admin.route('/comment/',methods=['GET','POST'])
def admin_comment():
    if request.method == 'GET':
        datas=[]
        id = request.args.get('id')
        if not id:
            id=0
        id = int(id)
        comms = Comments.query.paginate(id, 5, False)
        for i in range(len(comms.items)):
            if comms.items[i].articleid!=0:
                name = Article.query.get(comms.items[i].articleid).name
            else:
                name = '留言'
            datas.append({'comm': comms.items[i], 'name': name})
        return render_template('admin/comment.html',datas=datas,comms=comms)
    if request.method == 'POST':
        id = request.form.getlist('id')
        print(id)
        for i in id:
            i = int(i)
            comm = Comments.query.get(i)
            com = Comments.query.filter(Comments.father==comm.id).first()
            db.session.delete(comm)
            if com:
                com.father = 0 #子节点替换父节点
            db.session.commit()
        return redirect(url_for('admin.admin_comment'))


"""
开始前面显示
"""

#根路径：主动跳到/index/0/默认页面
@blog.route('/')
def home():
    return redirect(url_for('blog.index',id=0))


#index路径：主动跳到/index/0/默认页面,传默认参数0
@blog.route('/index/')
def blog_index():
    return redirect(url_for('blog.index',id=0))


#文章导航数据渲染函数，返回子节点个数和父节点包含所有子节点和自己的个数，
def artnav():
    data = []
    cates = Category.query.filter(Category.is_delete==True)
    for cate in cates:
        num = Article.query.filter(Article.categoryid == cate.id).all()
        num = len(num)
        num = father_num(cate, num)
        data.append({'cate': cate, 'num': num})
    return data


#文章显示，私密文章不显示，对于父标签也会显示子标签的文章
def art_show(id):
    art=[]
    if id==0:
        arts = Article.query.filter(Article.ispublic==True).all()
        art+=arts
    else:
        arts = Article.query.filter(Article.categoryid==id,Article.ispublic==True).all()
        art += arts
        cates = Category.query.filter(Category.father==id).all()
        for cate in cates:
            arts = Article.query.filter(Article.categoryid==cate.id,Article.ispublic==True).all()
            art += arts
    return art


#首页显示内容。函数调用,图片随机显示
@blog.route('/index/<int:id>/')
def index(id):
    data = artnav()
    arts = art_show(id)
    img=[]
    while True:
        a = random.randint(1,12)
        if a not in img:
            img.append(a)
        if len(img)==12:
            break
    return render_template('blog/index.html', data=data, arts=arts,img=img)


#评论增加函数，用户名随机生成，
def add_com(artval,fa_id,art_id,toname=None):
    com = Comments()
    com.info = artval
    com.name = random.randint(10000000, 99999999)
    com.father = fa_id
    com.toname = toname
    com.articleid = art_id
    db.session.add(com)
    db.session.commit()
    com = Comments.query.get(com.id)
    return com


#评论增加：首先确定，五分钟只能评论一次，节流，
# request.base_url+'addcomm'：作为标记，保证不和点赞，阅读数量冲突，用户少，cache简单存
#get:添加父评论，调用增加函数add_com
#post：添加子评论，调用增加函数add_com
@blog.route('/addcomment/',methods=['GET','POST'])
def addcomment():
    ip = request.base_url
    ip = ip + 'addcomm'
    data = datetime.datetime.now()
    if not cache.get(ip):
        cache.set(ip, data, timeout=60*5)
    else:
        return jsonify({'code': 0})

    if request.method == 'GET':
        artval = request.args.get('artval')
        art_id = request.args.get('art_id')
        com = add_com(artval, 0, art_id,)
        com = {
            'id': com.id,
            'info': com.info,
            'name': com.name,
            'date': com.date,
        }
        return jsonify({'com': com,'code':1})
    if request.method == 'POST':
        artval = request.form.get('artval')
        fa_id=request.form.get('userid')
        art_id=request.form.get('art_id')
        print(fa_id,artval,art_id)
        toname=Comments.query.get(fa_id).name
        com = add_com(artval,fa_id,art_id,toname)
        com={
            'id':com.id,
            'info':com.info,
            'name':com.name,
            'toname':com.toname,
            'fa_id':fa_id,
            'date':com.date,
        }
        return jsonify({'com':com,'code':1})


#某个文章评论数据获取函数，包含父评论和子评论
def comment(id):
    data = []
    fa_coms = Comments.query.filter(Comments.father==0,Comments.articleid==id)
    for fa_com in fa_coms:
        print('fa_com:',fa_com)
        son_com=Comments.query.filter(Comments.father==fa_com.id,Comments.articleid==id).order_by('date')
        print('fa_com.id----:', fa_com.id)
        print('son_com:',son_com)
        data.append({'fa_com': fa_com,'son_com':son_com})
    print(data)
    return data


#文章内容显示：get:渲染文章信息，评论信息，并且添加阅读数量一小时增加一次，分页，可点击获取上(下)一篇文章
#post：点赞返回数据，一天点赞一次
@blog.route('/info/<int:id>/',methods=['GET','POST'])
def info(id):
    if request.method =='GET':
        print(datetime.datetime.now())
        if id==0:
            art=Article.query.paginate(1,1,False)
        else:
            num = Article.query.filter(Article.id<=id,Article.ispublic==True).all()
            page = len(num)
            art = Article.query
            art = art.filter(Article.ispublic==True)
            art=art.paginate(page,1,False)
        ip = request.base_url
        data = datetime.datetime.now()
        artid = Article.query.get(art.items[0].id)
        if not cache.get(ip):
            cache.set(ip, data, timeout=60*60)
            artid.read_num +=1
            db.session.commit()
        cate_name = Category.query.get(artid.categoryid).name
        data = artnav()
        comms = comment(artid.id)
        return render_template('blog/info.html', data=data,art=art,cate_name=cate_name,comms=comms)
    elif request.method == "POST":
        ip = request.base_url
        ip=ip+'praise'
        data = datetime.datetime.now()
        artid = Article.query.get(id)
        if not cache.get(ip):
            cache.set(ip, data, timeout=60*60*24)
            artid.praise_num += 1
            db.session.commit()

        print(artid.praise_num)
        return jsonify({'pra_num':artid.praise_num})


@blog.route('/share/')
def share():
    return render_template('blog/share.html')
@blog.route('/list/<int:id>/')
def list(id):
    data = artnav()
    arts = art_show(id)
    return render_template('blog/list.html', data=data,arts=arts)
@blog.route('/about/')
def about():
    data = artnav()
    return render_template('blog/about.html', data=data)
@blog.route('/gbook/')
def gbook():
    data = artnav()
    return render_template('blog/gbook.html', data=data)
@blog.route('/infopic/')
def infopic():
    data = artnav()
    return render_template('blog/infopic.html', data=data)

