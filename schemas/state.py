# schemas/state.py
from dataclasses import dataclass

@dataclass
class PetState:
    """持有宠物所有实时、易变的内在状态参数。"""
    energy: float = 100.0