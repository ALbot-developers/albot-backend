import dotenv
import os

dotenv.load_dotenv()

SHARD_COUNT = 20
SESSION_SECRET = os.environ["SESSION_SECRET"]
