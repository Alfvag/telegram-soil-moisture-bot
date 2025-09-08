from dotenv import load_dotenv
import os

load_dotenv()

def check_password(password):
    if str(password) == str(os.getenv("SUBSCRIBER_PASSWORD")):
        return True
    
    return False

def message_builder(data):
    # query_result = 


    message = "🌱 Soil Moisture Report 🌱\n\n"
    for plant_name, moisture, timestamp in data:
        message += f"Plant: {plant_name}\n"
        message += f"Moisture: {moisture}%\n"
        message += f"Timestamp: {timestamp}\n"
        message += "-----------------------\n"
    
    return message
