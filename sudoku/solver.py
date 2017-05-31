"""A solver for sudoku puzzles"""
from utils import (CELLS, COLUMN_UNITS, PEERS, ROW_UNITS, SQUARE_UNITS, UNITS,
                   display)


def map_to_possibles(value):
  if value == '.':
    return '123456789'
  else:
    return value


def grid_values(grid):
  """Convert grid string into {<box>: <value>} dict with '.' value for empties.

  Args:
      grid: Sudoku grid in string form, 81 characters long
  Returns:
      Sudoku grid in dictionary form:
      - keys: Box labels, e.g. 'A1'
      - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
  """
  return dict(zip(CELLS, ["123456789" if c == '.' else c for c in grid]))


def eliminate(values):
  """Eliminate values from peers of each box with a single value.

  Go through all the boxes, and whenever there is a box with a single value,
  eliminate this value from the set of values of all its peers.

  Args:
      values: Sudoku in dictionary form.
  Returns:
      Resulting Sudoku in dictionary form after eliminating values.
  """
  for key, value in values.items():
    if (len(value) == 1):
      for peer in PEERS[key]:
        if (len(values[peer]) > 1):
          values[peer] = values[peer].replace(value, "")
  return values


def only_choice(values):
  """Finalize all values that are the only choice for a unit.

  Go through all the units, and whenever there is a unit with a value
  that only fits in one box, assign the value to this box.

  Input: Sudoku in dictionary form.
  Output: Resulting Sudoku in dictionary form after filling in only choices.
  """
  # TODO: Improve solution
  # e.g. iterate over units, digits and filter by occurence of digit
  # if only on element is filtered => only choice is found
  for key, value in values.items():
    if len(value) > 1:
      for possible_value in value:
        # print("check for key:value:possible_value %s:%s:%s" %
        #       (key, value, possible_value))
        for units in UNITS[key]:
          # print("units for key: %s:%s" % (key, units))
          found = False
          for cell in units:
            if cell != key and possible_value in values[cell]:
              # print("found possible_value:cell %s:%s" %
              #       (possible_value, cell))
              found = True
              break
          if not found:
            # print("not found key:possible_value %s:%s" % (key, possible_value))
            values[key] = possible_value
            break
  return values


def reduce_puzzle(values):
  """
  goes through eliminate and only_choice loops until
  a solution is found or no improvement was made

  Input: Sudoku in dictionary form.
  Output: Resulting Sudoku in dictionary form either
  as a solution or best effort constraint propagation.
  """
  stalled = False
  while not stalled:
        # Check how many boxes have a determined value
    solved_values_before = len(
        [cell for cell in values.keys() if len(values[cell]) == 1])

    # Your code here: Use the Eliminate Strategy
    values = eliminate(values)
    # Your code here: Use the Only Choice Strategy
    values = only_choice(values)
    # Check how many boxes have a determined value, to compare
    solved_values_after = len(
        [cell for cell in values.keys() if len(values[cell]) == 1])
    # If no new values were added, stop the loop.
    stalled = solved_values_before == solved_values_after
    # Sanity check, return False if there is a box with zero available values:
    if len([cell for cell in values.keys() if len(values[cell]) == 0]):
      return False
  return values


def search(values):
  """Using depth-first search and propagation, create a search tree and solve the sudoku."""
  # First, reduce the puzzle using the previous function
  values = reduce_puzzle(values)
  if values is False:
    return False ## Failed earlier
  if all(len(values[s]) == 1 for s in CELLS):
    return values ## Solved!
  # Choose one of the unfilled squares with the fewest possibilities
  n,s = min((len(values[s]), s) for s in CELLS if len(values[s]) > 1)
  # Now use recurrence to solve each one of the resulting sudokus, and
  for value in values[s]:
    new_sudoku = values.copy()
    new_sudoku[s] = value
    attempt = search(new_sudoku)
    if attempt:
        return attempt

print("*")
display(grid_values(
    '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))

print("*")
display(eliminate(grid_values(
    '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))
print("*")

display(only_choice(eliminate(grid_values(
    '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))))
print("*")

display(reduce_puzzle(grid_values(
    '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..')))

print("*")
display(reduce_puzzle(grid_values(
    '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))

print("*")
display(search(grid_values(
    '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')))
