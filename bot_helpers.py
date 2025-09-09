from dotenv import load_dotenv
import os
import db_helpers

load_dotenv()

def check_password(password):
    if str(password) == str(os.getenv("SUBSCRIBER_PASSWORD")):
        return True
    
    return False

def message_builder():
    query_result = db_helpers.query_data()

    message = "🌱 Soil Moisture Report 🌱\n\n"
    for plant_data in query_result:
        plant_name = plant_data['plant_name']
        message += f"🪴 Plant: {plant_name}\n"
        
        # Check if there are any measurements
        if plant_data['measurements']:
            # The measurements are already ordered DESC in query_data()
            # So the first element is the most recent measurement
            last_measurement = plant_data['measurements'][0]
            moisture = last_measurement['moisture']
            timestamp = last_measurement['timestamp']
            
            message += f"💧 Moisture: {moisture}%\n"
            message += f"🕑 Time: {timestamp.strftime('%Y-%m-%d %H:%M')}\n"
        else:
            message += "No measurements available\n"
        
        message += "\n"  # Add a blank line between plants
    
    return message