class Node:
    def __init__(self, data):
        self.data = data
        self.board = data
        self.next = [None for i in range(8)]

    def tie(self):
        count = 9
        for line in self.data:
            for item in line:
                if item:
                    count -= 1
        if count == 0:
            return True
        return False

    def winner(self):

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                if self.board[i][0]:
                    return '{} won'.format(self.board[i][0])
            elif self.board[0][i] == self.board[1][i] == self.board[2][1]:
                if self.board[0][i]:
                    return '{} won'.format(self.board[0][i])
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0]:
                return '{} won'.format(self.board[0][0])
        elif self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2]:
                return '{} won'.format(self.board[0][0])
        if self.tie():
            return 'Draw'
        else:
            return False
class BSTree:
    def __init__(self, data=None):
        self._root = Node(data)

    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

class Board:
    COMPUTER = 'x'
    USER = 'o'
    def __init__(self):
        self.board = [[0 for i in range(3)] for i in range(3)]
    def __str__(self):
        return '{0}|{1}|{2}\n{3}|{4}|{5}\n{6}|{7}|{8}'.format(
    str(self.board[0][0]).replace('0', ' '), str(self.board[0][1]).replace('0', ' '), str(self.board[0][2]).replace('0', ' '),
    str(self.board[1][0]).replace('0', ' '), str(self.board[1][1]).replace('0', ' '), str(self.board[1][2]).replace('0', ' '),
    str(self.board[2][0]).replace('0', ' '), str(self.board[2][1]).replace('0', ' '), str(self.board[2][2]).replace('0', ' '))

    def empty(self, row, col):
        if self.board[row, col]:
            return False
        return True




    def draw_tree(self):
        from copy import deepcopy
        tree = BSTree(deepcopy(self.board))

        def draw_field(current):
            from random import randint
            from copy import deepcopy
            coords = []
            while True:
                row, col = randint(0, 2), randint(0,2)
                row2, col2 = randint(0, 2), randint(0,2)
                if current.data[row][col] == 0 and current.data[row2][col2] == 0:
                    current = deepcopy(current)
                    current.best = [row, col]
                    current.data[row][col] = 'o'
                    current.data[row2][col2] = 'x'
                    return current

        def draw(current):
            if current.tie() == True:
                return
            current.left = draw_field(current)
            current.right = draw_field(current)
            draw(current.left)
            draw(current.right)

        draw(tree._root)
        return tree

    def find_best(self):
        tree = self.draw_tree()
        top = tree._root
        def count(top):
            if not top:
                return 0
            elif top.winner() == 'o won':
                return 1 + count(top.left) + count(top.right)
            elif top.winner() == 'x won':
                return -1 + count(top.left) + count(top.right)
            else:
                return 0 + count(top.left) + count(top.right)
        left = count(top.left)
        right = count(top.right)
        if left > right:
            return top.left.best
        else:
            return top.right.best

    def computer(self):
        coords = self.find_best()
        self.board[coords[0]][coords[1]] = 'o'

    def user_input(self):
        user = input('Your turn(row, col): ').split(',')
        try:
            user = [int(i)-1 for i in user]
        except ValueError:
            self.user_input()
        if self.board[user[0]][user[1]] == 0:
            self.board[user[0]][user[1]] = 'x'
        else:
            self.user_input()

    def start(self):
        while not Node(self.board).winner():
            if Node(self.board).winner():
                print(Node(self.board).winner())
                return
            print(self)
            self.user_input()
            print(self)
            if Node(self.board).winner():
                print(Node(self.board).winner())
                return
            print("Computer's turn")
            self.computer()



game = Board()
game.start()
