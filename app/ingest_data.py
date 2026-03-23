# Yarra Trams Service Alerts Viewer - Full Fields Extraction
# Requirements: pip install requests gtfs-realtime-bindings protobuf python-dotenv

import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()

# Configuration
API_URL = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/tram/trip-updates"
API_KEY = os.getenv("YARRA_TRAMS_KEYID")

if not API_KEY:
    raise ValueError("YARRA_TRAMS_KEYID not found in .env file. Please add it.")

HEADERS = {"KeyID": API_KEY}
OUTPUT_DIR = "output"
TIMEOUT_SECONDS = 15

# def get_translated_text(translated_string):
#     """Extract the first available text from a TranslatedString (usually English)"""
#     if not translated_string.translation:
#         return "(no text)"
#     # Prefer English, fall back to first available
#     for t in translated_string.translation:
#         if t.language == "en" or not t.language:
#             return t.text
#     return translated_string.translation[0].text  # fallback

def fetch_feed():
    print("Fetching latest Yarra Trams service alerts...")
    response = requests.get(API_URL, headers=HEADERS, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()
    return response.content

def parse_feed(feed_content):
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(feed_content)
    return feed

def translate_text(translated_string):
    """Extract the first available text from a TranslatedString (usually English)"""
    if not translated_string.translation:
        return "(no text)"
    # Prefer English, fall back to first available
    for t in translated_string.translation:
        if t.language == "en" or not t.language:
            return t.text
    return translated_string.translation[0].text  # fallback

def display_alerts(feed):
    feed_time = datetime.fromtimestamp(feed.header.timestamp, tz=timezone.utc) if feed.header.timestamp else "missing"
    print(f"\nFeed generated at: {feed_time} UTC")
    print(f"Total entities in feed: {len(feed.entity)}\n")

    active_count = 0
    now_unix = int(datetime.now(timezone.utc).timestamp())

    for entity in feed.entity:

        trip_update = entity.trip_update
        trip = trip_update.trip
        stop_time_update = trip_update.stop_time_update

        print("══════════════════════════════════════════════════════════════")

        print(f"  Entity ID         : {entity.id}")
        print(f"  Trip ID           : {trip.trip_id}")
        print(f"  Route ID          : {trip.route_id}")
        print(f"  Start Time         : {trip.start_time}")
        print(f"  Start Date        : {trip.start_date}")
        print(f"  Schedule Relationship : {trip.schedule_relationship}")
        
        for stop_time in stop_time_update:
            print(f"    Stop ID         : {stop_time.stop_id}")
            print(f"    Arrival Time    : {stop_time.arrival.time if stop_time.HasField('arrival') else 'N/A'}")
            print(f"    Departure Time  : {stop_time.departure.time if stop_time.HasField('departure') else 'N/A'}")
            print(f"    Schedule Relationship : {stop_time.schedule_relationship}")

def fetch_and_parse_alerts():
    try:
        feed_content = fetch_feed()
        feed = parse_feed(feed_content)
        display_alerts(feed)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_parse_alerts()