from flask import Flask, request, jsonify, session, redirect
from server.model import search_games, retrieve_game_by_id, retrieve_game_by_name, insert_game, delete_game
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

#### Pydantic models ####
class Game(BaseModel):
    id: int
    name: str
    document: str
    keywords: str
    cover: str
    rating: float
    websites: str

##### / ####
@app.route('/', method=['GET'])
def default():
    return redirect('/init')

@app.route('/init', method=['GET'])
def init():
    response = {
        "data" : "3 methods of search: search/by_name, search/by_id, search/by_similarity"
    }
    return jsonify(response)

##### /search ####
@app.route('/search', method=['GET'])
def search():
    response = {
        "data" : "3 methods of search: search/by_name, search/by_id, search/by_similarity"
    }
    return jsonify({ "data" : "3 methods of search: search/by_name, search/by_id, search/by_similarity" })

@app.route('/search/by_similarity', methods=['GET'])
def search():
    # Retrieve query parameters
    query = request.args.get('query')
    limit = request.args.get('limit')

    # Error handling
    if not query or not limit:
        return jsonify({"error": "Missing 'query' or 'limit' in query parameters"}), 400

    # Call the search function
    response = search_games(query, limit)
    return jsonify(response.dict())

@app.route('/search/by_name', method=['GET'])
def search():
    query = request.args.get('query')
    limit = request.args.get('limit')

    response = search_games(query, limit)
    return jsonify(response)

#### /add ####
@app.route('/insert', method=['POST'])
def insert():
    try:
        game = Game(**data)
        insert_game(game)
        return jsonify({ "data" : "Game inserted" }), 200
    except ValidationError as e:
        return jsonify({ "error" : e.errors() }), 400

#### /delete ####
@app.route('/delete', method=['POST'])
def delete():
    try:
        game_id = request.args.get('id')
        delete_game(game_id)
        return jsonify({ "data" : "Game deleted" }), 200
    except ValidationError as e:
        return jsonify({ "error" : e.errors() }), 400

#### game search ####
@app.route('/game_search', method=['GET'])
def game_search():
    """ 
    takes a list of game titles and searches for them in IGDB and returns the results.

    Args:
        games (list): A list of game titles to search for.
    Returns:
        list: A list of Game objects that match the search
    """
    pass

#### start here ####
if __name__ == "__main__":
    app.run(host='localhost', port=3000, debug=True)