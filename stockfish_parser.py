import os
import subprocess as sp


class Stockfish:
    # Integrates Stockfish engine into python
    def __init__(self, path, depth):
        '''
        :param path: STR .relative path to the stockfish engine executable
        :param depth: INT
        '''
        self.path = path
        self._conn = sp.Popen(
            path,
            universal_newlines=True,
            stdin=sp.PIPE,
            stdout=sp.PIPE)
        self.depth = str(depth)
        default_param = {
            'Write Debug Log': 'false',
            'Contempt': 0,
            'Min Split Depth': 0,
            'Threads': 4,
            'Ponder': 'false',
            'Hash': 16,
            'MultiPV': 1,
            'Skill Level': 1,
            'Move Overhead': 30,
            'Minimum Thinking Time': 20,
            'Slow Mover': 80,
            'UCI_Chess960': 'false'
        }
        for name, value in default_param.items():
            # set the default parameters
            self.set_option(name, value)
        self._start_new_game()

    def _start_new_game(self):
        self._isready()

    def set_depth(self, value):
        '''
        Setter for depth
        :param value: INT. New depth value
        '''
        self.depth = str(value)

    def _push(self, command):
        '''
        execute a command in the Stockfish terminal
        :param command: STR. Com,and to be execute
        '''
        self._conn.stdin.write(command + '\n')
        self._conn.stdin.flush()

    def set_option(self, option_name, value):
        '''
        Set stockfish parameters
        :param option_name: STR. Name of option from the list in default_param
        :param value: INT or BOOL
        '''
        self._push(f'setoption name {option_name} value {str(value)}')
        stdout = self._isready()  # wait for the engine to finish execution

    def set_threads_used(self, value):
        '''
        Set the amount of CPU threads to be used. More threads= faster execution
        :param value: INT
        '''
        self.set_option("Threads", value)

    def _isready(self):  # wait for the engine to finish executing. Deal with synchronisation
        self._push('isready')
        while True: # wait for program to be ready
            text = self._conn.stdout.readline().strip()
            if text == 'readyok':
                return text

    def set_fen_position(self, fen_position):
        '''
        Set fen
        :param fen_position:STR
        '''
        self._push(f'position fen {fen_position}')

    def set_skill_level(self, value):
        '''
        :param value: STR
        '''
        if value > 20:
            value = 20
        self.set_option("Skill Level", value)

    def get_best_move(self):
        # Get best move with current position and the depth
        self._push(f'go depth {self.depth}')
        lines = []
        while True:
            line = self._conn.stdout.readline().strip()
            lines.append(line)
            if line.split(" ")[0] == "bestmove":
                return line.split(" ")[1]
            elif line == "":  # if the tree couldn't be constructed to the desired depth because it reached mate
                split_line = lines[-2].split(" ")  # return the move from the maximum depth it could go to
                return split_line[19]

    def __del__(self):  # when the object is deleted, close the connection with the terminal
        self._conn.kill()


def init_stockfish(depth):
    '''
    Initialise Stockfish object with the appropriate path
    :param depth: INT
    :return: Stockfish object
    '''
    cwd = os.getcwd()
    exe_name = "stockfish_10_x64.exe"
    if len(cwd.split("\\")) == 3 or cwd.split("\\")[-1]=="Source":
        os.chdir(r"stockfish")
    stockfish = Stockfish(exe_name, depth)
    return stockfish

def get_best_move(stockfish, fen):
    '''
    :param stockfish: Stockfish object
    :param fen: STR
    :return: STR
    '''
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move
