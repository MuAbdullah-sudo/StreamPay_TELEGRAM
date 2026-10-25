from enum import Enum

class EscrowStatus(Enum):
    CREATED = "CREATED"
    AWAITING_DEPOSIT = "AWAITING_DEPOSIT"
    FUNDS_LOCKED = "FUNDS_LOCKED"
    RELEASED = "RELEASED"
    DISPUTED = "DISPUTED"
    EXPIRED = "EXPIRED"
    REFUNDED = "REFUNDED"

class InvalidStateTransition(Exception):
    pass

class EscrowStateMachine:
    VALID_TRANSITIONS = {
        EscrowStatus.CREATED: [EscrowStatus.AWAITING_DEPOSIT, EscrowStatus.EXPIRED],
        EscrowStatus.AWAITING_DEPOSIT: [EscrowStatus.FUNDS_LOCKED, EscrowStatus.EXPIRED],
        EscrowStatus.FUNDS_LOCKED: [EscrowStatus.RELEASED, EscrowStatus.DISPUTED],
        EscrowStatus.DISPUTED: [EscrowStatus.RELEASED, EscrowStatus.REFUNDED],
        EscrowStatus.RELEASED: [],
        EscrowStatus.EXPIRED: [],
        EscrowStatus.REFUNDED: []
    }

    def __init__(self, deal_id: str, current_status: EscrowStatus = EscrowStatus.CREATED):
        self.deal_id = deal_id
        self.status = current_status

    def transition_to(self, new_status: EscrowStatus) -> EscrowStatus:
        if new_status not in self.VALID_TRANSITIONS[self.status]:
            raise InvalidStateTransition(
                f"Illegal transition: Cannot move escrow {self.deal_id} "
                f"from {self.status.value} to {new_status.value}."
            )
        self.status = new_status
        return self.status

    @staticmethod
    def calculate_fee(amount_usd: float, fee_percentage: float = 0.02, min_fee: float = 1.00) -> float:
        calculated = amount_usd * fee_percentage
        return round(max(calculated, min_fee), 2)