#!/usr/bin/env python

import re
import sys
import argparse

def filter_threads(thread_dump, method_filter, name_filter, status_filter):
    filtered_threads = []

    current_thread = None

    for line in thread_dump:
        # Search for a line indicating the start of a new thread
        thread_match = re.match(r'^"(.+)"', line)
        if thread_match:
            # If we already have a current thread, add it to the list if it meets the specified filters
            if current_thread is not None and (
                (not method_filter or any(method_filter in method for method in current_thread["methods"])) and
                (not name_filter or name_filter in current_thread["name"]) and
                (not status_filter or current_thread["status"] == status_filter)
            ):
                filtered_threads.append(current_thread)

            # Initialize a new thread
            current_thread = {"name": thread_match.group(1), "methods": [], "status": None}
        elif 'java.lang.Thread.State' in line:
            # Extract the thread status
            current_thread["status"] = line.strip().split(':')[-1].strip()
        else:
            # Search for lines containing methods
            method_match = re.search(r'\s+at (.+)', line)
            if method_match:
                # Add the method to the current thread
                current_thread["methods"].append(method_match.group(1))

    # Add the last thread if it meets the specified filters
    if current_thread is not None and (
        (not method_filter or any(method_filter in method for method in current_thread["methods"])) and
        (not name_filter or name_filter in current_thread["name"]) and
        (not status_filter or current_thread["status"] == status_filter)
    ):
        filtered_threads.append(current_thread)

    return filtered_threads

def main():
    parser = argparse.ArgumentParser(description="Filter threads from a Java thread dump.")
    parser.add_argument("-f", "--file", help="Specify the thread dump file to read", required=True)
    parser.add_argument("--method", help="Filter threads containing a specified method (e.g., com.company)")
    parser.add_argument("--name", help="Filter threads by name (case-sensitive)")
    parser.add_argument("--status", help="Filter threads by status (e.g., RUNNABLE)")

    args = parser.parse_args()

    try:
        with open(args.file, "r") as file:
            thread_dump_lines = file.readlines()

        # Filter threads
        filtered_threads = filter_threads(thread_dump_lines, args.method, args.name, args.status)

        # Display filtered threads
        for thread in filtered_threads:
            print(f'Thread "{thread["name"]}" (Status: {thread["status"]}) meets the specified criteria:')
            for method in thread["methods"]:
                print(f'  {method}')
            print('\n')

    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()
