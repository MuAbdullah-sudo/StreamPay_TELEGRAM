StreamPay Telegram Edition was envisioned as a chat-native Web3 escrow engine integrated into Telegram’s bot ecosystem using Python (python-telegram-bot / telebot) with Supabase handling state management. Built for broader crypto trading communities, OTT account buyers, and digital service freelancing groups on Telegram, this version relied on inline keyboards and automated message polling/webhooks. Users could spin up P2P escrow deals inside group chats or via direct messages with the bot, featuring real-time status updates and simplified user identification using unique Telegram IDs without requiring explicit wallet web-app connections.


Why the Project Faced Friction & Was Paused

    Discord 3-Second Execution Timeout: Discord requires an immediate response to slash command webhooks within 3,000 milliseconds. Cold starts on serverless platforms combined with multiple sequential network roundtrips (fetching user data, inserting deals into Supabase, and sending HTTP requests) frequently breached this strict window, triggering constant "application didn't respond in time" errors.

    Environment & Serverless Network Bottlenecks: Hosting external bot logic on free serverless tiers (or free proxies like PythonAnywhere) caused proxy connection drops, HTTPSConnectionPool max-retry failures, and missing environment variable bindings (Error: fetch failed), making asynchronous database calls unreliable.

    High Infrastructure Maintenance vs. Zero Budget: Continuous backend state tracking, edge-case database handling, and real-time polling created heavy backend maintenance overhead—contradicting the goal of building a friction-free, zero-maintenance utility.
