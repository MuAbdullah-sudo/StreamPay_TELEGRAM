import os

# Supabase Dashboard > Project Settings > API se copy ki hui keys yahan dalo
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://tduagunqtwyufpbmqblx.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRkdWFndW5xdHd5dWZwYm1xYmx4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MTU2ODMwNiwiZXhwIjoyMTA3MTQ0MzA2fQ.ekQEZmr4oE2jtmsI4NYbBjRxZBZue0uvfDu-UzQmcTI")

TELEGRAM_BOT_TOKEN = "8910523871:AAEab9bazo_diKPQwXNcRtf8csWEzd6P_A4"



# Platform Fee Configuration
ESCROW_FEE_PERCENTAGE = 0.02  # 2% fee
MIN_FEE_USD = 1.00            # $1 minimum fee