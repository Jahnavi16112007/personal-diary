# app.py - Flask backend for Personal Diary Website
from flask import Flask, render_template, request, redirect, url_for, session, flash, g
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['DATABASE'] = str(Path(app.root_path) / 'diary.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            mood TEXT DEFAULT 'neutral',
            is_favorite INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    db.commit()


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        init_db()  # Ensure tables exist
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        init_db()  # Ensure tables exist
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()

        if existing:
            flash('Username already exists')
        else:
            hashed_password = generate_password_hash(password)
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            db.commit()
            flash('Registration successful. Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', 'All').strip()
    show_favorites = request.args.get('favorites', False)

    query = 'SELECT id, content, category, is_favorite, created_at, updated_at FROM entries WHERE user_id = ?'
    params = [session['user_id']]

    if search_query:
        query += ' AND content LIKE ?'
        params.append(f'%{search_query}%')

    if category_filter != 'All':
        query += ' AND category = ?'
        params.append(category_filter)

    if show_favorites:
        query += ' AND is_favorite = 1'

    query += ' ORDER BY created_at DESC'

    entries = db.execute(query, params).fetchall()

    # Get all categories for filter dropdown
    categories = db.execute(
        'SELECT DISTINCT category FROM entries WHERE user_id = ? ORDER BY category',
        (session['user_id'],)
    ).fetchall()

    return render_template('dashboard.html', entries=entries, categories=categories, search_query=search_query, category_filter=category_filter)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    entry = request.form['entry'].strip()
    category = request.form.get('category', 'General').strip()
    mood = request.form.get('mood', 'neutral').strip()
    if entry:
        db = get_db()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            'INSERT INTO entries (user_id, content, category, mood, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
            (session['user_id'], entry, category, mood, now, now)
        )
        db.commit()

    return redirect(url_for('dashboard'))


@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    entry = db.execute('SELECT * FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id'])).fetchone()

    if not entry:
        flash('Entry not found')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        content = request.form['entry'].strip()
        category = request.form.get('category', 'General').strip()
        mood = request.form.get('mood', 'neutral').strip()
        if content:
            updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute(
                'UPDATE entries SET content = ?, category = ?, mood = ?, updated_at = ? WHERE id = ?',
                (content, category, mood, updated_at, entry_id)
            )
            db.commit()
            flash('Entry updated successfully')
            return redirect(url_for('dashboard'))

    return render_template('edit_entry.html', entry=entry)


@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    entry = db.execute('SELECT id FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id'])).fetchone()

    if entry:
        db.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
        db.commit()
        flash('Entry deleted successfully')

    return redirect(url_for('dashboard'))


@app.route('/toggle_favorite/<int:entry_id>', methods=['POST'])
def toggle_favorite(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    entry = db.execute('SELECT is_favorite FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id'])).fetchone()

    if entry:
        new_favorite_status = 1 - entry['is_favorite']
        db.execute('UPDATE entries SET is_favorite = ? WHERE id = ?', (new_favorite_status, entry_id))
        db.commit()

    return redirect(url_for('dashboard'))


@app.route('/view_entry/<int:entry_id>')
def view_entry(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    entry = db.execute('SELECT * FROM entries WHERE id = ? AND user_id = ?', (entry_id, session['user_id'])).fetchone()

    if not entry:
        flash('Entry not found')
        return redirect(url_for('dashboard'))

    word_count = len(entry['content'].split())
    char_count = len(entry['content'])

    return render_template('view_entry.html', entry=entry, word_count=word_count, char_count=char_count)


@app.route('/stats')
def stats():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()

    # Total entries
    total_entries = db.execute('SELECT COUNT(*) as count FROM entries WHERE user_id = ?', (session['user_id'],)).fetchone()['count']

    # Entries by category
    categories = db.execute('SELECT category, COUNT(*) as count FROM entries WHERE user_id = ? GROUP BY category', (session['user_id'],)).fetchall()

    # Entries by mood
    moods = db.execute('SELECT mood, COUNT(*) as count FROM entries WHERE user_id = ? GROUP BY mood', (session['user_id'],)).fetchall()

    # Total words and characters
    entries = db.execute('SELECT content FROM entries WHERE user_id = ?', (session['user_id'],)).fetchall()
    total_words = sum(len(entry['content'].split()) for entry in entries)
    total_chars = sum(len(entry['content']) for entry in entries)

    # Favorite entries
    favorites = db.execute('SELECT COUNT(*) as count FROM entries WHERE user_id = ? AND is_favorite = 1', (session['user_id'],)).fetchone()['count']

    return render_template('stats.html', 
        total_entries=total_entries,
        categories=categories,
        moods=moods,
        total_words=total_words,
        total_chars=total_chars,
        favorites=favorites
    )


@app.route('/monthly')
def monthly():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db = get_db()
    entries = db.execute('SELECT id, content, category, mood, is_favorite, created_at FROM entries WHERE user_id = ? ORDER BY created_at DESC', (session['user_id'],)).fetchall()

    # Group by month
    from collections import defaultdict
    months = defaultdict(list)
    for entry in entries:
        month = entry['created_at'][:7]  # YYYY-MM
        months[month].append(entry)

    return render_template('monthly.html', months=sorted(months.items(), reverse=True))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)