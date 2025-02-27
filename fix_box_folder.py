
from asnake.client import ASnakeClient

# returns a list of ao refs for a resource
def get_ao_refs(client: ASnakeClient, repo_id: int, resource_id: int) -> list[str]:
    """returns a list of ao refs for a resource"""
    endpoint = f"/repositories/{repo_id}/resources/{resource_id}/ordered_records"
    response = client.get(endpoint).json()
    ao_refs = [ao["ref"] for ao in response.get("uris", [])]
    return ao_refs

# Modify instances by adding a Folder child container and fixing top container references.  
def fix_ao_instances(client: ASnakeClient, ao_ref: str):
    """Modify instances by adding a Folder child container and fixing top container references."""
    ao = client.get(ao_ref).json()
    for instance in ao.get("instances", []):
        if "sub_container" not in instance:
            return # ignore this instance
        if "top_container" not in instance["sub_container"]:
            return # ignore this instance
        tc_ref = instance["sub_container"]["top_container"]["ref"]
        top_container = client.get(tc_ref).json()
        # Check for improperly formatted top containers
        if top_container.get("type") not in ["box-folder", "Box-folder"]:
            return # ignore this instance
        indicator = top_container.get("indicator", "").strip()
        if ":" not in indicator:
            return # ignore this instance
        
        box_num, folder_num = indicator.split(":", 1)
        box_num, folder_num = box_num.strip(), folder_num.strip()
        # Set the child container correctly
        
        old_child_type = instance["sub_container"].get("child_type", "[None]")
        old_child_indicator = instance["sub_container"].get("child_indicator", "[None]")
        
        new_child_type = "Folder"
        new_child_indicator = folder_num
        # instance["sub_container"]["child_type"] = "Folder"
        # instance["sub_container"]["child_indicator"] = folder_num

        print(f"AO {ao_ref} changes:")
        print(f"-- child_type: '{old_child_type}' -> '{new_child_type}'")
        print(f"-- child_indicator: '{old_child_indicator}' -> '{new_child_indicator}'")

        print(f"-- top_container: {tc_ref}:")
        print(f"--- type: '{top_container.get('type')}' -> 'Box'")
        print(f"--- indicator: '{top_container.get('indicator')}' -> '{box_num}'")


if __name__ == "__main__":
    repo_id = 2
    resource_id = 4397
    batch_size = 5000
    client = ASnakeClient()
    ao_refs = get_ao_refs(client, repo_id, resource_id)
    for ao_ref in ao_refs:
       fix_ao_instances(client, ao_ref)