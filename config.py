import os

# Supabase Dashboard > Project Settings > API se copy ki hui keys yahan dalo
SUPABASE_URL = os.getenv("SUPABASE_URL", "PASTE SUPABASE_URL HERE!")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "PASTE SUPABASE_KEY HERE!")

TELEGRAM_BOT_TOKEN = "PASTE TELEGRAM_BOT_TOKEN HERE!"



# Platform Fee Configuration
ESCROW_FEE_PERCENTAGE = 0.02  # 2% fee
MIN_FEE_USD = 1.00            # $1 minimum fee
