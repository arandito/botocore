import boto3
import logging
import json

def print_buffer(val):
    for i in range(5):
        if i == 2:
            print(f"---------------------------- TEST {val} ------------------------------")
        else:
            print("----------------------------------------------------------------------")

def debug_event_handler(event_name, **kwargs):
    """Debug event handler to understand the event structure"""
    print(f"\n🔍 Event: {event_name}")
    print(f"📦 Event kwargs keys: {list(kwargs.keys())}")
    
    # Try different ways to access the request
    for key, value in kwargs.items():
        print(f"  {key}: {type(value)}")
        
        # If it's the request object, explore its attributes
        if hasattr(value, 'headers'):
            print(f"    📋 Headers: {dict(value.headers)}")
        elif hasattr(value, 'url'):
            print(f"    🌐 URL: {value.url}")
        elif key == 'request' and hasattr(value, '__dict__'):
            print(f"    🔧 Request attributes: {list(value.__dict__.keys())}")
            if hasattr(value, 'headers'):
                headers = value.headers
                print(f"    📋 Headers: {dict(headers) if headers else 'No headers'}")

def capture_user_agent(event_name, **kwargs):
    """Event handler to capture and print the User-Agent header"""
    if 'before-send' in event_name:
        # Try multiple ways to get the User-Agent
        request = kwargs.get('request')
        if request and hasattr(request, 'headers'):
            user_agent = request.headers.get('User-Agent', 'No User-Agent found')
            print(f"✅ User-Agent: {user_agent}")
            
            # Also show the service being called
            if hasattr(request, 'url'):
                print(f"🎯 URL: {request.url}\n")

# Create session
session = boto3.Session(profile_name="assumeroletest")

# # First, register a debug handler to see all events
# # print("🐛 Registering debug handler...")
# session.events.register('before-send', debug_event_handler)

# Then register the actual User-Agent capture handler
session.events.register('before-send', capture_user_agent)

s3 = session.client("s3")

response = s3.list_buckets()

response = s3.list_buckets()

response = s3.list_buckets()

