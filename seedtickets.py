from main import db, Ticket, Location
from app import app
from datetime import datetime

# Example tickets
sample_tickets = [
    {
        "issue": "Printer jammed in Town Hall",
        "description": "Main printer keeps jamming every 10 pages.",
        "assigned_to": "Sam",
        "assigned_by": "Dispatcher",
        "status": "open",
        "location_name": "Town Hall"
    },

]

with app.app_context():
    for t in sample_tickets:
        location = Location.query.filter_by(name=t["location_name"]).first()
        if location:
            new_ticket = Ticket(
                issue=t["issue"],
                description=t["description"],
                status=t["status"],
                assigned_to=t["assigned_to"],
                assigned_by=t["assigned_by"],
                location_id=location.id,
                date_created=datetime.utcnow()
            )
            db.session.add(new_ticket)
            print(f"Added: {t['issue']}")
        else:
            print(f"Location not found: {t['location_name']}")

    db.session.commit()
    print("Ticket seeding complete!")