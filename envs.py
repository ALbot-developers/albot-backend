import dotenv
import os

dotenv.load_dotenv()

SHARD_COUNT = 20
SESSION_SECRET = os.environ["SESSION_SECRET"]
DISCORD_CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
DISCORD_CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
