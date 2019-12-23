import pytest

from day20.puzzle import Maze, Point, bfs

MAZE_1 = '''         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       '''.split('\n')

MAZE_2 = '''                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               '''.split('\n')


def test_maze_parser():
    maze = Maze(MAZE_1)
    assert len(maze.tiles) == 47
    assert maze.entry == Point(9, 2)
    assert maze.exit == Point(13, 16)
    assert maze.tiles[Point(9, 6)]['to'] == Point(2, 8)
    assert maze.tiles[Point(9, 6)]['door'] == 'BC'
    assert maze.tiles[Point(2, 8)]['to'] == Point(9, 6)
    assert maze.tiles[Point(2, 8)]['door'] == 'BC'

    assert maze.tiles[Point(6, 10)]['to'] == Point(2, 13)
    assert maze.tiles[Point(6, 10)]['door'] == 'DE'
    assert maze.tiles[Point(2, 13)]['to'] == Point(6, 10)
    assert maze.tiles[Point(2, 13)]['door'] == 'DE'

    assert maze.tiles[Point(11, 12)]['to'] == Point(2, 15)
    assert maze.tiles[Point(11, 12)]['door'] == 'FG'
    assert maze.tiles[Point(2, 15)]['to'] == Point(11, 12)
    assert maze.tiles[Point(2, 15)]['door'] == 'FG'


@pytest.mark.parametrize('maze, result', [
    (MAZE_1, 23),
    (MAZE_2, 58),
])
def test_bfs(maze, result):
    assert bfs(Maze(maze)) == result
