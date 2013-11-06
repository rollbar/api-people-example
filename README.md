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
python fetch_people_for_items.py <read access token> <output filename> <item id 1> [<item id 2, etc.>]
```


## To get the item ids
If just one item, go to the Occurrences tab, then click on one of the timestamps, then find the id in the url: rollbar.com/item/ITEM_ID_HERE/instance/INSTANCE_ID_HERE

If lots of item ids (i.e. from a search), use the browser. Go to the Items page, run your search, and then you can get item ids for everything on the page by running this in the chrome console:

```js
var ids = []; 
$('tr.item-details').each(function() { ids.push($(this).attr('data-reactid').match(/\{(\d+)\}/)[1]); }); 
console.log(ids.join(" "));
```
