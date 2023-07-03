from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.name} - {self.author} - {self.publisher}"

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()

    output = []
    for book in books:
        book_data = {'name': book.name, 'author': book.author, 'publisher':book.publisher}
        output.append(book_data)
    return {'books': output}

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return ({'name': book.name, 'author':book.author, 'publisher':book.publisher})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(
        id=data['id'],
        name=data['name'],
        author=data['author'],
        publisher=data['publisher']
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'id': book.id})

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {'error': 'not found'}
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)