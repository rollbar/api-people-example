"""
Script to query the Rollbar API for "person" data for each occurrence of a list of items.

To run, you'll need:
- python with requests 2.0 installed (virtualenv will work)
- the 'read' access token for the project the items are in (find this in Settings > Access Tokens)
- the list of item ids (see below).

Output is written to a file with the person data for each occurrence on each line. Occurrences without person data are skipped. Output is written as a json object for each line.

Stdout will have status information.

Usage:

python fetch_people_for_items.py <read access token> <output filename> <item id 1> [<item id 2, etc.>]


To get the item ids
-------------------
If just one item, go to the Occurrences tab, then click on one of the timestamps, then find the id in the url: rollbar.com/item/ITEM_ID_HERE/instance/INSTANCE_ID_HERE

If lots of item ids (i.e. from a search), use the browser. Go to the Items page, run your search, and then you can get item ids for everything on the page by running this in the chrome console:

  var ids = []; 
  $('tr.item-details').each(function() { ids.push($(this).attr('data-reactid').match(/\{(\d+)\}/)[1]); }); 
  console.log(ids.join(" "));
"""

import sys
import json
import requests  # version 2


def fetch_people_for_item(access_token, output_file, item_id):
    page_number = 1
    while True:
        print "Fetching page", page_number
        page_data = fetch_page(access_token, item_id, page_number)
        if not page_data:
            # we have reached the end
            break

        for instance in page_data:
            person_data = instance['data'].get('person')
            if person_data:
                output_file.write(json.dumps(person_data) + '\n')
                output_file.flush()

        page_number += 1


def fetch_page(access_token, item_id, page=1):
    resp = requests.get('https://api.rollbar.com/api/1/item/%d/instances/?access_token=%s&page=%d' %
        (item_id, access_token, page))
    
    if resp.status_code != 200:
        print resp
        raise Exception("Got an error from the Rollbar API")
    
    return resp.json()['result']['instances']

    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: python fetch_people_for_items.py <read access token> <output filename> <item id 1> [<item id 2> ...]"
        sys.exit(1)
    
    access_token = sys.argv[1]
    output_filename = sys.argv[2]
    item_ids = [int(x) for x in sys.argv[3:]]

    output_file = open(output_filename, 'w')

    for item_id in item_ids:
        fetch_people_for_item(access_token, output_file, item_id)

