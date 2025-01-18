from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(200), nullable=False)
  date_created = db.Column(db.DateTime, default=datetime.now())

  def __repre__(self):
    return '<Task %r>' % self.id

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/hello')
def index():
  return 'Hello Flask!'

@app.route('/json')
def serve_json():
  data = {
    "message": "This is a JSON response " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": "success"
  }
  return jsonify(data)

if __name__ == '__main__':
  app.run(debug=True)