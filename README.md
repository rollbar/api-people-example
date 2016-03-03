# api-people-example

Script to query the Rollbar API for "person" data for each occurrence of a list of items.

To run, you'll need:
- python with requests 2.0 installed (virtualenv will work)
- the 'read' access token for the project the items are in (find this in Settings > Access Tokens)
- the list of item ids (see below).

Output is written to a file with the person data for each occurrence on each line. Occurrences without person data are skipped. Output is written as a json object for each line.

Stdout will have status information.

Usage:

```
python fetch_people_for_items.py <read access token> <output filename> <item counter 1> [<item counter 2, etc.>]
```
