from main import db, Location
from app import app  # ensures Flask app context

locations = [
    {
        "name": "Town Hall",
        "address": "1 Main St, Woodbridge",
        "latitude": 40.5549,
        "longitude": -74.2761,
        "type": "HQ"
    },
    {
        "name": "Police Department",
        "address": "1 Main St, Woodbridge",
        "latitude": 40.5549,
        "longitude": -74.2761,
        "type": "HQ"
    },
    {
        "name": "HR",
        "address": "1 Main St, Woodbridge",
        "latitude": 40.5549,
        "longitude": -74.2761,
        "type": "HQ"
    },
    {
        "name": "Courts",
        "address": "1 Main St, Woodbridge",
        "latitude": 40.5549,
        "longitude": -74.2761,
        "type": "HQ"
    },
    {
        "name": "Club of Woodbridge",
        "address": "585 Main St, Woodbridge",
        "latitude": 40.5432,
        "longitude": -74.3014,
        "type": "community"
    },
    {
        "name": "Acacia Youth Center",
        "address": "95 Port Reading Ave, Woodbridge",
        "latitude": 40.5644,
        "longitude": -74.2690,
        "type": "community"
    },
    {
        "name": "Avenel Performing Arts Center",
        "address": "150 Avenel St, Avenel",
        "latitude": 40.5774,
        "longitude": -74.2762,
        "type": "community"
    },
    {
        "name": "Public Works",
        "address": "225 Smith St, Keasbey",
        "latitude": 40.5125,
        "longitude": -74.3031,
        "type": "community"
    },
    {
        "name": "Health and Human Services",
        "address": "2 George Frederick Plaza, Woodbridge",
        "latitude": 40.5683,
        "longitude": -74.2870,
        "type": "community"
    },
    {
        "name": "Barron Arts Center",
        "address": "582 Rahway Ave, Woodbridge",
        "latitude": 40.5611,
        "longitude": -74.2735,
        "type": "community"
    },
    {
        "name": "Sycamore Senior Center ",
        "address": "290 Old Rd, Sewaren",
        "latitude": 40.5629,
        "longitude": -74.2576,
        "type": "senior"
    },
    {
        "name": "Highland Grove Pool",
        "address": "70 Highland Terrance, Fords",
        "latitude": 40.5430,
        "longitude": -74.3143,
        "type": "pool"
    },
    {
        "name": "Woodbridge Community Center",
        "address": "600 Main St, Woodbridge",
        "latitude": 40.5467,
        "longitude": -74.3020,
        "type": "community"
    },
    {
        "name": "Woodbridge Mall",
        "address": "250 Woodbridge Center Dr, Woodbridge",
        "latitude": 40.5567,
        "longitude": -74.2990,
        "type": "community"
    },
    {
        "name": "Woodbridge Animal Group",
        "address": "195 Woodbridge Ave, Sewaren",
        "latitude": 40.5541,
        "longitude": -74.2655,
        "type": "community"
    },
    {
        "name": "Hickory Senior Center",
        "address": "17 Corrielle St, Fords",
        "latitude": 40.5295,
        "longitude": -74.3141,
        "type": "senior"
    },
    {
        "name": "Woodbridge Fire Department",
        "address": "418 School St, Woodbridge",
        "latitude": 40.5560,
        "longitude": -74.2802,
        "type": "fire"
    },
    {
        "name": "Fords Fire Department",
        "address": "667 King George Rd, Fords",
        "latitude": 40.5333,
        "longitude": -74.3070,
        "type": "fire"
    },
    {
        "name": "Woodbridge History Museum",
        "address": "86 Green St, Woodbridge",
        "latitude": 40.5590,
        "longitude": -74.2802,
        "type": "community"
    },
    {
        "name": "Marina/Tiki Bar",
        "address": "648 Cliff Rd, Sewaren",
        "latitude": 40.5572,
        "longitude": -74.2555,
        "type": "community"
    },
    {
        "name": "Hopelawn Fire Department",
        "address": "127 Loretta St, Hopelawn",
        "latitude": 40.5252,
        "longitude": -74.2953,
        "type": "fire"
    },

]

with app.app_context():
    for loc in locations:
        existing = Location.query.filter_by(name=loc["name"]).first()
        if not existing:
            new_location = Location(
                name=loc["name"],
                address=loc["address"],
                latitude=loc["latitude"],
                longitude=loc["longitude"],
                type=loc["type"]
            )
            db.session.add(new_location)
            print(f"Added: {loc['name']}")
        else:
            print(f"Already exists: {loc['name']}")
    db.session.commit()
    print("Seeding complete!")