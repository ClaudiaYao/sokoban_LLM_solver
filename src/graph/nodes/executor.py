from src.graph.nodes.state import SokobanState
import copy

def execute_moves(state: SokobanState) -> SokobanState:
    """
    Executes the moves issued by plan.
    """

    tmp_map = copy.deepcopy(state['map'])
    total_moves = ""
    
    if state['moves'] == "":
        state['status'] = "empty"
        return state
        
    for move in state['moves']:
        if tmp_map.makeMove(move):
            total_moves += move
            cur_map_state = tmp_map.serialize_map()
            
            if tmp_map.isLevelFinished():
                state['status'] = "success"
                state['visited_map_state'].append(cur_map_state)
                state['solution'] = total_moves
                return state 
            else:

                if cur_map_state in state['visited_map_state']:
                    idx = state['visited_map_state'].index(cur_map_state)
                    total_moves = total_moves[: idx+1]
                    state['visited_map_state'] = state['visited_map_state'][: idx+1]
                    print("enter into repeated steps")
                    continue 
                else:
                    state['visited_map_state'].append(cur_map_state)
        else:
            state["moves"] = ""
            state["status"] = "invalid"
            return state

    state['status'] = "unsolved"
    return state
