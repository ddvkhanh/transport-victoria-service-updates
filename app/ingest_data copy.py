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
API_URL = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/tram/service-alerts"
API_KEY = os.getenv("YARRA_TRAMS_KEYID")

if not API_KEY:
    raise ValueError("YARRA_TRAMS_KEYID not found in .env file. Please add it.")

HEADERS = {"KeyID": API_KEY}

def get_translated_text(translated_string):
    """Extract the first available text from a TranslatedString (usually English)"""
    if not translated_string.translation:
        return "(no text)"
    # Prefer English, fall back to first available
    for t in translated_string.translation:
        if t.language == "en" or not t.language:
            return t.text
    return translated_string.translation[0].text  # fallback

def fetch_and_parse_alerts():
    try:
        print("Fetching latest Yarra Trams service alerts...")
        response = requests.get(API_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        feed_time = datetime.fromtimestamp(feed.header.timestamp, tz=timezone.utc) if feed.header.timestamp else "missing"
        print(f"\nFeed generated at: {feed_time} UTC")
        print(f"Total entities in feed: {len(feed.entity)}\n")

        active_count = 0
        now_unix = int(datetime.now(timezone.utc).timestamp())

        for entity in feed.entity:
            if not entity.HasField('alert'):
                continue

            alert = entity.alert


            print("══════════════════════════════════════════════════════════════")
            print(f"  Entity ID         : {entity.id}")
            print(f"  Header Text       : {get_translated_text(alert.header_text)}")
            print(f"  Description Text  : {get_translated_text(alert.description_text)}")

            # Optional but useful fields
            if alert.HasField('cause'):
                print(f"  Cause             : {alert.cause}")
            if alert.HasField('effect'):
                print(f"  Effect            : {alert.effect}")

            # Active periods
            if alert.active_period:
                print("  Active Periods:")
                for i, p in enumerate(alert.active_period, 1):
                    s = p.start if p.HasField('start') else "N/A (past)"
                    e = p.end   if p.HasField('end')   else "N/A (ongoing)"
                    print(f"    {i}: {s} → {e}")
            else:
                print("  Active Periods    : Always active (no time range defined)")

            # Informed entities (routes, stops, etc.)
            if alert.informed_entity:
                print("  Affected Entities:")
                for i, ie in enumerate(alert.informed_entity, 1):
                    parts = []
                    if ie.HasField('route_id'):     parts.append(f"route={ie.route_id}")
                    if ie.HasField('stop_id'):      parts.append(f"stop={ie.stop_id}")
                    if ie.HasField('agency_id'):    parts.append(f"agency={ie.agency_id}")
                    if ie.HasField('route_type'):   parts.append(f"type={ie.route_type}")
                    if ie.HasField('direction_id'): parts.append(f"dir={ie.direction_id}")
                    print(f"    {i}: {', '.join(parts) or 'empty selector'}")

            # Rare/optional fields
            extras = []
            if alert.HasField('url'):                  extras.append("url")
            if alert.HasField('tts_header_text'):      extras.append("tts_header_text")
            if alert.HasField('tts_description_text'): extras.append("tts_description_text")
            if alert.HasField('severity_level'):       extras.append("severity_level")
            if alert.HasField('cause'):         extras.append("cause")
            if alert.HasField('effect'):        extras.append("effect")
            if extras:
                print(f"  Additional fields present: {', '.join(extras)}")

            print()

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing feed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_parse_alerts()