ROWS = 'ABCDEFGHI'
COLUMNS = '123456789'


def cross(some_a, some_b):
  """cross product of some a and some b"""
  return [s + t for s in some_a for t in some_b]

CELLS = cross(ROWS, COLUMNS)
# print(CELLS)

ROW_UNITS = [cross(r, COLUMNS) for r in ROWS]
# print(ROW_UNITS)

COLUMN_UNITS = [cross(ROWS, c) for c in COLUMNS]
# print(COLUMN_UNITS)

SQUARE_UNITS = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
# print(SQUARE_UNITS)

UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS
# print(UNITLIST)

UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in CELLS)
# print(UNITS)

PEERS = dict((s, set(sum(UNITS[s], [])) - set([s])) for s in CELLS)


def display(values):
  """
  Display the values as a 2-D grid.
  Input: The sudoku in dictionary form
  Output: None
  """
  width = 1 + max(len(values[s]) for s in CELLS)
  line = '+'.join(['-' * (width * 3)] * 3)
  for r in ROWS:
    print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                  for c in COLUMNS))
    if r in 'CF':
      print(line)
  return

# WARNING! We've modified this function to return '123456789' instead of '.' for boxes with no value.
# Look at the explanation above in the text.


def grid_values(grid):
  """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

  Args:
      grid: Sudoku grid in string form, 81 characters long
  Returns:
      Sudoku grid in dictionary form:
      - keys: Box labels, e.g. 'A1'
      - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
  """
  values = []
  all_digits = '123456789'
  for c in grid:
    if c == '.':
      values.append(all_digits)
    elif c in all_digits:
      values.append(c)
  assert len(values) == 81
  return dict(zip(CELLS, values))
