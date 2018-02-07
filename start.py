import numpy as np

from field import Field
from game import Game
# from player import PlayerHuman
# from player import PlayerTrained
# from player import PlayerMax
# from player import PlayerRandomAll
from player import PlayerRandomValidOnly


def play_game(field_size: np.ndarray) -> (int, [np.ndarray], [np.ndarray]):
    field = Field(field_size)  # type: Field
    players = (PlayerRandomValidOnly(0, field_size), PlayerRandomValidOnly(1, field_size))

    game_ins = Game(field, players, [], [], show=True)  # type: Game
    winner, fields, coords = game_ins.start()

    return winner, fields, coords


if __name__ == "__main__":
    # フィールドサイズ
    field_size = np.array([6, 6])

    winner, fields, coords = play_game(field_size)

    print("Winner: " + str(winner))
    print()
