from datetime import datetime
from db_connection import events_table
from botocore.exceptions import ClientError
import uuid

sample_events = [{
    "_id": "event_id_001",
    "type": "Concert",
    "name": "Honkai Impact Music Fest 2024",
    "date": "15/12/2024 19:00:00",
    "location": "Singapore Indoor Stadium",
    "available_tickets": 12000,
    "reserved_tickets": 0,
    "sold_tickets": 0,
    "image_url": "static/images/concert_one.jpeg",
    "duration": "2 hours",
    "age_advisory": "PG-13",
    "description": "Experience the magical world of Honkai Impact through an orchestral performance featuring beloved tracks from the game.",
    "synopsis": "Join us for an unforgettable evening of music from Honkai Impact. The concert will feature a full orchestra performing iconic tracks from the game's soundtrack, accompanied by stunning visuals on the big screen. Please note that this event features actresses cosplaying game characters who may wear revealing costumes.",
    "artist": "HOYO-MiX Symphony Orchestra",
    "organizer": "HoYoverse Entertainment",
    "terms_conditions": [
        "No photography or video recording allowed during the performance",
        "Late entry will only be permitted during suitable breaks",
        "No refunds or exchanges permitted",
        "Parental guidance is advised due to cosplay performances featuring revealing costumes"
    ],
    "faq": [
        {
            "question": "Is there a dress code?",
            "answer": "Smart casual is recommended"
        },
        {
            "question": "Are cameras allowed?",
            "answer": "No photography or recording devices are permitted during the show"
        },
        {
            "question": "Will there be cosplayers at the event?",
            "answer": "Yes, professional actresses will be cosplaying game characters. Please note that some costumes may be revealing, as they stay true to the original character designs."
        }
    ],
    "highlights": [
        "Live orchestral performance",
        "HD screen projections", 
        "Exclusive merchandise",
        "Meet & greet opportunities with cosplaying performers"
    ]
},

{
    "_id": "event_id_002",
    "type": "Concert",
    "name": "Genshin Impact Music Fest 2024",
    "date": "2024-12-18T19:00:00Z",
    "location": "Singapore Indoor Stadium",
    "available_tickets": 12000,
    "reserved_tickets": 0,
    "sold_tickets": 0,
    "image_url": "static/images/concert_two.jpeg",
    "duration": "2 hours",
    "age_advisory": "General Audience",
    "description": "Immerse yourself in the enchanting world of Teyvat through a spectacular orchestral concert featuring the beloved music of Genshin Impact.",
    "synopsis": "Experience an extraordinary evening of music from Genshin Impact. The concert will showcase a full orchestra performing the game's most iconic melodies, complemented by stunning game footage and visual effects.",
    "artist": "HOYO-MiX Symphony Orchestra",
    "organizer": "HoYoverse Entertainment",
    "terms_conditions": [
        "No photography or video recording allowed during the performance",
        "Late entry will only be permitted during suitable breaks",
        "No refunds or exchanges permitted"
    ],
    "faq": [
        {
            "question": "Is there a dress code?",
            "answer": "Smart casual is recommended"
        },
        {
            "question": "Are cameras allowed?",
            "answer": "No photography or recording devices are permitted during the show"
        }
    ],
    "highlights": [
        "Live orchestral performance",
        "HD screen projections",
        "Exclusive merchandise",
        "Meet & greet opportunities"
    ]
},
{
    "_id": "event_id_003",
    "type": "Concert", 
    "name": "Honkai Star Rail Music Fest 2024",
    "date": "24/12/2024 19:00:00",
    "location": "Singapore Indoor Stadium",
    "available_tickets": 12000,
    "reserved_tickets": 0,
    "sold_tickets": 0,
    "image_url": "static/images/concert_three.jpeg",
    "duration": "2 hours",
    "age_advisory": "General Audience",
    "description": "Embark on a musical journey through the cosmos with the stellar soundtrack of Honkai: Star Rail performed live in concert.",
    "synopsis": "Join us for a stellar evening of music from Honkai: Star Rail. Experience the cosmic adventure through orchestral arrangements of the game's soundtrack, accompanied by spectacular visuals from your favorite moments.",
    "artist": "HOYO-MiX Symphony Orchestra",
    "organizer": "HoYoverse Entertainment",
    "terms_conditions": [
        "No photography or video recording allowed during the performance",
        "Late entry will only be permitted during suitable breaks",
        "No refunds or exchanges permitted"
    ],
    "faq": [
        {
            "question": "Is there a dress code?",
            "answer": "Smart casual is recommended"
        },
        {
            "question": "Are cameras allowed?",
            "answer": "No photography or recording devices are permitted during the show"
        }
    ],
    "highlights": [
        "Live orchestral performance",
        "HD screen projections",
        "Exclusive merchandise", 
        "Meet & greet opportunities"
    ]
}]

