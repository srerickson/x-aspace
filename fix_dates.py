from asnake.client import ASnakeClient
import asnake.logging as logging

# ASnake expects a file: ~/.archivessnake.yml with 
# 'baseurl', 'username', and 'password'
client = ASnakeClient()

logging.setup_logging(level='DEBUG') # logging takes several arguments, provides defaults, etc

# Check all the archival objects in the "Marjorie Kellogg papers" resource
# https://ucsbsbstaff.as.atlas-sys.com/resources/1463
repo_id = 2
resource_id = 1463

# API request to get list of all AOs in the resource.
resources_url = f'/repositories/{repo_id}/resources/{resource_id}/ordered_records'
resp = client.get(resources_url).json()
ao_refs = [ao['ref'] for ao in resp['uris']]

# check each Archival Object ...
for ref in ao_refs:
    ao = client.get(ref).json()
    # check date: inclusive dates where begin and end are the same
    needs_update = False
    for i, date in enumerate(ao['dates']):
        if date['date_type'] == 'inclusive' and date['begin'] == date['end']:
            # fix the date
            ao['dates'][i]['date_type'] = 'single'
            del ao['dates'][i]['end']
            needs_update = True
    # update the ao with fixed dates
    if needs_update:     
       client.post(ref, json=ao)
        
