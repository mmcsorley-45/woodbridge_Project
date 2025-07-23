from flask import Flask, request, jsonify
from flask_cors import CORS
from main import db, Ticket, Location
from datetime import datetime
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)


# ------------------ ROUTES ------------------
@app.route('/')
def serve_index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static_file(path):
    return send_from_directory('frontend', path)

# GET /tickets - Return all tickets (optionally filtered by location)
@app.route('/tickets', methods=['GET'])
def get_tickets():
    location_name = request.args.get('location')
    if location_name:
        tickets = Ticket.query.join(Location).filter(Location.name == location_name).all()
    else:
        tickets = Ticket.query.all()

    return jsonify([serialize_ticket(t) for t in tickets])

# POST /tickets - Create a new ticket
@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    ticket = Ticket(
        issue=data['issue'],
        description=data['description'],
        status=data.get('status', 'open'),
        assigned_to=data.get('assigned_to'),
        assigned_by=data.get('assigned_by'),
        location_type=data['location_type']
    )
    db.session.add(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket created', 'ticket': serialize_ticket(ticket)}), 201

# PATCH /tickets/<id> - Update an existing ticket (status or assignment)
@app.route('/tickets/<int:ticket_id>', methods=['PATCH'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    data = request.json

    if 'status' in data:
        ticket.status = data['status']
        if data['status'] == 'closed':
            ticket.date_closed = datetime.utcnow()
    if 'assigned_to' in data:
        ticket.assigned_to = data['assigned_to']

    db.session.commit()
    return jsonify({'message': 'Ticket updated', 'ticket': serialize_ticket(ticket)})

# ------------------ HELPERS ------------------

# Helper function to convert Ticket object to dict
def serialize_ticket(ticket):
    return {
        'id': ticket.id,
        'issue': ticket.issue,
        'description': ticket.description,
        'status': ticket.status,
        'assigned_to': ticket.assigned_to,
        'assigned_by': ticket.assigned_by,
        'date_created': ticket.date_created.isoformat(),
        'date_closed': ticket.date_closed.isoformat() if ticket.date_closed else None,
        'location_id': ticket.location_id,
        'location_type': ticket.location.type,
        'location_name': ticket.location.name,
        'latitude': ticket.location.latitude,
        'longitude': ticket.location.longitude
    }
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{
        'id': loc.id,
        'name': loc.name,
        'type': loc.type,
        'latitude': loc.latitude,
        'longitude': loc.longitude
    } for loc in locations])
# ------------------ RUN APP ------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)