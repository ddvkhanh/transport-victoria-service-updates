import json
import os
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from google.transit import gtfs_realtime_pb2

# Load environment variables from .env file
load_dotenv()

# Configuration
API_URL = "https://api.opendata.transport.vic.gov.au/opendata/public-transport/gtfs/realtime/v1/metro/service-alerts"
API_KEY = os.getenv("PTV_KEYID")
HEADERS = {"KeyID": API_KEY}
OUTPUT_DIR = "output"
TIMEOUT_SECONDS = 15

if not API_KEY:
    raise ValueError("YARRA_TRAMS_KEYID not found in .env file. Please add it.")


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
    """
    Extract the first available text from a TranslatedString.
    Prefer English if present, otherwise fall back to the first translation.
    """
    if not translated_string.translation:
        return None

    for t in translated_string.translation:
        if t.language == "en" or not t.language:
            return t.text

    return translated_string.translation[0].text


def to_iso_or_none(unix_time):
    """Convert Unix timestamp to ISO-8601 UTC string, or None if not set."""
    if not unix_time:
        return None
    return datetime.fromtimestamp(unix_time, tz=timezone.utc).isoformat()


def get_enum_name(enum_type, value):
    """
    Safely convert protobuf enum numeric value to enum name.
    Returns None if the value is missing/unknown.
    """
    try:
        return enum_type.Name(value)
    except ValueError:
        return f"UNKNOWN_{value}"
    

def save_records(records):
    output_path = f"service_updates_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ndjson"

    with open(output_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved {len(records)} records to: {output_path}")



def extract_informed_entities(alert):
    entities = []

    for ie in alert.informed_entity:
        item = {
            "agency_id": ie.agency_id if ie.HasField("agency_id") else None,
            "route_id": ie.route_id if ie.HasField("route_id") else None,
            "direction_id": ie.direction_id if ie.HasField("direction_id") else None,
            "stop_id": ie.stop_id if ie.HasField("stop_id") else None,
        }
        entities.append(item)
    return entities

def extract_active_periods(alert):
    periods = []
    for p in alert.active_period:
        start = to_iso_or_none(p.start) if p.HasField("start") else None
        end = to_iso_or_none(p.end) if p.HasField("end") else None
        periods.append({"start": start, "end": end})
    return periods


def extract_alert_record(alert):
        alert = {
            "header_text": translate_text(alert.header_text) if alert.HasField("header_text") else None,
            "description_text": translate_text(alert.description_text) if alert.HasField("description_text") else None,
            "severity_level": get_enum_name(gtfs_realtime_pb2.Alert.SeverityLevel, alert.severity_level) if alert.HasField("severity_level") else None,
            "cause": get_enum_name(gtfs_realtime_pb2.Alert.Cause, alert.cause) if alert.HasField("cause") else None,
            "effect": get_enum_name(gtfs_realtime_pb2.Alert.Effect, alert.effect) if alert.HasField("effect") else None,
            "informed_entities": extract_informed_entities(alert),
            "active_periods": extract_active_periods(alert)
        }
        return alert


def fetch_and_parse_record(feed):
    records = []
    now_unix = int(datetime.now(timezone.utc).timestamp())
    feed_time = to_iso_or_none(feed.header.timestamp) if feed.header.timestamp else "missing"
    print(f"\nFeed generated at: {feed_time}")
    print(f"Total entities in feed: {len(feed.entity)}\n")

    for entity in feed.entity:
        if not entity.HasField('alert'):
            continue

        record = {
            "entity_timestamp": to_iso_or_none(feed.header.timestamp) if feed.header.timestamp else None,
            "entity_id": entity.id,
            "alert": extract_alert_record(entity.alert) if entity.HasField("alert") else None,
            "ingest_timestamp": to_iso_or_none(int(datetime.now(timezone.utc).timestamp()))        
        }
        records.append(record)

    save_records(records)


if __name__ == "__main__":
    try:
        feed_content = fetch_feed()
        feed = parse_feed(feed_content)
        fetch_and_parse_record(feed)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.RequestException as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)