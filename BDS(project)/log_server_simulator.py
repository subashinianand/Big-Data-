import socket
import threading
import time
import random
from datetime import datetime

HOST = "127.0.0.1"

BRANCHES = [
    ("amazon-chennai", 9001),
    ("amazon-bangalore", 9002),
    ("amazon-mumbai", 9003),
]

LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]

MESSAGES = [
    "Order received",
    "Payment successful",
    "Payment failed",
    "Order packed",
    "Order shipped",
    "Order delivered",
    "Inventory updated",
    "Low stock detected",
    "Warehouse temperature high",
    "Delivery delayed",
    "Customer cancelled order",
    "Package scanned",
    "Driver assigned",
    "Server health check completed",
    "Database connection established",
    "API response timeout",
    "Customer refund initiated",
    "Item returned",
    "Shipment departed",
    "Shipment arrived"
]


def generate_log(branch):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(LEVELS)
    message = random.choice(MESSAGES)

    return f"{timestamp} | {level} | {branch} | {message}\n"


def start_server(branch, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, port))
    server.listen(5)

    print(f"{branch} running on port {port}")

    while True:
        client, addr = server.accept()
        print(f"{branch}: Client Connected")

        while True:
            try:
                log = generate_log(branch)
                client.sendall(log.encode("utf-8"))
                print(log.strip())
                time.sleep(random.uniform(0.5, 2))
            except:
                print(f"{branch}: Client Disconnected")
                break

        client.close()


def main():
    threads = []

    for branch, port in BRANCHES:
        t = threading.Thread(
            target=start_server,
            args=(branch, port),
            daemon=True
        )
        t.start()
        threads.append(t)

    print("\nAmazon Log Server Simulator Running...\n")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()