from datetime import datetime
from db_connection import seats_table, events_table
from botocore.exceptions import ClientError
import uuid

# Predefined seat sections with their configurations
seat_sections = [
    {"section": "333", "price": 200, "color": "Periwinkle Blue", "color_code": "#9391f7", "capacity_limit": 200},
    {"section": "332", "price": 200, "color": "Periwinkle Blue", "color_code": "#9391f7", "capacity_limit": 200},
    {"section": "309", "price": 200, "color": "Periwinkle Blue", "color_code": "#9391f7", "capacity_limit": 200},

    {"section": "331", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "330", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "329", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "328", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "327", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "326", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "325", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "324", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "323", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "322", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "320", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "319", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "318", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "314", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "313", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "312", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "311", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},
    {"section": "310", "price": 300, "color": "Lavender Blue", "color_code": "#c9c7fb", "capacity_limit": 100},

    {"section": "233", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 100},
    {"section": "232", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 100},
    {"section": "230", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 100},
    {"section": "229", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 100},
    {"section": "213", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 100},
    {"section": "212", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 150},
    {"section": "209", "price": 300, "color": "Sour Candy", "color_code": "#5bb343", "capacity_limit": 150},
    
    {"section": "231", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "210", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "211", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "114", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "219", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "223", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    {"section": "128", "price": 300, "color": "Green Gooseberry", "color_code": "#add9a1", "capacity_limit": 150},
    
    {"section": "133", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "132", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "131", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "130", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "129", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "113", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "112", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "111", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "110", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "109", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "222", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "221", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
    {"section": "220", "price": 300, "color": "Peaches N Cream", "color_code": "#f3a7a7", "capacity_limit": 150},
   
    {"section": "228", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "227", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "226", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "225", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "224", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "218", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "217", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "216", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "215", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},
    {"section": "214", "price": 300, "color": "Skullcrusher Brass", "color_code": "#efc58f", "capacity_limit": 200},

    {"section": "pa2", "price": 400, "color": "Light Whimsy", "color_code": "#97cfe9", "capacity_limit": 400},
    {"section": "pb2", "price": 400, "color": "Light Whimsy", "color_code": "#97cfe9", "capacity_limit": 400},

    {"section": "234", "price": 300, "color": "Peppermint Frosting", "color_code": "#b3f7ed", "capacity_limit": 200},
    {"section": "208", "price": 300, "color": "Peppermint Frosting", "color_code": "#b3f7ed", "capacity_limit": 200},
    
    {"section": "pa1", "price": 500, "color": "Leaf Bud", "color_code": "#f1ef9d", "capacity_limit": 1000},
    {"section": "pb1", "price": 450, "color": "Leaf Bud", "color_code": "#f1ef9d", "capacity_limit": 1000},

    {"section": "134", "price": 500, "color": "Lime Sherbet", "color_code": "#d1d989", "capacity_limit": 200},
    {"section": "108", "price": 450, "color": "Lime Sherbet", "color_code": "#d1d989", "capacity_limit": 200},
]

def initialize_seat_sections():
    """Initialize seat sections for all events"""
    try:
        # Get all events
        response = events_table.scan()
        events = response.get('Items', [])
        
        for event in events:
            event_id = event['event_id']
            
            # Check if seats exist for this event
            existing_seats = seats_table.query(
                IndexName='event_id_index',
                KeyConditionExpression='event_id = :eid',
                ExpressionAttributeValues={':eid': event_id}
            )
            
            if existing_seats.get('Items'):
                print(f"Seats already initialized for event {event_id}")
                continue
            
            # Create seats for this event
            for section in seat_sections:
                seat_id = f"seat_section_{event_id}_{section['section']}"
                seat_item = {
                    'seat_id': seat_id,
                    'event_id': event_id,
                    'section': section['section'],
                    'price': section['price'],
                    'available_tickets': section['capacity_limit'],
                    'reserved_tickets': 0,
                    'sold_tickets': 0,
                    'color': section['color'],
                    'color_code': section['color_code'],
                    'capacity_limit': section['capacity_limit']
                }
                seats_table.put_item(Item=seat_item)
            
            print(f"Initialized seats for event {event_id}")
            
    except ClientError as e:
        print(f"Error initializing seats: {e}")

def update_seat_count(event_id, section, quantity):
    """Update seat availability atomically."""
    try:
        seat_id = f"seat_section_{event_id}_{section}"
        response = seats_table.update_item(
            Key={'seat_id': seat_id},
            UpdateExpression='SET available_tickets = available_tickets - :qty, sold_tickets = sold_tickets + :qty',
            ConditionExpression='available_tickets >= :qty',
            ExpressionAttributeValues={':qty': quantity},
            ReturnValues='UPDATED_NEW'
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        print(f"Error updating seat count: {e}")
        return False

def get_seat_availability(event_id):
    """Get seat availability for an event"""
    try:
        response = seats_table.query(
            IndexName='event_id_index',
            KeyConditionExpression='event_id = :eid',
            ExpressionAttributeValues={':eid': event_id}
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error getting seat availability: {e}")
        return []

