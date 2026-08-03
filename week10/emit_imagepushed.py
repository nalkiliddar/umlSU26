"""Announce an ImagePushed event by hand, so you can drive the release gate
without running Jenkins.

    python emit_imagepushed.py 1     # ImagePushed for calculator version 1
"""
import sys
import json
from kafka import KafkaProducer

version = sys.argv[1] if len(sys.argv) > 1 else "1"

# Connect directly to the hostname advertised by the broker
BROKER = "week10-kafka:9092"

print(f"Connecting to broker [{BROKER}] to emit event for version {version}...")

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    api_version=(2, 5, 0),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

event = {
    "event": "ImagePushed", 
    "image": "calculator", 
    "version": version, 
    "registry": "localhost:5001"
}

try:
    # Send the message and force an instant 5-second failure check
    producer.send("ci.images", event).get(timeout=5)
    producer.flush()
    print(f"🎉 Emitted successfully to cluster log: {event}")
except Exception as e:
    print(f"❌ Failed to send event: {e}")
