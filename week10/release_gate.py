"""Week 10 capstone (skeleton) — the release gate.

It consumes `ImagePushed` events from Kafka. For each one it should deploy that
version of the calculator, run the acceptance test, and promote the version to
`:latest` if the test passes. If the test fails, it does nothing.

The docker and HTTP mechanics are written for you (deploy, run_tests, promote,
teardown). run_tests already waits for the container to come up. YOUR job is the
consumer loop, marked with TODO: read the version, deploy it, test it, and
promote it on success.

Run it:  python release_gate.py
Feed it: run the pipeline, or `python emit_imagepushed.py <version>`
"""
import json
import subprocess
import time
import urllib.request
import os
import sys

# --- Force Auto-Install Kafka library if it's missing ---
try:
    from kafka import KafkaConsumer
except ModuleNotFoundError:
    print("📦 'kafka' module missing inside Jenkins environment. Attempting runtime installation...")
    subprocess.run([sys.executable, "-m", "pip", "install", "kafka-python", "--break-system-packages"], check=True)
    from kafka import KafkaConsumer

BROKER = os.environ.get("BROKER", "week10-kafka:9092")
IN = "ci.images"
HOST_PORT = 18080          

# --- DYNAMIC REGISTRY RESOLUTION BLOCK ---
# If running inside the Jenkins container filesystem, route over the docker bridge to local-registry:5000
if os.path.exists("/var/jenkins_home") or os.environ.get("JENKINS_HOME"):
    REGISTRY = "local-registry:5000"
else:
    REGISTRY = "localhost:5001"


# ===========================================================================
# Provided for you. These do the docker and HTTP work; you should not need to
# change them. Focus on the consumer loop at the bottom.
# ===========================================================================

def deploy(version):
    """Pull and start calculator:<version>, mapped to HOST_PORT."""
    ref = f"{REGISTRY}/calculator:{version}"
    name = f"candidate-{version}"
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    subprocess.run(["docker", "pull", ref], check=True, capture_output=True)
    subprocess.run(["docker", "run", "-d", "--name", name, "-p", f"{HOST_PORT}:8080", ref],
                   check=True, capture_output=True)


def run_tests():
    """The acceptance test: 1 + 2 must equal 3. Waits for the service to come up
    (it takes a few seconds), then returns True (passed) or False (wrong answer,
    or it never came up)."""
    url = f"http://localhost:{HOST_PORT}/sum?a=1&b=2"
    for _ in range(15):
        try:
            answer = urllib.request.urlopen(url, timeout=2).read().decode().strip()
            print(f"    GET /sum?a=1&b=2 -> {answer!r} (want '3')")
            return answer == "3"
        except OSError:
            time.sleep(1)          # not up yet, wait and retry
    print("    service never came up")
    return False


def promote(version):
    """Promote the tested image to the released tag: tag :latest and push."""
    src = f"{REGISTRY}/calculator:{version}"
    dst = f"{REGISTRY}/calculator:latest"
    print(f"    [PROMOTE] Tagging {src} -> {dst}")
    subprocess.run(["docker", "pull", src], check=True, capture_output=True)
    subprocess.run(["docker", "tag", src, dst], check=True)
    subprocess.run(["docker", "push", dst], check=True, capture_output=True)
    print(f"    promoted calculator:{version} to calculator:latest")


def teardown(version):
    """Stop and remove the candidate container once you are done testing it."""
    subprocess.run(["docker", "rm", "-f", f"candidate-{version}"], capture_output=True)


# ===========================================================================
# YOUR WORK starts here: the consumer loop.
# ===========================================================================

consumer = KafkaConsumer(
    IN,
    bootstrap_servers=BROKER,
    group_id="release-gate-final-v4", # Changed name to force Kafka to read from the 'earliest' offset again
    auto_offset_reset="latest",
    api_version=(2, 5, 0),
    value_deserializer=lambda b: json.loads(b.decode()),
)

print("release gate up — waiting for ImagePushed events. Ctrl-C to stop.")
for msg in consumer:
    event = msg.value
    print(f"\n[EVENT Received]: Full Payload Received -> {json.dumps(event)}")
        
    version = event.get('version')
    print(f"--> Extracted Version: {version}")
    
    if not version:
        print("⚠️ Warning: Event message format missing 'version' key. Skipping workflow loop.")
        continue
        
    try:
        
        print(f" Start Deployment pipeline or Version #{version}...")
        deploy(version)
        
        
        test_passed = run_tests()
        
        # 4. 
        if test_passed:
            print(f" Test successful for Version #{version}. Begin Promote...")
            promote(version)
        else:
            print(f"Test failed for Version #{version}. Abort.")
            
    except Exception as error_context:
        print(f"Exception: {error_context}")
        
    finally:
        
        teardown(version)
        print(f"Work is complete for Build Version: {version}")
        
    
    print("Processing completed successfully.")
    break


    # TODO: read the version from the event.
    # TODO: deploy(version), then run_tests(). If it passes, promote(version).
    #       If it fails, do nothing.
    # TODO: teardown(version) when you are done with the candidate container.
