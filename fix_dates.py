from asnake.client import ASnakeClient
import asnake.logging as logging
import argparse
import sys
from typing import Optional

def fix_dates(client: ASnakeClient, repo_id: int, resource_id: int) -> None:
    """
    Fix date types in ArchivesSpace records where inclusive dates have identical begin/end dates.
    
    Args:
        client (ASnakeClient): Initialized ArchivesSpace client
        repo_id (int): Repository ID in ArchivesSpace
        resource_id (int): Resource ID to process
    """
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

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Fix ArchivesSpace dates where inclusive dates have identical begin/end dates'
    )
    parser.add_argument(
        '--repo-id',
        type=int,
        required=True,
        help='Repository ID in ArchivesSpace'
    )
    parser.add_argument(
        '--resource-id',
        type=int,
        required=True,
        help='Resource ID to process'
    )
    return parser.parse_args()

def main() -> Optional[int]:
    """Main entry point for the script."""
    try:
        args = parse_args()
        # Initialize client and logging here
        client = ASnakeClient()
        logging.setup_logging(level='DEBUG')
        
        fix_dates(client, args.repo_id, args.resource_id)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
        
