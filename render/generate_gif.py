
import numpy as np
from PIL import Image, ImageDraw
import imageio
import numpy as np
import pkg_resources
import imageio
from typing import List

def map_sign_to_suface_id(sign: str) -> int:
    """
    Maps a character sign to a surface ID.
    wall, floor, box_target, box_on_target, box, player, player_on_target
    """
    if sign == '#':
        return 0  # wall
    elif sign == ' ':
        return 1  # empty space
    elif sign == '.':
        return 2  # box target
    elif sign == '*':
        return 3  # box on target
    elif sign == '$':
        return 4  # box not on target
    elif sign == '@':
        return 5  # player
    elif sign == '+':
        return 6  # player on target
    else:
        print("sign:", sign)
        raise ValueError(f"Unknown sign: {sign}")


def room_to_img(serialized_map: str):
    """
    Creates an RGB image of the room.
    :param room:
    :param room_structure:
    :return:
    """
    resource_package = __name__
    room = serialized_map.split("\n")
    room = [row.strip() for row in room]
    height = len(room)
    width = len(room[0])
    
    # Load images, representing the corresponding situation
    box_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'box.png')))
    box = imageio.imread(box_filename)

    box_on_target_filename = pkg_resources.resource_filename(resource_package,
                                                             '/'.join(('surface', 'box_on_target.png')))
    box_on_target = imageio.imread(box_on_target_filename)

    box_target_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'box_target.png')))
    box_target = imageio.imread(box_target_filename)

    floor_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'floor.png')))
    floor = imageio.imread(floor_filename)

    player_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'player.png')))
    player = imageio.imread(player_filename)

    player_on_target_filename = pkg_resources.resource_filename(resource_package,
                                                                '/'.join(('surface', 'player_on_target.png')))
    player_on_target = imageio.imread(player_on_target_filename)

    wall_filename = pkg_resources.resource_filename(resource_package, '/'.join(('surface', 'wall.png')))
    wall = imageio.imread(wall_filename)

    surfaces = [wall, floor, box_target, box_on_target, box, player, player_on_target]

    # Assemble the new rgb_room, with all loaded images
    room_rgb = np.zeros(shape=(height * 16, width * 16, 3), dtype=np.uint8)
    for i in range(height):
        x_i = i * 16

        for j in range(width):
            y_j = j * 16
            surface_sign = room[i][j]
            surfaces_id = map_sign_to_suface_id(surface_sign)
            room_rgb[x_i:(x_i + 16), y_j:(y_j + 16), :] = surfaces[surfaces_id]

    return room_rgb


def create_gif(observations, filename="sokoban.gif", success=False):
    """Create GIF from observations"""
    if not observations:
        print("No observations to visualize")
        return

    images = []
    total_frames = len(observations)
    for i in range(total_frames):

        # Get observation and ensure correct format
        obs = observations[i]

        # Create PIL image
        img = Image.fromarray(room_to_img(obs))

        if i == total_frames - 1:
            Im = ImageDraw.Draw(img)
            if success:
                Im.text((20, 20), "Success!",fill=(255, 255, 255))
        
        images.append(img)


    # Save as GIF
    durations = [200] * (len(images) - 1) + [2000]  # last frame stays longer (1s)
    if images:
        images[0].save(
            filename,
            save_all=True,
            append_images=images[1:],
            duration=durations,
            loop=0
        )
        print(f"GIF saved to {filename}")

    else:
        print("No images to create GIF")

from pathlib import Path
from src.sokoban import game_environment
if __name__ == "__main__":

    parent_dir =  Path.cwd()
    data_file = parent_dir / "dataset/human_demos/4_1.txt" 
    model_name = "openai/gpt-oss-20b"

    initial_map = game_environment.SokobanGame(data_file)
    room = initial_map.serialize_map()

    img = room_to_img(room)
    imageio.imwrite('test_room.png', img)