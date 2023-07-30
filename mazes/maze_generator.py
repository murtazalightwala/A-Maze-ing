from colorama import init, Fore
from random import choice
import time
import os


class PrimsMaze:
    def __init__(self, size: tuple):
        self.size = size 
        height, width = size
        self.grid = []
        for i in range(0, height):
        	line = []
        	for j in range(0, width):
        		line.append("u")
        	self.grid.append(line)

    def pp_maze(self):
        init()
        os.system("clear")
        m = self.grid
        for i in range(0, len(m)):
            for j in range(0, len(m[i])):
                if m[i][j] == 'u':
                    print(Fore.BLUE, f'{m[i][j]}', end="")
                elif m[i][j] == 'c':
                    print(Fore.GREEN, f'{m[i][j]}', end="")
                else:
                    print(Fore.RED, f'{m[i][j]}', end="")
            print('\n')

    def get_random_start_cell(self):
        height = self.size[0]
        width = self.size[1]
        starting_height = choice(range(1, height-1))
        starting_width = choice(range(1, width -1))
        return starting_height, starting_width

    @staticmethod
    def add_sides_to_wall(wall: list, loc: tuple, maze: list):
        if maze[loc[0] - 1][loc[1]] != "c":
            wall.append((loc[0]-1, loc[1]))
            maze[loc[0] - 1][loc[1]] = "w"
        if maze[loc[0]][loc[1] - 1] != "c":
            wall.append((loc[0], loc[1]-1))
            maze[loc[0]][loc[1] - 1] = "w"
        if maze[loc[0] + 1][loc[1]] != "c":
            wall.append((loc[0]+1, loc[1]))
            maze[loc[0] + 1][loc[1]] = "w"
        if maze[loc[0]][loc[1] + 1] != "c":
            wall.append((loc[0], loc[1]+1))
            maze[loc[0]][loc[1] + 1] = "w"
        wall = list(set(wall))

    @staticmethod
    def mark_neighbours_as_walls(maze:list, loc: tuple):
        maze[loc[0] - 1, loc[1]] = "w"
        maze[loc[0], loc[1] - 1] = "w"
        maze[loc[0] + 1, loc[1]] = "w"
        maze[loc[0], loc[1] + 1] = "w"

    @staticmethod
    def check_if_border(size: tuple, loc:tuple):
        height, width = size
        h, w = loc
        if h <= 0 or h >= height-1 or w <= 0 or w>= width -1:
            return False
        return True

    @staticmethod
    def delete_wall(walls: list, loc: tuple):
        for wall in walls:
            if (wall[0], wall[1]) == loc:
                walls.remove(wall)
            
        

    def get_surrounding_cell_count(self, loc:tuple, type = "c"):
        count = 0
        h, w = loc
        if self.grid[h - 1][w] == type:
            count += 1
        if self.grid[h + 1][w] == type:
            count += 1
        if self.grid[h][w - 1] == type:
            count += 1
        if self.grid[h -1][w + 1] == type:
            count += 1
        return count
    
    def check_if_exactly_one_visited(self, maze:list, loc:tuple, size: tuple):
        pass


    def mark_unvisited_as_walls(self):
        height, width = self.size
        for i in range(0, height):
        	for j in range(0, width):
        		if (self.grid[i][j] == 'u'):
        			self.grid[i][j] = 'w' 

    def mark_entrance_and_exit(self):
        height, width = self.size
        for i in range(0, width):
            if self.grid[1][i] == "c":
                self.grid[0][i] = "c"
                self.entrance = (0,i)
                break
        for i in range(0, width):
            if self.grid[height -2][i] == "c":
                self.grid[height -1][i] = "c"
                self.exit = (height - 1, i)
                break
            
    def build_maze(self):
        sh, sw = self.get_random_start_cell()
        self.grid[sh][sw] = "c"
        walls = []
        __class__.add_sides_to_wall(walls, (sh, sw), self.grid)
        while walls:
            rand_wall = choice(walls)
            r_h, r_w = rand_wall
            
            if r_w != 0:
                if  self.grid[r_h][r_w - 1]  == "u" and self.grid[r_h][r_w + 1] == "c":
                    if self.get_surrounding_cell_count(rand_wall) < 2:
                        self.grid[r_h][r_w] = "c"
                        __class__.add_sides_to_wall(walls, rand_wall, self.grid)
                    __class__.delete_wall(walls, rand_wall)
                    continue
                        
            if r_w != self.size[1] - 1:
                if  self.grid[r_h][r_w - 1]  == "c" and self.grid[r_h][r_w + 1] == "u":
                    if self.get_surrounding_cell_count(rand_wall) < 2:
                        self.grid[r_h][r_w] = "c"
                        __class__.add_sides_to_wall(walls, rand_wall, self.grid)
                    __class__.delete_wall(walls, rand_wall)
                    continue
                        
            if r_h != 0:
                if  self.grid[r_h - 1][r_w]  == "u" and self.grid[r_h + 1][r_w] == "c":
                    if self.get_surrounding_cell_count(rand_wall) < 2:
                        self.grid[r_h][r_w] = "c"
                        __class__.add_sides_to_wall(walls, rand_wall, self.grid)
                    __class__.delete_wall(walls, rand_wall)
                    continue
                        
            if r_h != self.size[0] - 1:
                if  self.grid[r_h + 1][r_w]  == "u" and self.grid[r_h - 1][r_w] == "c":
                    if self.get_surrounding_cell_count(rand_wall) < 2:
                        self.grid[r_h][r_w] = "c"
                        __class__.add_sides_to_wall(walls, rand_wall, self.grid)
                    __class__.delete_wall(walls, rand_wall)
                    continue

            __class__.delete_wall(walls, rand_wall)
        self.mark_unvisited_as_walls()
        self.mark_entrance_and_exit()
        
    
