from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

def calculate_hand_score(tiles, win_tile, melds, is_tsumo):
    calculator = HandCalculator()
    config = HandConfig()

    config.is_tsumo = is_tsumo

    result = calculator.estimate_hand_value(
        tiles=tiles,
        win_tile=win_tile,
        melds=melds,
        config=config
    )
    

    return result