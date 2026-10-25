from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

class SupabaseDB:
    def __init__(self):
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    async def create_user(self, platform: str, platform_user_id: str) -> dict:
        data = {
            "platform": platform.upper(),
            "platform_user_id": str(platform_user_id)
        }
        response = self.client.table("users").upsert(data, on_conflict="platform,platform_user_id").execute()
        return response.data[0] if response.data else {}

    async def get_deal(self, deal_id: str) -> dict:
        response = self.client.table("escrow_deals").select("*").eq("id", deal_id).single().execute()
        return response.data

    async def update_deal_status(self, deal_id: str, new_status: str, tx_hash: str = None) -> dict:
        update_data = {"status": new_status, "updated_at": "now()"}
        if tx_hash:
            update_data["tx_hash"] = tx_hash
            
        response = self.client.table("escrow_deals").update(update_data).eq("id", deal_id).execute()
        return response.data[0] if response.data else {}