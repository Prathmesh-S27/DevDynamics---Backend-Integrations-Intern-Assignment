def get_current_time():
    from datetime import datetime
    return datetime.utcnow()

def format_response(data, message="Success", status_code=200):
    return {
        "status": status_code,
        "message": message,
        "data": data
    }

def validate_id(id):
    if not isinstance(id, int) or id <= 0:
        raise ValueError("Invalid ID provided")