from flask import render_template, request, flash, redirect, url_for
# LoginManager用于实例化flask_login  login_user用于更新登录状态
# login_required是装饰器 logout_user登出
from flask_login import login_user, login_required, logout_user, current_user

from watchList import app, db
from watchList.models import User, Movie


@app.route('/', methods=["POST", "GET"])
def index():
    # 函数名字必须是与base_url的参数一样
    if request.method == "POST":
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('index'))  # 重定向到主页
        # 和内容input的name对应
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        new_movie = Movie(title=title, year=year)
        db.session.add(new_movie)
        db.session.commit()
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()
    return render_template("index.html", movies=movies)
@app.route("/movie/edie<int:movie_id>", methods=["POST", "GET"])
@login_required  # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template("edit.html", movie=movie)

@app.route("/movie/delete/<int:movie_id>", methods=["POST"])
@login_required  # 登录保护
def delete(movie_id):
    movie_to_del = Movie.query.get(movie_id)
    db.session.delete(movie_to_del)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页

        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面

    return render_template('login.html')

@app.route('/logout')
@login_required  # 用于视图保护，后面会详细介绍
def logout():
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404
