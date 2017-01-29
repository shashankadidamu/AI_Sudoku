# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: If there are two boxes with same two possible values, we go over all the boxes in their same unit, and remove the values.
I first created a dictionary to store naked twins values, then tried to see to which unit the two boxes belong to. After getting to know the unit , iterated through the boxes present in the unit and updated the values. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Add new unit containing diagnol boxes to existing row, column and 3*3 units.
In the normal sudoku solution, code was checking 3 conditions, each row, each column, and each of the 9 principal 3x3 subsquares should contain all of the digits from 1 to 9. So, all the possible combinations of units were stored and elimination/only choice/naked twins/search were taking these units into consideration. In the case of diagonal sudoku, we have to make sure that among the two main diagonals, the numbers 1 to 9 should all appear exactly once. So, I added a new unit called diagonal_units that had the diagnol box names in the form a list. By doing this we are making sure that the functions are taking this condition into consideration as well.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.