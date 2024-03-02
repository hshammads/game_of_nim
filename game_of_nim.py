import copy
import itertools
import random
from collections import namedtuple
import numpy as np
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QPushButton, QLabel

GameState = namedtuple('GameState', 'to_move, utility, board, moves')
StochasticGameState = namedtuple('StochasticGameState', 'to_move, utility, board, moves, chance')

global number_of_rows
number_of_rows = 1
global items_list
items_list = []
global moves_list
moves_list = []
global move
move = tuple()
move = 0,0

class StartWindow(QDialog):
    def __init__(self):
        super(StartWindow, self).__init__()
        loadUi("start.ui", self)
        self.next.clicked.connect(self.gotorowWindow)

    def gotorowWindow(self):
        rownumwin = RowWindow()
        widget.addWidget(rownumwin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class RowWindow(QDialog):
    def __init__(self):
        super(RowWindow, self).__init__()
        loadUi("rownum.ui", self)

        self.rownuminput.setPlaceholderText("1 - 10")
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("""color: red;""")
        self.success_label = QLabel(self)
        self.error_label.move(290,170)
        self.success_label.move(285,175)

        self.verify.clicked.connect(self.validate)
        #self.home.clicked.connect(self.gotostartWindow)
        self.next.clicked.connect(self.gotoitemWindow)

    def gotostartWindow(self):
        #self.error_label.setText("")
        #self.success_label.setText("")
        startwindow = StartWindow()
        widget.addWidget(startwindow)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def gotoitemWindow(self):
        itemwin = ItemWindow()
        widget.addWidget(itemwin)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def validate(self):

        global number_of_rows
        rownumval = self.rownuminput.text()
        if rownumval == "":
            rownumval = 0
        try:
            val = float(rownumval)
            if val == "" or not val.is_integer() or val < 1 or val > 10:
                print("Invalid input! Parameter given is either blank or not an integer or it is outside of defined range")
                self.success_label.setText("")
                self.error_label.setText("Invalid Input: " + str(rownumval) + "\nPlease enter a valid integer (1 - 10)")
                self.error_label.adjustSize()
                self.error_label.setDisabled(True)
            else:
                number_of_rows = int(val)
                self.error_label.setText("")
                self.success_label.setText("Number of rows selected: " + str(number_of_rows))
                self.success_label.adjustSize()
                self.success_label.setDisabled(True)
                print("Number of rows value: " + str(number_of_rows))
        except:
            print("Invalid input! Please enter a valid input")
            self.success_label.setText("")
            self.error_label.setText("Invalid Input: " + rownumval + "\nPlease enter a valid integer (1 - 10)")
            self.error_label.adjustSize()
            self.error_label.setDisabled(True)


class ItemWindow(QDialog):
    def __init__(self):
        super(ItemWindow, self).__init__()
        loadUi("itemnum.ui", self)

        global number_of_rows

        self.itemnuminput.setPlaceholderText("separate by commas")
        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("""color: red;""")
        self.success_label = QLabel(self)
        self.row_num_label = QLabel(self)
        self.error_label.move(220,225)
        self.success_label.move(110,225)
        self.row_num_label.move(220,205)

        self.row_num_label.setText("Number of rows selected: " + str(number_of_rows))
        self.row_num_label.adjustSize()
        self.row_num_label.setDisabled(True)

        self.verify.clicked.connect(self.validate)
        #self.home.clicked.connect(self.gotostartWindow)
        self.next.clicked.connect(self.gotogame)

    def gotostartWindow(self):
        #self.error_label.setText("")
        #self.success_label.setText("")
        startwindow = StartWindow()
        widget.addWidget(startwindow)
        widget.setCurrentIndex(widget.currentIndex() - 2)

    def gotogame(self):
        gamewindow = GameWindow()
        widget.addWidget(gamewindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def validate(self):

        global items_list
        items_list = []
        global number_of_rows
        global moves_list
        moves_list = []
        item_input = self.itemnuminput.text()
        temp_item_array = item_input.split(",")
        validation_success = True
        for i in range(0,len(temp_item_array)):
            item_num_val = temp_item_array[i]
            if item_num_val == "":
                item_num_val = 0
            try:
                val = float(item_num_val)
                if not val.is_integer() or val < 0:
                    print("Invalid input! Parameter given is either not an integer or is negative")
                    validation_success = False
                    self.success_label.setText("")
                    self.error_label.setText("Invalid Input: " + str(item_num_val) + "\nPlease enter a valid integer")
                    self.error_label.adjustSize()
                    self.error_label.setDisabled(True)
                    break
                else:
                    items_list.append(int(val))
                    self.error_label.setText("")
            except:
                print("Invalid input! Please enter a valid input")
                validation_success = False
                self.success_label.setText("")
                self.error_label.setText("Invalid Input: " + item_num_val + "\nPlease enter a valid integer")
                self.error_label.adjustSize()
                self.error_label.setDisabled(True)

        if len(items_list) > number_of_rows:
            items_list = items_list[0:number_of_rows]
        elif len(items_list) < number_of_rows:
            zeros_to_add = number_of_rows - len(items_list)
            for i in range(0,zeros_to_add):
                items_list.append(0)
        if validation_success == True:
            moves_list = [(x, y) for x in range(0, len(items_list))
                                 for y in range(1, items_list[x] + 1)]
            self.success_label.setText("Items selected (each row is separated by comma): " + str(items_list))
            self.success_label.adjustSize()
            self.success_label.setDisabled(True)
            print("Items list: " + str(items_list))

class GameWindow(QDialog): # NEED TO DO!!!!!
    # Here need to pull in the items list from the previous frame and run the game and output the result
    def __init__(self):
        super(GameWindow, self).__init__()
        loadUi("game.ui", self)

        global number_of_rows
        global items_list
        global moves_list
        global move

        self.moveinput.setPlaceholderText("row num, items")
        self.row_num_label = QLabel(self)
        self.row_num_label.move(150,90)
        self.items_label = QLabel(self)
        self.items_label.move(150,110)
        self.moves_label = QLabel(self)
        self.moves_label.setWordWrap(True)
        self.moves_label.move(150,130)

        self.error_label = QLabel(self)
        self.error_label.setStyleSheet("""color: red;""")
        self.error_label.move(220,250)
        self.success_label = QLabel(self)
        self.success_label.move(220,250)
        self.rem_moves_label = QLabel(self)
        self.rem_moves_label.setWordWrap(True)
        self.rem_moves_label.move(220,270)
        self.game_over_label = QLabel(self)
        self.game_over_label.move(220,290)
        self.board_display_label1 = QLabel(self)
        self.board_display_label1.setWordWrap(True)
        self.board_display_label1.move(220,320)
        self.board_display_label2 = QLabel(self)
        self.board_display_label2.setWordWrap(True)
        self.board_display_label2.move(220,340)
        self.board_display_label3 = QLabel(self)
        self.board_display_label3.setWordWrap(True)
        self.board_display_label3.move(220,360)
        self.board_display_label4 = QLabel(self)
        self.board_display_label4.setWordWrap(True)
        self.board_display_label4.move(220,380)
        self.board_display_label5 = QLabel(self)
        self.board_display_label5.setWordWrap(True)
        self.board_display_label5.move(220,400)
        self.board_display_label6 = QLabel(self)
        self.board_display_label6.setWordWrap(True)
        self.board_display_label6.move(220,420)
        self.board_display_label7 = QLabel(self)
        self.board_display_label7.setWordWrap(True)
        self.board_display_label7.move(220,440)
        self.board_display_label8 = QLabel(self)
        self.board_display_label8.setWordWrap(True)
        self.board_display_label8.move(220,460)
        self.board_display_label9 = QLabel(self)
        self.board_display_label9.setWordWrap(True)
        self.board_display_label9.move(220,480)
        self.board_display_label10 = QLabel(self)
        self.board_display_label10.setWordWrap(True)
        self.board_display_label10.move(220,500)



        self.row_num_label.setText("Number of rows selected: " + str(number_of_rows))
        self.row_num_label.adjustSize()
        self.row_num_label.setDisabled(True)

        self.items_label.setText("Board selected: " + str(items_list))
        self.items_label.adjustSize()
        self.items_label.setDisabled(True)

        self.moves_label.setText("Available moves: " + str(moves_list))
        self.moves_label.adjustSize()
        self.moves_label.setWordWrap(True)
        self.moves_label.setDisabled(True)

        # display board in GUI
        if len(items_list) > 0:
            self.board_display_label1.setText('0 '*(items_list[0] if len(items_list) >= 1 else 0))
            self.board_display_label1.adjustSize()
            self.board_display_label1.setWordWrap(True)
            self.board_display_label1.setDisabled(True)
            self.board_display_label2.setText('1 '*(items_list[1] if len(items_list) >= 2 else 0))
            self.board_display_label2.adjustSize()
            self.board_display_label2.setWordWrap(True)
            self.board_display_label2.setDisabled(True)
            self.board_display_label3.setText('2 '*(items_list[2] if len(items_list) >= 3 else 0))
            self.board_display_label3.adjustSize()
            self.board_display_label3.setWordWrap(True)
            self.board_display_label3.setDisabled(True)
            self.board_display_label4.setText('3 '*(items_list[3] if len(items_list) >= 4 else 0))
            self.board_display_label4.adjustSize()
            self.board_display_label4.setWordWrap(True)
            self.board_display_label4.setDisabled(True)
            self.board_display_label5.setText('4 '*(items_list[4] if len(items_list) >= 5 else 0))
            self.board_display_label5.adjustSize()
            self.board_display_label5.setWordWrap(True)
            self.board_display_label5.setDisabled(True)
            self.board_display_label6.setText('5 '*(items_list[5] if len(items_list) >= 6 else 0))
            self.board_display_label6.adjustSize()
            self.board_display_label6.setWordWrap(True)
            self.board_display_label6.setDisabled(True)
            self.board_display_label7.setText('6 '*(items_list[6] if len(items_list) >= 7 else 0))
            self.board_display_label7.adjustSize()
            self.board_display_label7.setWordWrap(True)
            self.board_display_label7.setDisabled(True)
            self.board_display_label8.setText('7 '*(items_list[7] if len(items_list) >= 8 else 0))
            self.board_display_label8.adjustSize()
            self.board_display_label8.setWordWrap(True)
            self.board_display_label8.setDisabled(True)
            self.board_display_label9.setText('8 '*(items_list[8] if len(items_list) >= 9 else 0))
            self.board_display_label9.adjustSize()
            self.board_display_label9.setWordWrap(True)
            self.board_display_label9.setDisabled(True)
            self.board_display_label10.setText('9 '*(items_list[9] if len(items_list) == 10 else 0))
            self.board_display_label10.adjustSize()
            self.board_display_label10.setWordWrap(True)
            self.board_display_label10.setDisabled(True)

        self.rungame.clicked.connect(self.validate)
        #self.home.clicked.connect(self.gotostartWindow)

    def gotostartWindow(self):
        #self.row_num_label.setText("")
        #self.items_label.setText("")
        #self.moves_label.setText("")
        #self.error_label.setText("")
        #self.success_label.setText("")
        #self.rem_moves_label.setText("")
        #self.game_over_label.setText("")
        startwindow = StartWindow()
        widget.addWidget(startwindow)
        widget.setCurrentIndex(widget.currentIndex() - 3)


    def validate(self):

        global number_of_rows
        global items_list
        global moves_list
        local_move = []
        move_input = self.moveinput.text()
        temp_move_array = move_input.split(",")
        validation_success = True
        if len(temp_move_array) < 2:
            print("Invalid input! Not enough parameters given.")
            validation_success = False
            self.success_label.setText("")
            self.error_label.setText("Invalid Input: " + str(temp_move_array) + "\nPlease enter a valid move")
            self.error_label.adjustSize()
            self.error_label.setDisabled(True)
        else:
            for i in range(0,len(temp_move_array)):
                item_num_val = temp_move_array[i]
                if item_num_val == "":
                    item_num_val = 0
                    print("Invalid input! Blank parameter given")
                    validation_success = False
                    self.success_label.setText("")
                    self.error_label.setText("Invalid Input: " + str(item_num_val) + "\nPlease enter a valid move")
                    self.error_label.adjustSize()
                    self.error_label.setDisabled(True)
                val = float(item_num_val)
                if not val.is_integer() or val < 0:
                    print("Invalid input! Paramter is either not an integer or is negative")
                    validation_success = False
                    self.success_label.setText("")
                    self.error_label.setText("Invalid Input: " + str(item_num_val) + "\nPlease enter a valid move")
                    self.error_label.adjustSize()
                    self.error_label.setDisabled(True)
                    break
                else:
                    local_move.append(int(val))
                    self.error_label.setText("")

            if len(local_move) > 2:
                local_move = local_move[0:2]
            global move
            move = tuple(i for i in local_move)
            # print(move)
            if move not in moves_list:
                print("Invalid input! Move is not in the available moves list")
                validation_success = False
                self.success_label.setText("")
                self.rem_moves_label.setText("")
                self.error_label.setText("Invalid move: " + str(move) + "\nPlease enter a valid move")
                self.error_label.adjustSize()
                self.error_label.setDisabled(True)
            if validation_success == True:
                self.success_label.setText("Move selected: " + str(move))
                self.success_label.adjustSize()
                self.success_label.setDisabled(True)
                print("Move: " + str(move))

                nim = GameOfNim(board = items_list)
                self.moves_label.setText("Available moves: " + str(moves_list))
                self.moves_label.adjustSize()
                self.moves_label.setWordWrap(True)
                self.moves_label.setDisabled(True)
                utility = nim.play_game(query_player, alpha_beta_player)

                self.rem_moves_label.setText("Remaining moves: " + str("None" if len(moves_list) == 0 else moves_list))
                self.rem_moves_label.adjustSize()
                self.rem_moves_label.setWordWrap(True)
                self.rem_moves_label.setDisabled(True)

                if len(moves_list) == 0:
                    if utility < 0:
                        self.game_over_label.setText("You lost! Please try again!")
                        self.game_over_label.setStyleSheet("""color: red;""")
                        self.game_over_label.adjustSize()
                        self.game_over_label.setDisabled(True)
                    elif utility > 0:
                        self.game_over_label.setText("Congratulations! You won!")
                        self.game_over_label.setStyleSheet("""color: green;""")
                        self.game_over_label.adjustSize()
                        self.game_over_label.setDisabled(True)

                # display board in GUI
                # board_display(items_list)
                if len(items_list) > 0:
                    self.board_display_label1.setText('0 '*(items_list[0] if len(items_list) >= 1 else 0))
                    self.board_display_label1.adjustSize()
                    self.board_display_label1.setWordWrap(True)
                    self.board_display_label1.setDisabled(True)
                    self.board_display_label2.setText('1 '*(items_list[1] if len(items_list) >= 2 else 0))
                    self.board_display_label2.adjustSize()
                    self.board_display_label2.setWordWrap(True)
                    self.board_display_label2.setDisabled(True)
                    self.board_display_label3.setText('2 '*(items_list[2] if len(items_list) >= 3 else 0))
                    self.board_display_label3.adjustSize()
                    self.board_display_label3.setWordWrap(True)
                    self.board_display_label3.setDisabled(True)
                    self.board_display_label4.setText('3 '*(items_list[3] if len(items_list) >= 4 else 0))
                    self.board_display_label4.adjustSize()
                    self.board_display_label4.setWordWrap(True)
                    self.board_display_label4.setDisabled(True)
                    self.board_display_label5.setText('4 '*(items_list[4] if len(items_list) >= 5 else 0))
                    self.board_display_label5.adjustSize()
                    self.board_display_label5.setWordWrap(True)
                    self.board_display_label5.setDisabled(True)
                    self.board_display_label6.setText('5 '*(items_list[5] if len(items_list) >= 6 else 0))
                    self.board_display_label6.adjustSize()
                    self.board_display_label6.setWordWrap(True)
                    self.board_display_label6.setDisabled(True)
                    self.board_display_label7.setText('6 '*(items_list[6] if len(items_list) >= 7 else 0))
                    self.board_display_label7.adjustSize()
                    self.board_display_label7.setWordWrap(True)
                    self.board_display_label7.setDisabled(True)
                    self.board_display_label8.setText('7 '*(items_list[7] if len(items_list) >= 8 else 0))
                    self.board_display_label8.adjustSize()
                    self.board_display_label8.setWordWrap(True)
                    self.board_display_label8.setDisabled(True)
                    self.board_display_label9.setText('8 '*(items_list[8] if len(items_list) >= 9 else 0))
                    self.board_display_label9.adjustSize()
                    self.board_display_label9.setWordWrap(True)
                    self.board_display_label9.setDisabled(True)
                    self.board_display_label10.setText('9 '*(items_list[9] if len(items_list) == 10 else 0))
                    self.board_display_label10.adjustSize()
                    self.board_display_label10.setWordWrap(True)
                    self.board_display_label10.setDisabled(True)

# use this to display the board in console
def board_display(board):
    for i in range(0,len(board)):
        print('* '*board[i])

"""Copied over code from games.py and game_of_nim.py, so we can edit freely"""
def alpha_beta_search(state, game):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


# ______________________________________________________________________________
# Players for Games


def query_player(game, state):
    global move
    global moves_list
    """Make a move by querying standard input."""
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    localocal_move = None
    if game.actions(state):
        # print(move)
        if len(move) != 0 and move in moves_list:
            move_string = str(move) #input('Your move? ')
            try:
                localocal_move = eval(move_string)
            except NameError:
                localocal_move = move_string
        else:
            print("Invalid move! Please enter a valid move")
    else:
        print('no legal moves: passing turn to next player')
    return localocal_move

def alpha_beta_player(game, state):
    return alpha_beta_search(state, game)

class Game:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor."""

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print(state)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        global move
        global moves_list

        state = self.initial
        loop_counter = 1
        player = players[0]
        # print(player)
        while loop_counter == 1 and not self.terminal_test(state):
            # print("loop counter: " + str(loop_counter))
            move = player(self, state)
            state = self.result(state, move)
            print(state)
            if self.terminal_test(state):
                self.display(state)
                print("Game has ended ... ")
            # print(player)
            if player == alpha_beta_player:
                loop_counter += 1
            player = players[1]
        move = 0,0
        return self.utility(state, self.to_move(self.initial))

class GameOfNim(Game):

    # let's have a mapping for the players
    names = {"MAX": "Player",
             "MIN": "Computer"}

    def __init__(self, board):
        moves = [(x, y) for x in range(0, len(board))
                 for y in range(1, board[x] + 1)]
        global moves_list
        moves_list = moves
        self.initial = GameState(to_move="MAX", utility=0, board=board, moves=moves)

    def result(self, state, move):
        """Calculate the resulting state from applying given move"""
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()

        # we need to update the other moves in the row as well
        # that is, if we remove x item from a row having y items (x < y), then there are (y - x) items left
        r, n = move # r is row number, n is number of objects
        board[r] -= n
        moves = [(x, y) for x in range(0, len(board))
                 for y in range(1, board[x] + 1)]
        new_state = GameState(to_move=("MAX" if state.to_move == "MIN" else "MIN"),
                  utility=self.compute_utility(board, state.to_move),
                  board=board, moves=moves)
        global moves_list
        moves_list = moves
        global items_list
        items_list = board
        return new_state

    def actions(self, state):
        """Possible actions are picking items from rows that have items
           ranging from 1 to however many items are in the row"""
        return state.moves

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def compute_utility(self, board, player):
        """If there are no more moves
            Then if next to move would have been 'COMPUTER', 'PLAYER' wins so return 1.
            If next to move would have been 'PLAYER', 'COMPUTER' wins so return -1.
            else return 0."""
        utility = 0
        board_empty_after_move = True
        index = 0
        while index < len(board) and board_empty_after_move:
            if board[index] != 0:
                board_empty_after_move = False
                break
            index += 1

        if board_empty_after_move:
            utility = -1 if player == "MIN" else +1
        return utility

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
widget.setWindowTitle("Game of Nim")
startwindow = StartWindow()
widget.addWidget(startwindow)
widget.setFixedHeight(700)
widget.setFixedWidth(600)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting ...")
