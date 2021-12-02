"""
Script to query the Rollbar API for "person" data for each occurrence of a list of items.

To run, you'll need:
- python with requests 2.0 installed (virtualenv will work)
- the 'read' access token for the project the items are in (find this in Settings > Access Tokens)
- the list of item ids (see below).

Output is written to a file with the person data for each occurrence on each line. Occurrences without person data are skipped. Output is written as a json object for each line.

Stdout will have status information.

Usage:

python fetch_people_for_items.py <read access token> <output filename> <item counter 1> [<item counter 2, etc.>]
"""

from __future__ import print_function

import sys
import json
import requests  # version 2


def fetch_item_id_for_counter(access_token, item_counter):
    resp = requests.get(
        "https://api.rollbar.com/api/1/item_by_counter/{}".format(item_counter),
        headers={"X-Rollbar-Access-Token": access_token},
        allow_redirects=False,
    )

    if resp.status_code != 301:
        print(resp)
        raise Exception("Got an API error while fetching an item by counter")

    return resp.json()["result"]["itemId"]


def fetch_people_for_item_id(access_token, output_file, item_id):
    page_number = 1
    while True:
        print("Fetching page", page_number)
        page_data = fetch_page(access_token, item_id, page_number)
        if not page_data:
            # we have reached the end
            break

        for instance in page_data:
            person_data = instance["data"].get("person")
            if person_data:
                output_file.write(json.dumps(person_data) + "\n")
                output_file.flush()

        page_number += 1


def fetch_page(access_token, item_id, page=1):
    resp = requests.get(
        "https://api.rollbar.com/api/1/item/{}/instances/?page={}".format(item_id, page),
        headers={"X-Rollbar-Access-Token": access_token},
    )

    if resp.status_code != 200:
        print(resp)
        raise Exception("Got an error from the Rollbar API")

    return resp.json()["result"]["instances"]


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python fetch_people_for_items.py <read access token> <output filename> <item id 1> [<item id 2> ...]")
        sys.exit(1)

    access_token = sys.argv[1]
    output_filename = sys.argv[2]
    item_counters = [int(x) for x in sys.argv[3:]]

    output_file = open(output_filename, "w")

    for item_counter in item_counters:
        item_id = fetch_item_id_for_counter(access_token, item_counter)
        fetch_people_for_item_id(access_token, output_file, item_id)
