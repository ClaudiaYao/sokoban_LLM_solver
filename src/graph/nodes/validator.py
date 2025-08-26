
from src.graph.nodes.state import SokobanState

def validate_state(state: SokobanState) -> SokobanState:
    """
    validate the running status and then go back to different node in the graph.
    """

    if state['status'] == "invalid" or state['status'] == "unsolved" or state['status'] == "empty":
        if state['current_iteration'] >= state['max_iterations']:
            print(f"could not find the solution after {state['max_iterations']} times.")
            return "end"
        else:
            print("Could not find solution at trial: ", state['current_iteration'])
            return "go_moves"
    elif state['status'] == "success":
        return "success"
