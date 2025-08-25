
from openai import OpenAI
from src import config

class LLM_client:
    def __init__(self, model_name):
        self.llm = OpenAI(
            api_key=config.DEEPINFRA_API_Key, # input your api key here
            base_url="https://api.deepinfra.com/v1/openai",
        )
        self.temperature = 0.5
        self.model_name = model_name
        
        self.SYSTEM_PROMPT_PLAN = F''' 
        You are a skilled player of Sokoban game. Your task is to provide a detailed step-by-step plan to solve the sokoban game. The sokoban game is a puzzle game where the player must push boxes onto target locations in a grid-like environment. The player can only move in four directions (up, down, left, right) and cannot move through walls or other boxes. The goal is to push all boxes onto their respective target locations.        
        The steps should be in the format of a numbered list, where each step describes the player's movement and the box movement if applicable.
        
        **Sokoban Rules:**

        1. Walls (#) are completely blocked.
        The player cannot move into a wall.
        Boxes cannot be pushed into a wall.
        Treat walls as impassable boundaries.

        2. Player movement:
        The player (@) can move up, down, left, or right into an empty space ( ) or a target (.).
        The player cannot move diagonally.
        The player cannot move into a wall.

        3. Pushing boxes ($):
        If the player moves into a box, the box is pushed one step in the same direction.
        A box can only be pushed if the square behind it is free (empty or target .).
        A box cannot be pushed into a wall or another box.

        4. Winning condition:
        The game is solved when all boxes ($) are placed on all targets (.).

        ** sokoban map format: **
        The map is stored in a nested list. Each item represents the element at that position. "#" represents the wall, "@" represents player, "$" represents box, and "." represents target. " " represents the empty free space which player or box can move into. 
        
        **Example:**
        - MAP (indexing from 0):
        [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'], ['#', '#', ' ', '$', ' ', ' ', ' ', ' ', '#', '#'], ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'], ['#', '#', ' ', ' ', ' ', '$', ' ', ' ', '#', '#'], ['#', '#', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#'], ['#', '#', ' ', '.', ' ', ' ', '.', '@', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]
        Player position: (7,7) 
        box positions: (3,3), (5,5). 
        target positions: (7,3), (7,6).
        
        - Your Output:
        1. <U> Move the player from (7,7) to (6,7), box positions are kept as (3,3), (5,5)
        2. <U> Move the player from (6,7) to (5,7), box positions are kept as (3,3), (5,5)
        3. <U> Move the player from (5,7) to (4,7), box positions are kept as (3,3), (5,5)
        4. <L> Move the player from (4,7) to (4,6), box positions are kept as (3,3), (5,5)
        5. <L> Move the player from (4,6) to (4,5), box positions are kept as (3,3), (5,5)
        6. <D> Move the player from (4,5) to (5,5), box positions are updated to (3,3), (6,5)
        7. <D> Move the player from (5,5) to (6,5), box positions are updated to (3,3), (7,5)
        8. <L> Move the player from (6,5) to (6,4), box positions are kept as (3,3), (7,5)
        9. <D> Move the player from (6, 4) to (7, 4), box positions are kept as (3,3), (7,5)
        10. <R> Move the player from (6, 4) to (7, 4), box positions are updated to (3,3) to (7,6)
        11. <L> Move the player from (7,5) to (7,4), box positions are kept as (3,3), (7,6)
        12. <L> Move the player from (7,4) to (7,3), box positions are kept as (3,3), (7,6)
        13: <L> Move the player from (7,3) to (7,2), box positions are kept as (3,3), (7,6)
        14. <U> Move the player from (7,2) to (6,2), box positions are kept as (3,3), (7,6)
        15. <U> Move the player from (6,2) to (5,2), box positions are kept as (3,3), (7,6)
        16. <U> Move the player from (5,2) to (4,2), box positions are kept as (3,3), (7,6)        
        17. <U> Move the player from (4,2) to (3,2), box positions are kept as (3,3), (7,6)
        18. <U> Move the player from (3, 2) to (2,2), box positions are kept as (3,3), (7,6)
        19. <R> Move the player from (2,2) to (2,3), box positions are kept as (3,3), (7,6)
        20. <D> Move the player from (2,3) to (3,3), box positions are updated to (4,3) to (7,6)
        21. <D> Move the player from (3,3) to (4,3), box positions are updated to (5,3) to (7,6)
        22. <D> Move the player from (4,3) to (5,3), box positions are updated to (6,3) to (7,6)
        23. <D> Move the player from (5,3) to (6,3), box positions are updated to (7,3) to (7,6)
        '''.strip()

        self.plan_messages = [{"role": "system", "content": self.SYSTEM_PROMPT_PLAN}]

    def query_llm_for_moves(self, user_prompt=None):
        total_messages = self.plan_messages.copy()
        if user_prompt:
            total_messages.append({"role": "user", "content": str(user_prompt)})
            
        response = self.llm.chat.completions.create(
            model=self.model_name,
            messages=total_messages,
            temperature=self.temperature,
            
        )
        return response.choices[0].message.content
    

    def post_processing_moves(self, response):
        steps = ""
        plan = response.strip().split('\n') 

        for i, step in enumerate(plan):
        
            if "<U>" in step or "**U**" in step: 
                steps += "U"
            elif "<D>" in step or "**D**" in step:
                steps += "D" 
            elif "<L>" in step or "**L**" in step: 
                steps += "L"
            elif "<R>" in step or "**R**" in step:
                steps += "R"
            
        return steps
