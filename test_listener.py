import asyncio
from engine.db_client import SupabaseDB
from engine.deposit_listener import DepositListener
from engine.state_machine import EscrowStatus

async def run_listener_test():
    db = SupabaseDB()
    
    # Clean up any previous test entry with this zero address to avoid unique constraint violation
    db.client.table("escrow_deals").delete().eq("deposit_address", "0x0000000000000000000000000000000000000000").execute()

    # 1. Create a dummy escrow deal in AWAITING_DEPOSIT state
    print("📝 Creating Test Escrow Deal in DB...")
    user = await db.create_user("TELEGRAM", "123456789")
    
    deal_data = {
        "buyer_id": user["id"],
        "amount_usd": 10.0,
        "fee_usd": 1.0,
        "currency": "ETH",
        "deposit_address": "0x0000000000000000000000000000000000000000",  
        "expected_crypto_amount": 0.0000001,  
        "status": EscrowStatus.AWAITING_DEPOSIT.value
    }
    
    res = db.client.table("escrow_deals").insert(deal_data).execute()
    test_deal = res.data[0]
    print(f"✅ Created Test Deal ID: {test_deal['id']} | Status: {test_deal['status']}")

    # 2. Run Listener for 1 cycle (15 seconds)
    listener = DepositListener(db)
    print("\n🚀 Starting Listener Test (Will run for 15 seconds)...")
    
    task = asyncio.create_task(listener.poll_pending_deposits())
    await asyncio.sleep(15)
    listener.stop()
    task.cancel()
    
    # 3. Verify status updated in DB
    updated_deal = await db.get_deal(test_deal['id'])
    print(f"\n📊 Final Deal Status in DB: {updated_deal['status']}")
    
    if updated_deal['status'] == EscrowStatus.FUNDS_LOCKED.value:
        print("🎉 DEPOSIT LISTENER TEST PASSED! Status updated to FUNDS_LOCKED.")
    else:
        print("⚠️ Status was not updated.")

if __name__ == "__main__":
    asyncio.run(run_listener_test())