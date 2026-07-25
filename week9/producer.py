"""Week 9 lab — produce keyed messages across a multi-partition topic.

Each message is KEYED by order_id, so all events for the same order land on the
same partition and stay in order, while different orders spread across the three
partitions. Watch the partition each message is sent to: a given key always maps
to the same partition.
"""
import json
import time

from kafka import KafkaProducer
 

# Several events per ticket_id, across a handful of orders, interleaved in time.
# These ids spread across all three partitions of a 3-partition topic.
events = [
    ("INC123", "Ticket_created"), ("INC456", "Ticket_created"), ("INC789", "Ticket_created"), ("INC1112", "Ticket_created"),
    ("INC1516", "Ticket_created"), ("INC1314", "Ticket_created"), ("INC123", "Assigned"),    ("INC456", "Assigned"),
    ("INC789", "Assigned"),    ("INC1516", "In-Progress"), ("INC1314", "Assigned"),    ("INC1112", "In-Progress"),
    ("INC123", "In-Progress"), ("INC123", "Resolved"),
]

for ticket_id, status in events:
    event = {"ticket_id": ticket_id, "status": status}
    md = producer.send(TOPIC, key=ticket_id, value=event).get(timeout=10)
    print(f"ticket {ticket_id:<3} {status:<10} -> partition {md.partition} offset {md.offset}")
    time.sleep(0.3)

producer.flush()
producer.close()
print("done — notice every event for a given ticket_id landed on the same partition.")
