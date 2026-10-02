from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
import random
from collections import Counter


# Shuffle tiles brutely. Perhaps implement a better method?
def shuffle_tiles(tiles):
    random.shuffle(tiles)


#If the string can be converted into an array of tiles, return it
#otherwise return None

#minor bugs to catch for parse_tiles:
#1. 89z are not valid tiles but will pass
#2. invalid tile strings that contain valid chars will pass


def parse_tiles(tile_string):
    valid_chars = set("123456789mpsz")

    if not tile_string:
        return None

    if any(char not in valid_chars for char in tile_string.lower()):
        return None
    
    try:
        tiles = TilesConverter.one_line_string_to_136_array(tile_string)
    except (ValueError, IndexError):
        return None
    
    return tiles


def is_valid_tile_set(tiles):
    tile_types = [tile // 4 for tile in tiles]
    counts = Counter(tile_types)

    return all(count <= 4 for count in counts.values())

def validate_hand(tiles):
    if len(tiles) != 14:
        return False

    if not is_valid_tile_set(tiles):
        return False

    return True



def draw_hand(tiles):
    hand = []
    for x in range(13):
        hand.append(tiles[0])
        tiles.pop(0)
    return hand


#Returns tile drawn for sake of printing information conveniently
def draw_tile(hand, tiles):
    tiledrawn = [tiles[0]]
    hand.append(tiles[0])
    tiles.pop(0)
    return tiledrawn

def discard_tile(hand, tile):
    hand.remove(tile)


