from src.graph import sokoban_graph
from src.sokoban import game_environment
from pathlib import Path
from src.graph.nodes import state_initiator
from opik.integrations.langchain import OpikTracer

def main():
    print("Hello from sokoban-llm-agent!")
    parent_dir =  Path.cwd()
    
    data_file = parent_dir / "dataset/human_demos/4_1.txt" 
    model_name = "openai/gpt-oss-20b"
    # model_name = "google/gemini-2.5-flash"
    # model_name = "deepseek-ai/DeepSeek-R1-0528-Turbo"

    initial_map = game_environment.SokobanGame(data_file)
    
    print("Initial Map:")
    print(str(initial_map.serialize_map()))
    
    agent_state = state_initiator.initiate_state(initial_map, model_name)
    graph = sokoban_graph.build_sokoban_graph()
    app = graph.compile()
    opik_tracer = OpikTracer(graph=app.get_graph(xray=True))
    
    app.invoke(agent_state, config={
        "callbacks": [opik_tracer], 
    },)


if __name__ == "__main__":
    main()
