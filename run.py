from asnake.client import ASnakeClient
import asnake.logging as logging

logging.setup_logging(level='DEBUG')

client = ASnakeClient()
repos = client.get("repositories").json()

print(repos)