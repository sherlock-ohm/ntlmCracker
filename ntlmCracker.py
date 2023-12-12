#!/usr/bin/python3

import argparse
import requests
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def make_request(string):
    url = f"https://ntlm.pw/{string}"
    response = requests.get(url)
    return response.status_code, response.text

def process_input(input_data, num_threads=30):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request, line.strip()) for line in input_data]

        for future in as_completed(futures):
            try:
                status_code, response_body = future.result()
                line = input_data[futures.index(future)].strip()
                if status_code == 200:
                    print(f"{line}:{response_body}")
                elif status_code == 204:
                    continue
                elif status_code == 429:
                    print("Rate limit exceeded. Waiting for approx 15 minutes...")
                    time.sleep(905)
                else:
                    print(f"Error: Unexpected status code {status_code} for string '{line}'")
            except Exception as e:
                print(f"Error processing string '{line}': {e}")

def main():
    parser = argparse.ArgumentParser(description="This script makes requests to ntlm.pw with optional threading.")
    parser.add_argument("hashFile", nargs="?", help="Path to the file containing ntlm hashes to process")
    parser.add_argument("--threads", type=int, default=30, help="Number of threads to use (default: 30)")
    args = parser.parse_args()

    if args.hashFile:
        with open(args.hashFile, 'r') as file:
            input_data = file.readlines()
    else:
        input_data = sys.stdin.readlines()

    process_input(input_data, args.threads)

if __name__ == "__main__":
    main()