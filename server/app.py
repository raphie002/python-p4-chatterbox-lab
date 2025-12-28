# server/app.py
from flask import Flask, request, make_response, jsonify
from flask_cors import CORS # type: ignore
from flask_migrate import Migrate # type: ignore
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Requirement: ordered by created_at in ascending order
        all_messages = Message.query.order_by(Message.created_at.asc()).all()
        return make_response([m.to_dict() for m in all_messages], 200)

    elif request.method == 'POST':
        data = request.get_json()
        new_msg = Message(
            body=data.get('body'),
            username=data.get('username')
        )
        db.session.add(new_msg)
        db.session.commit()
        return make_response(new_msg.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg = Message.query.filter_by(id=id).first()
    
    if not msg:
        return make_response({"error": "Message not found"}, 404)

    if request.method == 'PATCH':
        data = request.get_json()
        # Requirement: update the body
        if 'body' in data:
            msg.body = data['body']
        db.session.commit()
        return make_response(msg.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(msg)
        db.session.commit()
        return make_response({}, 204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)