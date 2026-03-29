# Yarra Trams Service Alerts Viewer - Full Fields Extraction
# Requirements: pip install requests gtfs-realtime-bindings protobuf python-dotenv

import json
import re

import requests
from google.transit import gtfs_realtime_pb2
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import sys

# Load environment variables from .env file
load_dotenv()


# Configuration
API_URL = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/metro/trip-updates"
API_KEY = os.getenv("YARRA_TRAMS_KEYID")

if not API_KEY:
    raise ValueError("YARRA_TRAMS_KEYID not found in .env file. Please add it.")

HEADERS = {"KeyID": API_KEY}
OUTPUT_DIR = "output"
TIMEOUT_SECONDS = 15

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

def get_enum_name(enum_type, value):
    """Get the name of an enum value, or return the numeric value if unknown"""
    try:
        return enum_type.Name(value)
    except ValueError:
        return f"Unknown({value})"
    
def to_iso_or_none(unix_time):
    """Convert a Unix timestamp to ISO format, or return None if not set"""
    if unix_time == 0:
        return None
    return datetime.fromtimestamp(unix_time, tz=timezone.utc).isoformat()

def parse_trip(feed):
    records = []
    for entity in feed.entity:
        if not entity.HasField('trip_update'):
            continue

        trip_update = entity.trip_update
        trip = trip_update.trip
        stop_time_update = trip_update.stop_time_update

        record = {
            "feed_timestamp": to_iso_or_none(feed.header.timestamp) if feed.header.timestamp else None,
            "entity_id": entity.id,
            "trip_id": trip.trip_id,
            "route_id": trip.route_id,
            "start_time": trip.start_time if trip.HasField('start_time') else None,
            "start_date": trip.start_date if trip.HasField('start_date') else None,
            "delay": trip_update.delay if trip_update.HasField('delay') else None,
            "schedule_relationship": get_enum_name(gtfs_realtime_pb2.TripDescriptor.ScheduleRelationship, trip.schedule_relationship),
            "stop_time_updates": [],
            "modifications": []
        }


        for stop_time in stop_time_update:
            record["stop_time_updates"].append({
                "stop_id": stop_time.stop_id,
                "arrival_time": to_iso_or_none(stop_time.arrival.time) if stop_time.HasField('arrival') else None,
                "departure_time": to_iso_or_none(stop_time.departure.time) if stop_time.HasField('departure') else None,
                "schedule_relationship": get_enum_name(gtfs_realtime_pb2.TripUpdate.StopTimeUpdate.ScheduleRelationship, stop_time.schedule_relationship)
            })

        # for mod in trip_modification:
        #     record["modifications"].append({
        #         "modification_type": get_enum_name(gtfs_realtime_pb2.TripModification.ModificationType, mod.modification_type),
        #         "modified_trip_id": mod.trip.trip_id
        #     })

        records.append(record)
    print(f"Parsed {len(records)} trip updates from feed.")
    save_records(records)


def save_records(records):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    output_path = os.path.join(OUTPUT_DIR, f"trip_updates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ndjson")
    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def fetch_and_parse_alerts():
    try:
        feed_content = fetch_feed()
        feed = parse_feed(feed_content)
        parse_trip(feed)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_parse_alerts()