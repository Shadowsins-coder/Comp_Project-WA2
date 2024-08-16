from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)


DATABASE = 'python.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows for dict-like access to rows
    return conn

@app.route("/")
def home():
    return render_template("index.html")
  
@app.route('/login', methods=['POST'])
def login():
     email = request.form['email']
     password = request.form['password']
     # Handle login logic here, e.g., verify credentials

     # Redirect to home_page.html after successful login
     return redirect(url_for('home'))

@app.route('/')
def index():
  return render_template_string(open('login.html').read())

@app.route('/home')
def home_page():
  return render_template_string(open('home_page.html').read())

@app.route("/search", methods=["POST"])
def search_engine():
    program = request.form.get('programSelect')
    search_term = request.form.get('search', '').strip()

    data = []
    if program == "Python":
        conn = get_db_connection()
        try:
            if search_term:
                query = 'SELECT search_object, definition, image_source FROM Python_dictionary WHERE search_object LIKE ?'
                results = conn.execute(query, ('%' + search_term + '%',)).fetchall()
                data = [dict(row) for row in results]
            else:
                query = 'SELECT search_object, definition FROM Python_dictionary'
                results = conn.execute(query).fetchall()
                data = [dict(row) for row in results]
        except sqlite3.Error as e:
            print(f"SQL query error: {e}")
        finally:
            conn.close()

    return render_template("index.html", data=data, program=program, search_term=search_term)



@app.route("/recent-searches")
def recent_searches():
    conn = get_db_connection()
    recent_data = []  # Initialize recent_data here to ensure it's always defined
    try:
        query = 'SELECT search_query, timestamp FROM Recent_Searches ORDER BY timestamp DESC LIMIT 10'
        results = conn.execute(query).fetchall()
        recent_data = [dict(row) for row in results]
    except sqlite3.Error as e:
        print(f"SQL query error: {e}")
    finally:
        conn.close()

    return render_template("recent_searches.html", data=recent_data)





@app.route("/practice-code")
def practice_code():
    return render_template("practice_code.html")

if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=4905)