import memory_graph as mg
import copy
import random 
random.seed(0)  # use same random numbers each run

EMPTY_TILE = '█'
RANDOM_MOVES = 20  # measure of difficulty

def main():
    goal = Sliding_Puzzle(f"1,2,3;4,5,6;7,8,{EMPTY_TILE}")
    print('=== goal:')
    print(goal)
    board = goal.copy()
    board.random_move(RANDOM_MOVES) # make random moves to shuffle the board
    print('=== starting board:')
    print(board)
    solution, visited_boards = solve(board, goal)
    solution_path = get_solution_path(solution, visited_boards)
    
    mg.config.type_to_slicer[id(solution_path)] = mg.Slicer() # show full list
    print('===== solution_path:')
    for s in solution_path:
        print(s)
        print()
    print('SOLVED!')
        
    print('Now show all visited boards, this can get too big.')
    mg.config.type_to_slicer[id(visited_boards)] = mg.Slicer() # show full dict
    return solution_path

def solve(board, goal):
    """ Solve the sliding puzzle using breadth-first search. """
    visited_boards = {repr(board): None}
    if board == goal:
        return board, visited_boards
    generation = [board]
    generation_count = 0
    while generation:
        print(f"Generation {generation_count}: {len(generation)} boards")
        next_generation = []
        for board in generation:
            board_repr = repr(board)
            for child in board.get_childeren():
                child_repr = repr(child)
                if child_repr not in visited_boards:
                    visited_boards[child_repr] = board_repr
                    next_generation.append(child)
                    if child == goal:
                        return child, visited_boards
        generation = next_generation
        generation_count += 1
    print("No solution found.")
    return None, visited_boards

def get_solution_path(solution, visited_boards):
    """ Reconstruct the path from the initial board to the solution. """
    if solution is None:
        print("No solution exists.")
        return
    path = []
    current = repr(solution)
    while True:
        if not current:
            break
        path.append(Sliding_Puzzle(current))
        current = visited_boards[current]
    path.reverse()
    return path

class Sliding_Puzzle:

    def __init__(self, board):
        """ Create a sliding puzzle from a string representation, for example: 
            "1,2,3;4,5,6;7,8,#" where '#' represents the empty space.
        """
        self.tiles = [row.split(',') for row in board.split(';')]
        self.rows = len(self.tiles)
        self.cols = len(self.tiles[0]) if self.rows > 0 else 0

    def __repr__(self):
        """ Provide a unique string representation of the board."""
        return ';'.join([','.join(row) for row in self.tiles])

    def __str__(self):
        """ Provide a human-readable string representation of the board."""
        return '\n'.join([' '.join(row) for row in self.tiles])
    
    def get_empty_position(self):
        """ Return the (row, col) of the empty space (EMPTY_TILE). """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tiles[r][c] == EMPTY_TILE:
                    return (r, c)
        return None
    
    def copy(self):
        """ Return a deep copy of the current board. """
        return copy.deepcopy(self)

    def get_childeren(self):
        """ Generate all possible child boards from the current board by sliding
            each possible tile into the empty space.
        """
        children = []
        empty_r, empty_c = self.get_empty_position()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            new_r, new_c = empty_r + dr, empty_c + dc
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                child = self.copy()
                ct = child.tiles
                ct[empty_r][empty_c], ct[new_r][new_c] = ct[new_r][new_c], ct[empty_r][empty_c]
                children.append(child)
        return children

    def __eq__(self, other):
        """ Check if two boards are equal. """
        return self.tiles == other.tiles
    
    def random_move(self, moves=100):
        """ Perform a series of random valid moves to shuffle the board. """
        for _ in range(moves):
            self.tiles = random.choice(self.get_childeren()).tiles

# show Sliding_Puzzle instance as magenta table
mg.config.type_to_color[Sliding_Puzzle] = 'magenta'
mg.config.type_to_node[Sliding_Puzzle] = lambda s : mg.Node_Table(s, s.tiles)

if __name__ == "__main__":
    solution_path = main()
