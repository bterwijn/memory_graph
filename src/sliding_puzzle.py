import memory_graph as mg
import copy
import random 

def main():
    goal = Sliding_Puzzle("1,2,3;4,5,6;7,8,#")
    print('=== goal:')
    print(goal)
    board = goal.copy()
    board.random_move(40) # make random moves to shuffle the board
    print('=== starting board:')
    print(board)
    solution, closed_dict = solve(board, goal)
    solution_path = get_solution_path(solution, closed_dict)
    print('===== solution_path:')
    for s in solution_path:
        print(s)
        print()
    print('the end')

def solve(board, goal):
    """ Solve the sliding puzzle using breadth-first search. """
    closed_dict = {repr(board): None}
    if board == goal:
        return board, closed_dict
    generation = [board]
    generation_count = 0
    while True:
        print(f"Generation {generation_count}: {len(generation)} states")
        next_generation = []
        for board in generation:
            board_repr = repr(board)
            for child in board.get_childeren():
                child_repr = repr(child)
                if child_repr not in closed_dict:
                    closed_dict[child_repr] = board_repr
                    next_generation.append(child)
                    if child == goal:
                        return child, closed_dict
        generation = next_generation
        generation_count += 1
        if not generation:
            print("No solution found.")
            return None, closed_dict

def get_solution_path(solution, closed_dict):
    """ Reconstruct the path from the initial state to the solution. """
    if solution is None:
        print("No solution exists.")
        return
    path = []
    current = repr(solution)
    while True:
        if not current:
            break
        path.append(Sliding_Puzzle(current))
        current = closed_dict[current]
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
        """ Provide a unique string representation of the board state."""
        return ';'.join([','.join(row) for row in self.tiles])

    def __str__(self):
        """ Provide a human-readable string representation of the board."""
        return '\n'.join([' '.join(row) for row in self.tiles])
    
    def get_empty_position(self):
        """ Return the (row, col) of the empty space ('#'). """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.tiles[r][c] == '#':
                    return (r, c)
        return None
    
    def copy(self):
        """ Return a deep copy of the current board state. """
        return copy.deepcopy(self)

    def get_childeren(self):
        """ Generate all possible board states from the current state by sliding 
            each possible tile into the empty space. 
        """
        children = []
        empty_r, empty_c = self.get_empty_position()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for dr, dc in directions:
            new_r, new_c = empty_r + dr, empty_c + dc
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                child = self.copy()
                cb = child.tiles
                cb[empty_r][empty_c], cb[new_r][new_c] = cb[new_r][new_c], cb[empty_r][empty_c]
                children.append(child)
        return children

    def __eq__(self, other):
        """ Check if two board states are equal. """
        return self.tiles == other.tiles
    
    def random_move(self, moves=100):
        """ Perform a series of random valid moves to shuffle the board. """
        for _ in range(moves):
            self.tiles = random.choice(self.get_childeren()).tiles

# show Sliding_Puzzle instances as magenta tables
mg.config.type_to_color[Sliding_Puzzle] = 'magenta'
mg.config.type_to_node[Sliding_Puzzle] = lambda s : mg.Node_Table(s, s.tiles)

if __name__ == "__main__":
    main()