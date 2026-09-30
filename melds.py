#
from collections import Counter
from mahjong.meld import Meld


def is_valid_meld(tiles):
    """
    Returns meld type if valid, returns None if meld is not valid
    TODO: add pon from different players, as well as kan types
    """


    if len(tiles) not in (3, 4):
        return None

    # Convert 136-format tiles into their tile types.
    # 0-3   -> 1m
    # 4-7   -> 2m
    # ...
    tile_types = sorted(tile // 4 for tile in tiles)

    # Pon
    if len(tiles) == 3 and len(set(tile_types)) == 1:
        return "pon"

    # Kan
    if len(tiles) == 4 and len(set(tile_types)) == 1:
        return "kan"

    # Chi
    if len(tiles) == 3:
        first, second, third = tile_types

        # Honors can't form sequences
        if first >= 27:
            return None

        # Must belong to the same suit
        if first // 9 != third // 9:
            return None

        # Must be consecutive
        if second == first + 1 and third == second + 1:
            return "chi"

    return None


def meld_in_hand(hand, meld_tiles):
    """
    Returns True if the hand contains every tile required by the meld.
    """

    hand_counts = Counter(tile // 4 for tile in hand)
    meld_counts = Counter(tile // 4 for tile in meld_tiles)

    for tile, count in meld_counts.items():
        if hand_counts[tile] < count:
            return False

    return True


def create_meld(tiles, meld_type):
    """
    Creates the Meld object expected by the mahjong library.
    """

    meld = Meld()
    meld.tiles = tiles
    meld.type = meld_type

    return meld