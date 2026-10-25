import asyncio
from typing import Dict

class AsyncLockManager:
    def __init__(self):
        self._locks: Dict[str, asyncio.Lock] = {}

    def get_lock(self, deal_id: str) -> asyncio.Lock:
        if deal_id not in self._locks:
            self._locks[deal_id] = asyncio.Lock()
        return self._locks[deal_id]

    def release_lock(self, deal_id: str):
        if deal_id in self._locks and not self._locks[deal_id].locked():
            del self._locks[deal_id]

lock_manager = AsyncLockManager()