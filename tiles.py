from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld
import random


# Shuffle tiles brutely. Perhaps implement a better method?
def shuffle_tiles(tiles):
    random.shuffle(tiles)


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