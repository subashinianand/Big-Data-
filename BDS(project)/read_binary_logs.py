import struct
import sys


LEVEL_CODE = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3
}

CODE_LEVEL = {v: k for k, v in LEVEL_CODE.items()}


def read_records(filepath):
    """Read and decode binary log records."""

    with open(filepath, "rb") as file:
        data = file.read()

    offset = 0
    records = []

    while offset < len(data):

        
        (record_length,) = struct.unpack_from("!I", data, offset)
        offset += 4

        
        record = data[offset:offset + record_length]
        offset += record_length

        
        timestamp_bytes, level_byte, service_length = struct.unpack_from(
            "!19sBH", record, 0
        )

        position = 19 + 1 + 2

        
        service = record[position:position + service_length].decode("utf-8")
        position += service_length

        # Read message length
        (message_length,) = struct.unpack_from("!H", record, position)
        position += 2

        # Read message
        message = record[position:position + message_length].decode("utf-8")

        records.append({
            "timestamp": timestamp_bytes.decode("ascii").strip(),
            "level": CODE_LEVEL[level_byte],
            "service": service,
            "message": message
        })

    return records


def main():

    if len(sys.argv) != 2:
        print("Usage:")
        print("python read_binary_logs.py partitions/amazon-chennai_ERROR.bin")
        return

    filepath = sys.argv[1]

    records = read_records(filepath)

    print("\n==============================================")
    print(" AMAZON BINARY LOG READER")
    print("==============================================")
    print(f"File : {filepath}")
    print(f"Total Records : {len(records)}")
    print("==============================================\n")

    for record in records:
        print(
            f"{record['timestamp']} | "
            f"{record['level']} | "
            f"{record['service']} | "
            f"{record['message']}"
        )


if __name__ == "__main__":
    main()