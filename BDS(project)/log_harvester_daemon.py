import socket
import threading
import re
import struct
import os
import time
from collections import defaultdict

HOST = "127.0.0.1"

SERVICES = [
    ("amazon-orders", 9001),
    ("amazon-payment", 9002),
    ("amazon-inventory", 9003),
]

PARTITION_FOLDER = "partitions"

# ---------------- REGEX ----------------

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*\|\s*"
    r"(?P<level>INFO|WARNING|ERROR|DEBUG)\s*\|\s*"
    r"(?P<service>[\w\-]+)\s*\|\s*"
    r"(?P<message>.+)$"
)

LEVEL_CODE = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3
}

CODE_LEVEL = {v: k for k, v in LEVEL_CODE.items()}

partition_files = {}
partition_locks = defaultdict(threading.Lock)
master_lock = threading.Lock()

stats = defaultdict(int)
stats_lock = threading.Lock()


# ---------------- Partition ----------------

def get_partition(service, level):

    key = (service, level)

    with master_lock:

        if key not in partition_files:

            os.makedirs(PARTITION_FOLDER, exist_ok=True)

            filename = os.path.join(
                PARTITION_FOLDER,
                f"{service}_{level}.bin"
            )

            partition_files[key] = open(filename, "ab")

            print(f"Created Partition : {filename}")

        return partition_files[key]


# ---------------- Binary Encoder ----------------

def encode_record(timestamp, level, service, message):

    ts = timestamp.encode().ljust(19, b" ")[:19]

    level_byte = LEVEL_CODE[level]

    service_bytes = service.encode()

    message_bytes = message.encode()

    header = struct.pack(
        "!19sBH",
        ts,
        level_byte,
        len(service_bytes)
    )

    message_header = struct.pack(
        "!H",
        len(message_bytes)
    )

    return header + service_bytes + message_header + message_bytes


# ---------------- Write Binary ----------------

def write_record(record):

    binary = encode_record(
        record["timestamp"],
        record["level"],
        record["service"],
        record["message"]
    )

    length = struct.pack("!I", len(binary))

    key = (
        record["service"],
        record["level"]
    )

    file = get_partition(
        record["service"],
        record["level"]
    )

    with partition_locks[key]:

        file.write(length + binary)

        file.flush()


# ---------------- Process Log ----------------

def process_line(line, service_name):

    match = LOG_PATTERN.match(line)

    if not match:

        with stats_lock:
            stats[(service_name, "REJECTED")] += 1

        return

    record = {

        "timestamp": match.group("timestamp"),

        "level": match.group("level"),

        "service": match.group("service"),

        "message": match.group("message")

    }

    write_record(record)

    with stats_lock:

        stats[(service_name, record["level"])] += 1


# ---------------- Socket Slicing ----------------

def collect_logs(service_name, port):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, port))

    print(f"{service_name} Connected")

    buffer = b""

    try:

        while True:

            chunk = client.recv(4096)

            if not chunk:
                break

            buffer += chunk

            while b"\n" in buffer:

                line, buffer = buffer.split(b"\n", 1)

                try:
                    text = line.decode("utf-8").strip()

                    if text:
                        process_line(text, service_name)

                except UnicodeDecodeError:
                    pass

    finally:

        client.close()


# ---------------- Dashboard ----------------

def print_stats():

    while True:

        time.sleep(3)

        with stats_lock:

            if not stats:
                continue

            print("\n========== Live Statistics ==========")

            for key, value in sorted(stats.items()):

                print(
                    f"{key[0]:20} {key[1]:10} {value}"
                )

            print("=====================================\n")


# ---------------- Main ----------------

def main():

    for service, port in SERVICES:

        threading.Thread(
            target=collect_logs,
            args=(service, port),
            daemon=True
        ).start()

    threading.Thread(
        target=print_stats,
        daemon=True
    ).start()

    print("Amazon Log Harvester Running...\n")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\nClosing Files...")

        for file in partition_files.values():

            file.close()

if __name__ == "__main__":
    main()
   