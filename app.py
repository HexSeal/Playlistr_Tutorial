from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

# app.py

host = os.environ.get('MONGODB_URI', 'mongodb://host.docker.internal:27017/Contractor')
client = MongoClient(host=host)
db = client.get_default_database()
playlists = db.playlists
comments = db.comments


app = Flask(__name__)


@app.route('/')
def contractor_index():
    """Show all playlists"""
    return render_template('playlists_index.html', playlists = playlists.find()) 

@app.route('/playlists/new')
def playlists_new():
    """Create a new playlists."""
    return render_template('playlist_new.html')

@app.route('/playlists', methods=['POST'])
def playlists_submit():
    """Submit a new product."""
    product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'created_at': datetime.now()
    }
    print(product)
    product_id = playlists.insert_one(product).inserted_id
    return redirect(url_for('product_show', product_id=product_id))

@app.route('/playlists/<product_id>')
def playlists_show(product_id):
    """Show a single product."""
    product = playlists.find_one({'_id': ObjectId(product_id)})
    product_comments = comments.find({'product_id': ObjectId(product_id)})
    return render_template('playlists_show.html', product=product, comments=product_comments)

@app.route('/playlists/<product_id>/edit')
def playlists_edit(product_id):
    """Show the edit form for a product."""
    product = playlists.find_one({'_id': ObjectId(product_id)})
    return render_template('playlists_edit.html', product=product, title='Edit product')

@app.route('/playlists/<product_id>', methods=['POST'])
def playlists_update(product_id):
    """Submit an edited product."""
    updated_product = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'videos': request.form.get('videos').split()
    }
    playlists.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': updated_product})
    return redirect(url_for('playlists_show', product_id=product_id))

# app.py
...
@app.route('/playlists/<product_id>/delete', methods=['POST'])
def playlists_delete(product_id):
    """Delete one product."""
    playlists.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for('playlists_index'))

@app.route('/playlists/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'product_id': ObjectId(request.form.get('product_id'))
    }
    print(comment)
    return redirect(url_for('playlists_show', product_id=request.form.get('product_id')))

@app.route('/playlists/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('playlists_show', product_id=comment.get('product_id')))

if __name__ == '__main__':
  app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT', 5000))

