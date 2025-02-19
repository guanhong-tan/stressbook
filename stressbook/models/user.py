from datetime import datetime
from db_connection import users_table
from botocore.exceptions import ClientError
import uuid

def create_user(name, email, password):
    """Create a new user in DynamoDB."""
    try:
        user = {
            'user_id': str(uuid.uuid4()),
            'email': email,
            'name': name,
            'password': password,  # In production, use proper password hashing
            'created_at': datetime.now().isoformat()
        }
        users_table.put_item(
            Item=user,
            ConditionExpression='attribute_not_exists(email)'
        )
        return {"status": "success", "user_id": user['user_id']}
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return {"status": "error", "message": "Email already exists"}
        return {"status": "error", "message": str(e)}

def user_login(email, password):
    """Verify user login credentials."""
    try:
        response = users_table.get_item(
            Key={'email': email}
        )
        user = response.get('Item')
        if user and user['password'] == password:  # In production, use proper password verification
            return user
        return None
    except ClientError as e:
        print(f"Error in user login: {e}")
        return None

def update_user_profile(user_id, name, email):
    """Update user profile information."""
    try:
        users_table.update_item(
            Key={'email': email},
            UpdateExpression='SET #n = :name',
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': name
            }
        )
        return True
    except ClientError as e:
        print(f"Error updating user profile: {e}")
        return False

def is_email_used(email):
    """Check if email is already registered."""
    try:
        response = users_table.get_item(
            Key={'email': email}
        )
        return 'Item' in response
    except ClientError as e:
        print(f"Error checking email: {e}")
        return False