def create_events_onload():
    """Initialize sample events in DynamoDB"""
    try:
        # Check if events exist
        response = events_table.scan(Select='COUNT')
        if response['Count'] == 0:
            for event in sample_events:
                event_data = {
                    'event_id': event.pop('_id'),
                    'name': event['name'],
                    'date': event['date'],
                    'location': event['location'],
                    'available_tickets': event['available_tickets'],
                    'reserved_tickets': event['reserved_tickets'],
                    'sold_tickets': event['sold_tickets'],
                    'type': event['type'],
                    'image_url': event['image_url'],
                    'duration': event['duration'],
                    'age_advisory': event['age_advisory'],
                    'description': event['description'],
                    'synopsis': event['synopsis'],
                    'artist': event['artist'],
                    'organizer': event['organizer'],
                    'terms_conditions': event['terms_conditions'],
                    'faq': event['faq'],
                    'highlights': event['highlights']
                }
                events_table.put_item(Item=event_data)
            print("Sample events initialized")
        else:
            print("Events already exist")
    except ClientError as e:
        print(f"Error initializing events: {e}")

def retrieve_events():
    """Retrieve all events from DynamoDB"""
    try:
        response = events_table.scan()
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error retrieving events: {e}")
        return []

def get_event_by_id(event_id):
    """Get a single event by ID"""
    try:
        response = events_table.get_item(
            Key={'event_id': event_id}
        )
        return response.get('Item')
    except ClientError as e:
        print(f"Error retrieving event: {e}")
        return None

def reset_events():
    """Reset events in DynamoDB"""
    try:
        # Delete existing events
        response = events_table.scan(
            ProjectionExpression='event_id'
        )
        for item in response.get('Items', []):
            events_table.delete_item(
                Key={'event_id': item['event_id']}
            )

        # Insert sample events
        for event in sample_events:
            event_data = {
                'event_id': event['_id'],
                'name': event['name'],
                'date': event['date'],
                'location': event['location'],
                'available_tickets': event['available_tickets'],
                'reserved_tickets': event.get('reserved_tickets', 0),
                'sold_tickets': event.get('sold_tickets', 0),
                'type': event['type'],
                'image_url': event['image_url'],
                'duration': event['duration'],
                'age_advisory': event['age_advisory'],
                'description': event['description'],
                'synopsis': event['synopsis']
            }
            events_table.put_item(Item=event_data)
        
        return True
    except ClientError as e:
        print(f"Error resetting events: {e}")
        return False

def update_ticket_count(event_id, quantity, action="sold"):
    """Update ticket counts atomically"""
    try:
        update_expression = "SET available_tickets = available_tickets - :qty, sold_tickets = sold_tickets + :qty"
        condition_expression = "available_tickets >= :qty"
        
        if action == "refund":
            update_expression = "SET available_tickets = available_tickets + :qty, sold_tickets = sold_tickets - :qty"
            condition_expression = "sold_tickets >= :qty"

        response = events_table.update_item(
            Key={'event_id': event_id},
            UpdateExpression=update_expression,
            ConditionExpression=condition_expression,
            ExpressionAttributeValues={':qty': quantity},
            ReturnValues="UPDATED_NEW"
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print("Not enough tickets available")
            return False
        print(f"Error updating ticket count: {e}")
        return False

def check_ticket_availability(event_id, quantity):
    """Check if enough tickets are available"""
    try:
        event = get_event_by_id(event_id)
        if not event:
            return False
        return event.get('available_tickets', 0) >= quantity
    except Exception as e:
        print(f"Error checking ticket availability: {str(e)}")
        return False
