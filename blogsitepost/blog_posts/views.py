from os import abort
from flask import render_template,url_for,flash,request,redirect,Blueprint
from flask_login import current_user,login_required
from blogsitepost import db
from blogsitepost.models import BlogPost
from blogsitepost.blog_posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts',__name__)

#create
@blog_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_posts=BlogPost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)

        db.session.add(blog_posts)
        db.session.commit()
        flash('Blog Post Created!!!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html',form=form)

#post view
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_posts = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',
                           title=blog_posts.title,
                           date=blog_posts.date,
                           post=blog_posts)

#update
@blog_posts.route('/<int:blog_post_id>/update',methods=['GET','POST'])
@login_required
def update(blog_post_id):
    blog_posts = BlogPost.query.get_or_404(blog_post_id)
    if blog_posts.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_posts.title = form.title.data
        blog_posts.text = form.text.data
        db.session.commit()
        flash('Blog Post Updated!!!')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=blog_post_id))

    elif request.method=='GET' :
        form.title.data=blog_posts.title
        form.text.data=blog_posts.text
    return render_template('create_post.html',title='Updating',form=form)

#delete
@blog_posts.route('/<int:blog_post_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(blog_post_id):
    blog_posts = BlogPost.query.get_or_404(blog_post_id)
    if blog_posts.author != current_user:
        abort(403)
    db.session.delete(blog_posts)
    db.session.commit()
    flash('Blog Post Deleted!!!')
    return redirect(url_for('core.index'))

