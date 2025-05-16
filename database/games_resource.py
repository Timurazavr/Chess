from flask import jsonify
from flask_restful import abort, Resource
from .db_session import create_session
from .games import Game


def abort_if_game_not_found(game_id):
    session = create_session()
    user = session.get(Game, game_id)
    if not user:
        abort(404, message=f"User {game_id} not found")


class GamesResource(Resource):
    def get(self, game_id):
        abort_if_game_not_found(game_id)
        session = create_session()
        game = session.get(Game, game_id)
        return jsonify({"game": {"id": game.id, "fen": eval(game.board)[-1]}})


class GamesListResource(Resource):
    def get(self):
        session = create_session()
        games = session.query(Game).all()
        return jsonify(
            {"games": [{"id": item.id, "fen": eval(item.board)[-1]} for item in games]}
        )
