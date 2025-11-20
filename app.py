from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB = "database.db"

if not os.path.exists(DB):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def query_db(query, args=(), one=False):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return (rows[0] if rows else None) if one else rows

@app.route('/')
def index():
    posts = query_db("SELECT id, title FROM posts ORDER BY id DESC")
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = query_db("SELECT id, title, content FROM posts WHERE id = ?", [post_id], one=True)
    return render_template('view.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        query_db("INSERT INTO posts (title, content) VALUES (?, ?)", [title, content])
        return redirect('/')
    return render_template('create.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
