from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class InspectorDetails(db.Model):
    OrderID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)

@app.route('/get_inspector_details/<int:OrderID>', methods=['GET'])
def get_inspector_details(OrderID):
    try:
        inspector = InspectorDetails.query.filter_by(OrderID=OrderID).first()

        if inspector:
            inspector_info = {
                'OrderID': inspector.OrderID,
                'name': inspector.name,
                'contact_number': inspector.contact_number,
                'email': inspector.email
            }
            return jsonify(inspector_info), 200
        else:
            return jsonify({'error': 'Inspector details not found for order ID {}'.format(OrderID)}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/post_inspector_details', methods=['POST'])
def post_inspector_details():
    try:
        data = request.get_json()

        new_inspector = InspectorDetails(
            OrderID=data['OrderID'],
            name=data['name'],
            contact_number=data['contact_number'],
            email=data['email']
        )

        db.session.add(new_inspector)
        db.session.commit()

        return jsonify({'message': 'Inspector details added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        # Create tables within the context of the Flask application
        db.create_all()
    # Create tables before running the app
    # db.create_all()
    # app.run(debug=True)
    port = int(os.environ.get("PORT", 443))
    app.run(host='0.0.0.0', port=port, debug=True)
