**RAnalysis**
-------------

A python tools to display / plot data from csv files.

![RAnalaysis](ranalysis.jpg "RAnalaysis")

-------------
### Dependencies

Install Python 3.7+ and matplotlib library.

### Data format

| Variable 1 | Variable 2 | Variable 3 | Variable 4 | ... |
|------------|------------|------------|------------|-----|
| unit       | unit       | unit       | unit       | ... |
| value      | value      | value      | value      | ... |
| value      | value      | value      | value      | ... |
| ...        | ...        | ...        | ...        | ... |

*Note*: By default the delimiter of the csv column is ";" but you can use anything you want.
It is important to notice the content of the line in the csv file:

- First line : Name of the variable (string)
- Second line (optional) : Unit of the variable (string) 
- Other lines : Value of the variable (int or float)

### Standalone

#### GUI

Clone the repository or download a zip file from Gitlab, go to the folder and simply run the following command in the *cmd* (Windows) or *terminal* (Linux / MacOs):

	python ./ranalysis/run.py -gui

#### CLI

Clone the repository or download a zip file from Gitlab, go to the folder and simply run one of the following command in the *cmd* (Windows) or *terminal* (Linux / MacOs):
    
    # Display variable x and variable y in a plot
	python run.py -f <path_to_csv_file> -x <x_variable_name> -y <y_variable_name>
	# Display variable x and variables y1, y2, ...  in a plot
	python run.py -f <path_to_csv_file> -x <x_variable_name> -my <y_variable_name1,y_variable_name2>
	# Display usage / help
	python .run.py -h

### Library

#### Generate the library

Clone the repository or download a zip file from Gitlab, go to the folder and simply run the following command in the *cmd* (Windows) or *terminal* (Linux / MacOs):

    # Build RAnalysis source distribution package
    python setup.py sdist
    # Build RAnalysis binary distribution package
    python setup.py bdist
    # Generate RAnalysis pydoc
    pydoc -w <name>

#### Install the library

After generating binary distribution package, copy the content of the zip file in your *site-packages* folder (it can be found in the *lib* Python folder).

#### Use the library (How to ?)

##### Read CSV file

##### Create Plot object

##### Plot data

