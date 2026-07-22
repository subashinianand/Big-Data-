Amazon Log Monitoring System

This project simulates an Amazon log monitoring system using Python sockets and multithreading. It collects real-time logs from multiple servers,
stores them in binary partition files based on service and log level, and provides a binary log reader to decode and display the stored logs.
The project demonstrates log collection, partitioning, binary encoding, and decoding for efficient log management.



# MapReduce Simulation in Python

## Project Overview
This project demonstrates the working of the MapReduce programming model using Python. It processes a sample hospital dataset 
and counts the number of patients in each department through different MapReduce phases.

## Project Structure
```

│── data.txt
│── splitter.py
│── mapper.py
│── partitioner.py
│── sorter.py
│── reducer.py
│── master.py

```

## Files Description
- **data.txt** – Sample input dataset.
- **splitter.py** – Splits the input data into smaller chunks.
- **mapper.py** – Converts each record into key-value pairs.
- **partitioner.py** – Groups identical keys together.
- **sorter.py** – Sorts the grouped key-value pairs.
- **reducer.py** – Counts the values for each key and produces the final output.
- **master.py** – Executes all MapReduce stages in sequence.

## How to Run
Open a terminal in the project folder and run:

```bash
python master.py
```

## Sample Output
```
Final Output:
Cardiology : 3
Neurology : 2
Orthopedics : 2
Pediatrics : 1
```

## Technologies Used
- Python 3
- MapReduce Concepts
- File Handling
- Dictionary and List Data Structures

