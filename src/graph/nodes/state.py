# src/graph/state.py
from typing import TypedDict, List
from src.sokoban.game_environment import SokobanGame

class SokobanState(TypedDict, total=False):
    map: SokobanGame                    # Current board
    status: str                         # "unsolved", "continue", "invalid", "success", etc.
    moves: str                          # All executed primitive moves (L/R/U/D)
    solution: str                       # solution steps (exclude those repetitive cyclic steps)
    max_iterations: int                 # max allowed iteration times
    visited_map_state: List[str]        # visited maps (serialized)
    current_iteration: int              # current iteration index
    records: dict                       # running metadata recording
    model_name: str                     # the LLM model name on deepinfra
    
