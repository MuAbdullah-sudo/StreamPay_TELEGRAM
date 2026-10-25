import asyncio
import logging
import sys
import uuid
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TELEGRAM_BOT_TOKEN
from engine.db_client import SupabaseDB
from engine.state_machine import EscrowStateMachine, EscrowStatus

# Initialize DB & Bot
db = SupabaseDB()
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Welcomes the user and shows how to use StreamPay."""
    name = message.from_user.full_name
    welcome_text = (
        f"Yo, **{name}**! 🛡️\n\n"
        f"Welcome to **StreamPay** — The Zero-Scam P2P Crypto Escrow Engine.\n\n"
        f"📌 **Commands:**\n"
        f"• `/escrow <amount_usd>` - Create a new secure escrow deal.\n"
        f"• `/status <deal_id>` - Check your escrow status."
    )
    await message.answer(welcome_text, parse_mode="Markdown")


@dp.message(Command("escrow"))
async def command_escrow_handler(message: Message) -> None:
    """Handles escrow creation via Telegram command: /escrow 50"""
    args = message.text.split()

    if len(args) < 2:
        await message.answer("⚠️ **Usage Error:** Please specify the amount.\nExample: `/escrow 50` (for $50 USD)", parse_mode="Markdown")
        return

    try:
        amount_usd = float(args[1])
        if amount_usd < 1.0:
            await message.answer("⚠️ Minimum escrow amount is **$1.00 USD**.", parse_mode="Markdown")
            return

        # 1. Register or fetch user in Supabase
        user = await db.create_user("TELEGRAM", str(message.from_user.id))

        # 2. Calculate fee using our 2% state machine rule
        fee = EscrowStateMachine.calculate_fee(amount_usd)
        total_due = amount_usd + fee

        # 3. Generate unique deposit address for this deal
        dummy_deposit_address = f"0xStreamPay{uuid.uuid4().hex[:32]}"

        # 4. Insert deal into Supabase
        deal_data = {
            "buyer_id": user["id"],
            "amount_usd": amount_usd,
            "fee_usd": fee,
            "currency": "USDT/ETH",
            "deposit_address": dummy_deposit_address,
            "expected_crypto_amount": total_due,
            "status": EscrowStatus.AWAITING_DEPOSIT.value,
            "description": f"Telegram P2P Escrow by User ID {message.from_user.id}"
        }

        res = db.client.table("escrow_deals").insert(deal_data).execute()
        deal = res.data[0]

        # 5. Send confirmation response to user
        response_text = (
            f"🛡️ **StreamPay Escrow Initialized!**\n\n"
            f"🆔 **Deal ID:** `{deal['id']}`\n"
            f"💵 **Trade Amount:** `${amount_usd}` USD\n"
            f"⚡ **Platform Fee (2%):** `${fee}` USD\n"
            f"💰 **Total Expected:** `{total_due}`\n\n"
            f"📍 **Deposit Address:**\n`{dummy_deposit_address}`\n\n"
            f"⏳ Send funds to the address above. Our automated background watcher is listening for your deposit!"
        )
        await message.answer(response_text, parse_mode="Markdown")

    except ValueError:
        await message.answer("⚠️ Invalid amount format. Please enter a valid number (e.g., `/escrow 100`).", parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Error creating escrow deal: {e}")


async def main():
    if TELEGRAM_BOT_TOKEN == "YOUR_BOTFATHER_TOKEN_HERE":
        print("❌ ERROR: Please put your valid Telegram Bot Token from BotFather in config.py!")
        return

    bot = Bot(token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    print("🤖 Telegram Bot UI Started & Polling for Messages...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())