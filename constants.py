import os

import dotenv

dotenv.load_dotenv()

# todo: 動的に取得
SHARD_COUNT = 20
DB_HOST = os.environ.get("DB_HOST", "100.121.195.21")
DB_DATABASE = os.environ.get("DB_DATABASE", "postgres")
SESSION_SECRET = os.environ["SESSION_SECRET"]
SESSION_DOMAIN = os.environ.get("SESSION_DOMAIN", "albot.info")
BEARER_TOKEN = os.environ["BEARER_TOKEN"]
STRIPE_SECRET_KEY = os.environ["STRIPE_SECRET_KEY"]
STRIPE_PUBLIC_KEY = os.environ["STRIPE_PUBLIC_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]
DISCORD_CLIENT_ID = os.environ["DISCORD_CLIENT_ID"]
DISCORD_CLIENT_SECRET = os.environ["DISCORD_CLIENT_SECRET"]
BOT_DISCORD_TOKEN = os.environ["BOT_DISCORD_TOKEN"]
BOT_SENTRY_DSN = os.environ["BOT_SENTRY_DSN"]
MONTHLY1_PRICE_ID = os.environ['MONTHLY1_PRICE_ID']
MONTHLY2_PRICE_ID = os.environ['MONTHLY2_PRICE_ID']
YEARLY1_PRICE_ID = os.environ['YEARLY1_PRICE_ID']
YEARLY2_PRICE_ID = os.environ['YEARLY2_PRICE_ID']
SENTRY_DSN = os.environ["SENTRY_DSN"]
PRICE_IDS = {
    'monthly1': MONTHLY1_PRICE_ID,
    'monthly2': MONTHLY2_PRICE_ID,
    'yearly1': YEARLY1_PRICE_ID,
    'yearly2': YEARLY2_PRICE_ID
}
