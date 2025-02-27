from asnake.client import ASnakeClient
import argparse
import sys
from typing import Optional


def fix_box_folders(client: ASnakeClient, repo_id: int) -> None:
    """
   find top-level containers with "box-folder" type and fix them.
    
    Args:
        client (ASnakeClient): Initialized ArchivesSpace client
        repo_id (int): Repository ID in ArchivesSpace
    """
    
    # api endpoint for top-level containers
    endpoint = f'/repositories/{repo_id}/top_containers'
    params = {
        'page': 1,
        'page_size': 1000,
    }
    
    # loop through all pages of top-level containers
    while True:
        response = client.get(endpoint, params=params).json()
        box_folders = [c for c in response['results'] if c['type'] == 'box-folder']
        for box_folder in box_folders:
            print(f"box-folder: {box_folder['uri']}")

            # what are the linked resources to update?

            series_refs = [series['ref'] for series in box_folder.get('series', [])]
            for series_ref in series_refs:
                print(f"-- series: {series_ref}")
            
            collection_refs = [collection['ref'] for collection in box_folder.get('collection', [])]
            for collection_ref in collection_refs:
                print(f"-- collection: {collection_ref}")
                

        
        # Check if there are more pages
        if response['this_page'] == response['last_page']:
            break
        else:
            params['page'] += 1
    

def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Fix box and folder numbers in ArchivesSpace records'
    )
    parser.add_argument(
        '--repo-id',
        type=int,
        required=True,
        help='Repository ID in ArchivesSpace'
    )
    return parser.parse_args()

def main() -> Optional[int]:
    """Main entry point for the script."""
    try:
        args = parse_args()
        # Initialize client and logging here
        client = ASnakeClient()
        # logging.setup_logging(level='DEBUG')
        
        fix_box_folders(client, args.repo_id)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main()) 