"""Announce an ImagePushed event by hand, so you can drive the release gate
without running Jenkins.

    python emit_imagepushed.py 1     # ImagePushed for calculator version 1
"""
import sys
import json
from kafka import KafkaProducer

version = sys.argv[1] if len(sys.argv) > 1 else "1"

# DYNAMIC FIX: Uses 'localhost:9092' if run on Windows, or 'week10-kafka:9092' if run inside Docker
BROKER = "week10-kafka:9092" 

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    api_version=(2, 5, 0),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
)

event = {"event": "ImagePushed", "image": "calculator", "version": version, "registry": "localhost:5001"}
print(f"Connecting to broker [{BROKER}] to emit event...")

producer.send("ci.images", event)
producer.flush()
print("emitted", event)
