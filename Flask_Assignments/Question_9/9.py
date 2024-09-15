from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database
books = []

# Route to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

# Route to get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    return jsonify({'book': book})

# Route to create a new book
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({'message': 'Bad request'}), 400
    
    new_book = {
        'id': len(books) + 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify({'book': new_book}), 201

# Route to update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    if not request.json:
        return jsonify({'message': 'Bad request'}), 400

    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    return jsonify({'book': book})

# Route to delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({'message': 'Book deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)
