
assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#-----adding diagnol constraint -------#
diagnol_units = []
diag_i = 1
l1 = []
l2 = []
for row in rows:
    l1.append(row+str(diag_i))
    l2.append(row+str(10-diag_i))
    diag_i += 1
diagnol_units.append(l1)
diagnol_units.append(l2)

#-----------------#
unitlist = row_units + column_units + square_units + diagnol_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    twins_dict = {}
    # append naked-twins to dictionary
    # Find all instances of naked twins, if yes add them to dictionary
    for value in values:
        if len(values[value]) ==2:
            if values[value] in twins_dict:
                twins_dict[values[value]].append(value)
            else:
                twins_dict[values[value]] = [value]

    # Eliminate the naked twins as possibilities for their peers
    for entry in twins_dict: #iterate through all the entries of twins dictionary
        if len(twins_dict[entry]) >= 2:
            pairs = twins_dict[entry]
            for pair in pairs:  #iterate through the list of boxes with a twin value
                for pairtemp in pairs: #iterate through the list of boxes with a twin value
                    if pairtemp == pair:
                        continue
                    else: 
                        if pairtemp in peers[pair]:#this logic will check if two boxes are peers or not.
                            for unit in unitlist: #this logic will check if two boxes are from same unit.
                                if pairtemp in unit and pair in unit: #if both boxes belong to a particular unit
                                    for unit_entry in unit: #Eliminate naked twins from peers belonging to a particular unit.
                                        if unit_entry==pairtemp or unit_entry==pair:
                                            continue
                                        else:
                                            for e in entry:
                                                values[unit_entry] = values[unit_entry].replace(e,'')
                                                assign_value(values,unit_entry,values[unit_entry])
    return values
    
def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    boxes_dict = {}
    i = 0
    digits = '123456789'
    for s in grid:
        if i < len(boxes):
            if s == '.':
                boxes_dict[boxes[i]]=digits
            else:
                boxes_dict[boxes[i]]=s
        i += 1
    return boxes_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    dictkeys = []
    for key in values:
        i = values[key]
        if len(i) == 1:
            dictkeys.append(key)
    for key in dictkeys:
        i = values[key]
        for item in peers[key]:
            if i in values[item]:
                values[item] = values[item].replace(i,'')
                assign_value(values,item,values[item])
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()  # note: do not modify original values
    # TODO: Implement only choice strategy here
    
    for value in values:
        if len(values[value]) > 1:
            for entry in values[value]:
                entryvar = False
                for unit in units[value]:
                    flagvar = True
                    for box in unit:
                        if box==value:
                            continue
                        if entry in values[box]:
                            flagvar = False
                            break
                    if flagvar:
                        new_values[value]=entry
                        entryvar = True
                        break
                if entryvar:
                    break
    for val in new_values:
        assign_value(values,val,new_values[val])
    return values 

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    #display(values)
    values = reduce_puzzle(values)
    if values is False:
        return False
    if all(len(values[s]) ==1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s])>1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    #return new_sudoku

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return(search(grid_values(grid)))


def main():
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


if __name__ == '__main__':
    main()
    