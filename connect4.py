import numpy as np


class Connect4():
    '''
    To play:
    game.play(column), where column in [0, 1, 2, 3, 4, 5, 6]
    there are two players setting their numbers
    If there are diagonally, horisontally or vertically 4 numbers of player,
    he won.
    '''

    def __init__(self):
        self.matrix = np.zeros((7, 6), dtype=np.int0).tolist()
        self.player = 1
        self.over = False

    def play(self, col):
        if self.over:
            return "Game has finished!"
        try:
            index = self.matrix[col].index(0)
        except ValueError:
            return "Column full!"
        self.matrix[col][index] = self.player
        array = np.array(self.matrix)
        diags = []
        for i in np.rot90(np.array(self.matrix)).tolist():
            print(i)
        for i in range(-6, 6):
            diags.append(np.diag(array, k=i).tolist())
            diags.append(np.diag(array[::-1], k=i).tolist())
        for i in self.matrix + array.T.tolist() + diags:
            counter = 0
            for j in i:
                counter = counter + 1 if j == self.player else 0
                if counter == 4:
                    self.over = True
                    print(f"Here we have {i}")
                    return f"Player {self.player} wins!"
        self.player = 1 + self.player % 2
        return f"Player {1 + self.player % 2} has a turn"


game = Connect4()
while not game.over:
    try:
        print(game.play(int(input())))
    except Exception:
        print("Incorrent input! Print something from 0 to 6")