import random

class DFSCell:
    """A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.

    """

    # A wall separates a pair of cells in the N-S or W-E directions.
    wall_pairs = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        """Initialize the cell at (x,y). At first it is surrounded by walls."""

        self.x, self.y = x, y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.is_correct_path = False

    def has_all_walls(self):
        """Does this cell still have all its walls?"""

        return all(self.walls.values())

    def knock_down_wall(self, other, wall):
        """Knock down the wall between cells self and other."""

        self.walls[wall] = False
        other.walls[DFSCell.wall_pairs[wall]] = False

    def set_wall(self, wall, val = False):
        self.walls[wall] = val


class DFSMaze:
    """A Maze, represented as a grid of cells."""

    def __init__(self, size: tuple, ix=0, iy=0):
        """Initialize the maze grid.
        The maze consists of nx x ny cells and will be constructed starting
        at the cell indexed at (ix, iy).

        """

        self.nx, self.ny = size
        self.ix, self.iy = ix, iy
        ex, ey = size
        self.ex, self.ey = ex - 1, ey - 1
        print(self.ex, self.ey)
        self.maze_map = [[DFSCell(x, y) for y in range(self.ny)] for x in range(self.nx)]
        self.is_solved = False
        self.solution_path = [(0, 0)]
        self.build_maze()
        self.is_solved = self.solve_maze(self.solution_path)

    def cell_at(self, x, y):
        """Return the Cell object at (x,y)."""

        return self.maze_map[x][y]

    @classmethod
    def from_serializable(cls, size: tuple, data):
        maze_object = cls((size))
        for x, column in enumerate(data):
            for y, cell in enumerate(column):
                for dir, val in cell.items():
                    maze_object.maze_map[x][y].set_wall(dir, val)
        return maze_object
        

    def to_serializable(self):
        _output = []
        for row in self.maze_map:
            cell_row = []
            for cell in row:
                cell_row.append(cell.walls)
            _output.append(cell_row)
        return _output
                

    def __str__(self):
        """Return a (crude) string representation of the maze."""

        maze_rows = ['-' * self.nx * 2]
        for y in range(self.ny):
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['E']:
                    maze_row.append(' |')
                else:
                    maze_row.append('  ')
            maze_rows.append(''.join(maze_row))
            maze_row = ['|']
            for x in range(self.nx):
                if self.maze_map[x][y].walls['S']:
                    maze_row.append('-+')
                else:
                    maze_row.append(' +')
            maze_rows.append(''.join(maze_row))
        return '\n'.join(maze_rows)

    def write_svg(self, filename, with_solution = False):
        """Write an SVG image of the maze to filename."""

        aspect_ratio = self.nx / self.ny
        # Pad the maze all around by this amount.
        padding = 10
        # Height and width of the maze image (excluding padding), in pixels
        height = 500
        width = int(height * aspect_ratio)
        # Scaling factors mapping maze coordinates to image coordinates
        scy, scx = height / self.ny, width / self.nx

        def write_wall(ww_f, ww_x1, ww_y1, ww_x2, ww_y2):
            """Write a single wall to the SVG image file handle f."""

            print('<line x1="{}" y1="{}" x2="{}" y2="{}"/>'
                  .format(ww_x1, ww_y1, ww_x2, ww_y2), file=ww_f)

        # Write the SVG image file for maze
        with open(filename, 'w') as f:
            # SVG preamble and styles.
            print('<?xml version="1.0" encoding="utf-8"?>', file=f)
            print('<svg xmlns="http://www.w3.org/2000/svg"', file=f)
            print('    xmlns:xlink="http://www.w3.org/1999/xlink"', file=f)
            print('    width="{:d}" height="{:d}" viewBox="{} {} {} {}">'
                  .format(width + 2 * padding, height + 2 * padding,
                          -padding, -padding, width + 2 * padding, height + 2 * padding),
                  file=f)
            print('<defs>\n<style type="text/css"><![CDATA[', file=f)
            print('line {', file=f)
            print('    stroke: #000000;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 5;\n}', file=f)
            print('#solution {', file=f)
            print('    stroke: #7CFC00;\n    stroke-linecap: square;', file=f)
            print('    stroke-width: 2;\n}', file=f)
            print(']]></style>', file=f)
            print('</defs>', file=f)
            # Draw the "South" and "East" walls of each cell, if present (these
            # are the "North" and "West" walls of a neighbouring cell in
            # general, of course).
            for x in range(self.nx):
                for y in range(self.ny):
                    if self.cell_at(x, y).walls['S']:
                        x1, y1, x2, y2 = x * scx, (y + 1) * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
                    if self.cell_at(x, y).walls['E']:
                        x1, y1, x2, y2 = (x + 1) * scx, y * scy, (x + 1) * scx, (y + 1) * scy
                        write_wall(f, x1, y1, x2, y2)
            # Draw the North and West maze border, which won't have been drawn
            # by the procedure above.
            if self.cell_at(0, 0).walls["N"]:
                print('<line x1="0" y1="0" x2="{}" y2="0"/>'.format(width), file=f)
            else:
                print('<line x1="{}" y1="0" x2="{}" y2="0"/>'.format(scx ,width), file=f)
            if self.cell_at(0, 0).walls["W"]:
                print('<line x1="0" y1="0" x2="0" y2="{}"/>'.format(height), file=f)
            else:
                print('<line x1="0" y1="{}" x2="0" y2="{}"/>'.format(scy, height), file=f)
            if with_solution and self.is_solved:
                prev_point = self.solution_path[0]
                for item in self.solution_path[1:]:
                    x1, y1 = prev_point
                    x1, y1 = scx*(0.5 + x1), scy*(0.5 + y1)
                    x2, y2 = item
                    x2, y2 = scx*(0.5 + x2), scy*(0.5 + y2)
                    print('<line id="solution" x1="{}" y1="{}" x2="{}" y2="{}"/>'.format(x1, y1, x2, y2), file=f)
                    prev_point = item
            print('</svg>', file=f)
             

    def find_valid_neighbours(self, cell):
        """Return a list of unvisited neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))
        return neighbours
    
    def find_path_neighbours(self, cell):
        """Return a list of possible neighbours to cell."""

        delta = [('W', (-1, 0)),
                 ('E', (1, 0)),
                 ('S', (0, 1)),
                 ('N', (0, -1))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.cell_at(x2, y2)
                if not cell.walls[direction]:
                    neighbours.append((x2, y2))
        return neighbours

    def build_maze(self):
        
        # Total number of cells.
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # We've reached a dead end: backtrack.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.knock_down_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1
        #set entry and exit
        self.cell_at(self.ix, self.iy).set_wall("N", False)
        self.cell_at(self.ex, self.ey).set_wall("S", False)

    def solve_maze(self, solution_path = [(0, 0)]):
        current_cell = solution_path[-1]
        if current_cell == (self.ex, self.ey):
            return True
        for neighbour in self.find_path_neighbours(self.cell_at(*current_cell)):
            if neighbour in solution_path:
                continue
            solution_path.append(neighbour)
            if self.solve_maze(solution_path):
                return True
            solution_path.pop()
            
        
        
           
        
    
                        
                            
                            
            
        
        
        
