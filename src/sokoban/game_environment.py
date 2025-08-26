from typing import List

class SokobanGame:
    """A class that contains the AI for the Sokoban game."""

    def __init__(self, data_file=None):
        self.DATA_FILE = data_file
        self.AcTION_SEQUENCE = None
        self.gameStateObj = None
        self.mapObj = None
        self.levelObj = None
        
        self.read_map(data_file)
        self.data_file = str(data_file).rsplit("/", 1)[1]


    def isWall(self, x, y):
        """Returns True if the (x, y) position on
        the map is a wall, otherwise return False."""
        if x < 0 or x >= len(self.mapObj) or y < 0 or y >= len(self.mapObj[x]):
            return False # x and y aren't actually on the map.
        elif self.mapObj[x][y] in ('#', 'x'):
            return True # wall is blocking
        return False


    def isBlocked(self, x, y):
        """Returns True if the (x, y) position on the map is
        blocked by a wall or star, otherwise return False."""

        if self.isWall(x, y):
            return True

        elif x < 0 or x >= len(self.mapObj) or y < 0 or y >= len(self.mapObj[x]):
            return True # x and y aren't actually on the map.

        elif (x, y) in self.gameStateObj['boxes']:
            return True # a box is blocking
        return False


    def makeMove(self, playerMoveTo):
        """Given a map and game state object, see if it is possible for the
        player to make the given move. If it is, then change the player's
        position (and the position of any pushed box). If not, do nothing.
        Returns True if the player moved, otherwise False."""

        # Make sure the player can move in the direction they want.
        playerx, playery = self.gameStateObj['player']
        boxes = self.gameStateObj['boxes']

        if playerMoveTo == "U":
            xOffset = -1
            yOffset = 0
        elif playerMoveTo == "R":
            xOffset = 0
            yOffset = 1
        elif playerMoveTo == "D":
            xOffset = 1
            yOffset = 0
        elif playerMoveTo == "L":
            xOffset = 0
            yOffset = -1

        # See if the player can move in that direction.
        if self.isWall(playerx + xOffset, playery + yOffset):
            return False
        else:
            if (playerx + xOffset, playery + yOffset) in boxes:
                if not self.isBlocked(playerx + (xOffset*2), playery + (yOffset*2)):
                    ind = boxes.index((playerx + xOffset, playery + yOffset))
                    boxes[ind] = (boxes[ind][0] + xOffset, boxes[ind][1] + yOffset)
                else:
                    return False
            self.gameStateObj['player'] = (playerx + xOffset, playery + yOffset)
            return True


    def read_map(self, file_path):
        current_map = []
        with open(file_path, 'r') as sf:
            for line in sf.readlines():
                if '#' == line[0]:          # if the current line contains # which represents wall, then continue add this line as current map
                    current_map.append(line.strip())
                else:
                    break  
                
        self.mapObj = [list(mapline) for mapline in current_map]     

        # Loop through the spaces in the map and find the @, ., and $
        # characters for the starting game state.
        startx = None # The x and y for the player's starting position
        starty = None
        goals = [] # list of (x, y) tuples for each goal.
        boxes = [] # list of (x, y) for each star's starting position.

        for x in range(len(self.mapObj)):
            for y in range(len(self.mapObj[0])):

                if self.mapObj[x][y] == '@':
                    startx = x
                    starty = y

                if self.mapObj[x][y] == '.':
                    goals.append((x, y))
                if self.mapObj[x][y] == '$':
                    boxes.append((x, y))
                if self.mapObj[x][y] == "*":
                    goals.append((x, y))
                    boxes.append((x, y))

        # Basic level design sanity checks:
        assert startx != None and starty != None, 'Level missing a "@" or "+" to mark the start point.' 
        assert len(goals) > 0, 'Levelmust have at least one goal.'
        assert len(boxes) >= len(goals), 'Level is impossible to solve. It has %s goals but only %s stars.'

        # Create level object and starting game state object.
        self.gameStateObj = {'player': (startx, starty),
                        'stepCounter': 0,
                        'boxes': boxes}
        self.levelObj = {'width': len(self.mapObj[0]),
                    'height': len(self.mapObj),
                    'mapObj': self.mapObj,
                    'goals': goals,
                    'startState': self.gameStateObj}

    # store back the current map conditions to file again for rendering/observation purposing 
    def convert_current_state_to_map(self) -> List[List[str]]:
        map_width = self.levelObj['width']
        map_height = self.levelObj['height']
        map = self.levelObj['mapObj']
        
        starting_map = self.levelObj['mapObj']
        goal_pos = self.levelObj['goals']
        
        for i in range(map_height):
            for j in range(map_width):
                if starting_map[i][j] == "#":
                    map[i][j] = "#"
                # updated player and stars position
                elif starting_map[i][j] == ".":
                    if (i, j) == self.gameStateObj['player']:
                        map[i][j] = "+"
                    elif (i, j) in self.gameStateObj['boxes']:
                        map[i][j] = "*"
                    else:
                        map[i][j] = "."
                elif (i, j) == self.gameStateObj['player']:
                        map[i][j] = "@" 
                elif (i, j) in self.gameStateObj['boxes']:
                        map[i][j] = "$"
                else:
                # other places are just floor
                    map[i][j] = " "

        return map

    def serialize_map(self) -> str:
        return "\n".join("".join(row) for row in self.convert_current_state_to_map())

    def deserialize_map(self, s: str) -> List[List[str]]:
        return [list(row) for row in s.splitlines()]

    def isLevelFinished(self):
        """Returns True if all the goals have stars in them."""
        for goal in self.levelObj['goals']:
            if goal not in self.gameStateObj['boxes']:
                return False
        return True