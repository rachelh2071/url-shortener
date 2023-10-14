from flask import Flask, request, jsonify, redirect, render_template
import random
import string
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('urls.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS url_map (id INTEGER PRIMARY KEY, long_url TEXT, short_url TEXT)')
conn.commit()
conn.close()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.json.get('longUrl')

    # Check if the URL is valid
    if not long_url.startswith(('http://', 'https://')):
        return jsonify({"error": "Invalid URL"}), 400

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    # Check if the URL already exists in the database
    cursor.execute('SELECT short_url FROM url_map WHERE long_url = ?', (long_url,))
    result = cursor.fetchone()

    if result:
        short_url = result[0]
    else:
        while True:
            short_url = generate_short_url()
            cursor.execute('SELECT id FROM url_map WHERE short_url = ?', (short_url,))
            if cursor.fetchone() is None:
                break

        cursor.execute('INSERT INTO url_map (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
        conn.commit()

    conn.close()
    return jsonify({"shortUrl": f"/r/{short_url}"})

@app.route('/r/<short_url>')
def redirect_to_original(short_url):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM url_map WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        return jsonify({"error": "URL not found"}, 404)

@app.route('/list')
def list_urls():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url, short_url FROM url_map')
    urls = cursor.fetchall()
    conn.close()

    url_list = [{"longUrl": url[0], "shortUrl": url[1]} for url in urls]
    return jsonify(url_list)

if __name__ == '__main__':
    app.run(debug=True)
