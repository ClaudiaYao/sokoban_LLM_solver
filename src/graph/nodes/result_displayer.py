from src.graph.nodes.state import SokobanState
import os
import pandas as pd 
from pathlib import Path
from render import generate_gif 

record_path = "result/running_record.csv"
temp_folder = Path.cwd() / "result"
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

    
def generate_result(state: SokobanState) -> SokobanState:
    """
    Record the running information to save to dataframe.
    Record the running steps to show dynamic map change.
    """
    if state['status'] == "success":
        print("🚀Congratulation🚀 You solved the puzzle: ", state['moves'])        
    elif state['status'] == "end":
        print("The AI fails to solve it. Try it later🏄🏽")
        
    # record the running meta data for model comparison
    file_name = state['map'].data_file
    state['records']['data_file']  = file_name
    state['records']['moves'] = state["moves"]
    state['records']['result'] = state['status']
    state['records']['iteration'] = state['current_iteration']
    
    print("state['records]:", state['records'])
    new_df = pd.DataFrame([state['records']])
    if os.path.exists(record_path):
        existing_df = pd.read_csv(record_path)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(record_path, index=False)
    else:
        new_df.to_csv(record_path, index=False)
        
    # record each step in the dynamic map.    
    with open(temp_folder / f"result_map_{file_name}", 'w') as f:
        f.write(state['map'].serialize_map())
        f.write("\n")
        f.write("\n")
        
        for map in state['visited_map_state']:
            f.write(map)
            f.write("\n")
            f.write("\n")
    print("Save the dynamic steps in result.txt.")
    
    # save the dynamic map as gif
    generate_gif.create_gif(state['visited_map_state'], filename=temp_folder / f"result_map_{file_name[:-4]}.gif", success=(state['status']=="success"))
            
    return state
