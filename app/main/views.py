import datetime
import os

from flask import render_template, request, session, redirect
# 导入蓝图程序-main，用于构建路由
from . import main
# 导入db 以及　models
from .. import db
from ..models import *


# 首页的访问路由
@main.route('/')
def index_views():
    categories = Category.query.all()
    # 查询所有的Topic信息
    topics = Topic.query.all()
    # 获取登录信息
    if "uid" in session and 'uname' in session:
        user = User.query.filter_by(id=session.get("uid")).first()

    return render_template('index.html', params=locals())


@main.route('/login', methods=["GET", "POST"])
def login_views():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # 接收前端的数据与数据库验证
        loginname = request.form.get("username")
        upwd = request.form.get('password')
        user = User.query.filter_by(loginname=loginname, upwd=upwd).first()
        # 如果用户存在的话,则将数据保存进session
        if user:
            # 登录成功
            session['uid'] = user.id
            session['uname'] = user.uname
            return redirect("/")
        else:
            # 登录失败
            errMsg = "用户名或密码不正确"
            return render_template("login.html", errMsg=errMsg)


@main.route('/logout')
def logout_views():
    # 获取源地址,有源地址的话返回到源地址,否则跳转至首页
    url = request.headers.get('referer', '/')
    print(url)
    # 判断登录信息是否在session中
    if 'uid' in session and 'uname' in session:
        del session['uid']
        del session['uname']
    return redirect(url)


@main.route('/release', methods=["GET", "POST"])
def release_views():
    if request.method == "GET":
        # 实现权限的验证
        # 判断用户是否是登录状态,否则重定向登录页
        if 'uid' in session and 'uname' in session:
            # 判断是否为作者
            user = User.query.filter_by(id=session.get('uid')).first()
            if user.is_author != 1:
                return redirect('/')
            else:
                blogTypes = BlogType.query.all()
                categories = Category.query.all()
                return render_template('release.html', params=locals())
        else:
            return redirect('/login')
    else:
        # 将发表的博客信息保存进数据库
        topic = Topic()
        # 为topic的各个属性赋值
        topic.title = request.form.get('author')
        topic.blogtype_id = request.form.get("list")
        topic.category_id = request.form.get("category")
        topic.user_id = session.get('uid')
        topic.content = request.form.get('content')
        topic.pub_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # 选择性为topic.images属性赋值
        if request.files:
            # 获取要上传的文件
            f = request.files['picture']
            # 处理文件名称,并赋值给topic.images
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            ext = f.filename.split('.')[1]
            filename = ftime + "." + ext
            topic.images = "upload/" + filename
            # 将文件保存至服务器
            basedir = os.path.dirname(os.path.dirname(__file__))
            upload_path = os.path.join(basedir, 'static/upload', filename)
            f.save(upload_path)
        db.session.add(topic)
        return redirect('/')


@main.route('/info')
def info_views():
    # 接收前端传递过来的id
    id = request.args.get('id')
    # 再根据id的值查询一个博客
    topic = Topic.query.filter_by(id=id).first()
    # 更新阅读量
    topic.read_num = int(topic.read_num) + 1
    db.session.add(topic)
    # 查找上一篇和下一篇
    # 上一篇：查找topic_id比当前topic_id值小的最后一条数据
    prevTopic = Topic.query.filter(Topic.id < id).order_by('id desc').first()
    # 下一篇：查找topic_id比当前topic_id值大的第一条数据
    nextTopic = Topic.query.filter(Topic.id > id).first()
    return render_template('info.html', params=locals())
