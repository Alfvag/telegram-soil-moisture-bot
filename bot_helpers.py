from dotenv import load_dotenv
import os
import db_helpers
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
from datetime import datetime

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

def generate_moisture_plot():
    # Get the data
    query_result = db_helpers.query_data()
    
    # Create a DataFrame to hold all data
    all_data = []
    
    # Process each plant's data
    for plant_data in query_result:
        plant_name = plant_data['plant_name']
        
        for measurement in plant_data['measurements']:
            all_data.append({
                'plant_name': plant_name,
                'moisture': measurement['moisture'],
                'timestamp': measurement['timestamp']
            })
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    
    # Make sure timestamp is datetime type
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp
    df = df.sort_values('timestamp')
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    
    # Plot each plant as a separate line
    for plant_name, group in df.groupby('plant_name'):
        plt.plot(group['timestamp'], group['moisture'], marker='o', linestyle='-', label=plant_name)
    
    # Set labels and title
    plt.xlabel('Date & Time')
    plt.ylabel('Moisture Percentage (%)')
    plt.title('Soil Moisture Levels Over Time')
    
    # Format the x-axis to show dates nicely
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.gcf().autofmt_xdate()  # Rotate date labels for better visibility
    
    # Add legend to distinguish between plants
    plt.legend()
    
    # Add grid for better readability
    plt.grid(True, alpha=0.3)
    
    # Set y-axis to start from 0
    plt.ylim(bottom=0)
    
    # Create a buffer to save the plot
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Close the plot to free memory
    plt.close()
    
    return buf