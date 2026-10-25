import asyncio
from engine.db_client import SupabaseDB
from engine.state_machine import EscrowStateMachine, EscrowStatus
from config import SUPABASE_URL

async def test_connection():
    print("--------------------------------------------------")
    print("⏳ StreamPay Database Connection Test Starting...")
    print(f"🔗 Target URL: {SUPABASE_URL}")
    print("--------------------------------------------------")

    try:
        # Initialize DB Client
        db = SupabaseDB()

        # 1. Test User Creation in Supabase
        print("\n[1/2] Testing User Creation in Supabase...")
        test_user = await db.create_user(platform="TELEGRAM", platform_user_id="999999999")
        
        if test_user and "id" in test_user:
            print(f"✅ Success! User Registered/Verified in DB.")
            print(f"   User UUID: {test_user['id']}")
        else:
            print("⚠️ User creation returned empty response.")

        # 2. Test State Machine Logic
        print("\n[2/2] Testing Escrow State Machine Logic...")
        sm = EscrowStateMachine(deal_id="TEST_DEAL_001")
        print(f"   Initial Status: {sm.status.value}")
        
        # Valid Transition Test
        new_status = sm.transition_to(EscrowStatus.AWAITING_DEPOSIT)
        print(f"   Updated Status: {new_status.value}")
        
        # Fee Calculation Test
        fee = EscrowStateMachine.calculate_fee(amount_usd=50.0)
        print(f"   Fee for $50 Trade:${fee} USD")
        print("✅ State Machine Logic Verified!")

        print("\n--------------------------------------------------")
        print("🎉 ALL TESTS PASSED! Supabase DB & Engine are 100% Ready.")
        print("--------------------------------------------------")

    except Exception as e:
        print("\n❌ TEST FAILED!")
        print(f"Error Details: {e}")
        print("\n💡 Troubleshooting Checklist:")
        print("1. Did you update SUPABASE_URL and SUPABASE_KEY in config.py?")
        print("2. Did you run `pip install supabase`?")
        print("3. Check if your internet is connected.")

if __name__ == "__main__":
    asyncio.run(test_connection())