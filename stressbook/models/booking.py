from datetime import datetime
from db_connection import bookings_table, events_table, seats_table
from botocore.exceptions import ClientError
import uuid

# Create indexes
def create_indexes():
    """Create indexes for the bookings collection"""
    # Index for querying bookings by user_id
    bookings_table.meta.client.create_index(
        TableName=bookings_table.name,
        IndexName='user_id_index',
        KeySchema=[{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
        Projection={'ProjectionType': 'ALL'},
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    
    # Compound index for querying by event_id and status
    bookings_table.meta.client.create_index(
        TableName=bookings_table.name,
        IndexName='event_id_status_index',
        KeySchema=[{'AttributeName': 'event_id', 'KeyType': 'HASH'}, {'AttributeName': 'status', 'KeyType': 'RANGE'}],
        Projection={'ProjectionType': 'ALL'},
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )
    
    # Index for timestamp to optimize sorting by date
    bookings_table.meta.client.create_index(
        TableName=bookings_table.name,
        IndexName='timestamp_index',
        KeySchema=[{'AttributeName': 'timestamp', 'KeyType': 'RANGE'}],
        Projection={'ProjectionType': 'ALL'},
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

# Call create_indexes when initializing the application
create_indexes()

def create_booking(user_id, event_id, section, quantity, price_per_ticket, event_name, event_location):
    """Create a new booking using DynamoDB transactions"""
    try:
        booking_id = str(uuid.uuid4())
        booking = {
            'booking_id': booking_id,
            'user_id': user_id,
            'event_id': event_id,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'total_price': price_per_ticket * quantity,
            'seat_details': {
                'section': section,
                'quantity': quantity,
                'price_per_ticket': price_per_ticket
            },
            'event_name': event_name,
            'event_location': event_location
        }

        # Use DynamoDB transactions
        dynamodb = bookings_table.meta.client
        response = dynamodb.transact_write_items(
            TransactItems=[
                {
                    'Put': {
                        'TableName': bookings_table.name,
                        'Item': booking,
                        'ConditionExpression': 'attribute_not_exists(booking_id)'
                    }
                },
                {
                    'Update': {
                        'TableName': events_table.name,
                        'Key': {'event_id': event_id},
                        'UpdateExpression': 'SET available_tickets = available_tickets - :qty, sold_tickets = sold_tickets + :qty',
                        'ConditionExpression': 'available_tickets >= :qty',
                        'ExpressionAttributeValues': {':qty': quantity}
                    }
                }
            ]
        )
        return {"success": True, "booking_id": booking_id}
    except ClientError as e:
        if e.response['Error']['Code'] == 'TransactionCanceledException':
            return {"error": "Not enough tickets available"}
        return {"error": str(e)}

def get_user_bookings(user_id):
    """Get all bookings for a specific user"""
    try:
        response = bookings_table.query(
            IndexName='user_id_index',
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id}
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error fetching user bookings: {e}")
        return []