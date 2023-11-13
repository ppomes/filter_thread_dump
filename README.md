# Java Thread Dump Analyzer

This Python script filters and analyzes Java thread dumps. It provides flexibility in selectively displaying thread information based on criteria such as method names, thread names, and thread statuses. Use it to gain insights into thread activity in Java applications.

## Features

- Filter threads by specified method names (`--method`).
- Filter threads by thread names (`--name`).
- Filter threads by thread status (`--status`).
- Mandatory option to specify the thread dump file (`-f`).

## Usage

```bash
./filter_thread_dump.py -f thread_dump.txt [--method METHOD] [--name NAME] [--status STATUS]
```

