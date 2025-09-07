from dotenv import load_dotenv
import os

load_dotenv()

def check_password(password):
    if str(password) == str(os.getenv("SUBSCRIBER_PASSWORD")):
        return True
    
    return False

def fetch_subscribers():
    pass

def fetch_data():
    pass

def enroll_subscriber(chat_id):
    pass

def unenroll_subscriber(chat_id):
    pass

