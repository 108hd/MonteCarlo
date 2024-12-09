# Metadata
Monte Carlo is a Python package for creating and rolling dice in various permutations. The module allows the user to select the number of faces on each die, the number of die, the weight of each die, and the number of die rolls, while the program will show and analyze the output of such activities.  

Monte Carlo contains a Dice module, a Game module, and an Analyzer module.  The Dice module takes an array of faces, which can be either numeric or strings, and each is assigned the same weight of 1.  The weight of any of the faces can be changed and then the list of die is sent to the Game module, where the dice are roled and the results are returned in a wide or narrow dataframe.  The Analyzer module determines the total number of jackpots, counts how many times each face is rolled and in what order, counts the order independent combinations of faces rolled (i.e. a roll of 1-2-3 would be counted as the same as a roll of 3-2-1), and counts the order-dependent combinations of faces (i.e. a roll of 1-2-3 would counted as different from a roll of 3-2-1).  

## Developer
Seth Bitney (wkr8bh)


# Synopsis 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Monte Carlo.

```bash
pip install Monte_Carlo_Module
```

## Usage

```python

# create dice faces, H and T
name_of_list_of_faces = MonteCarlo.np.array(["H","T"])

#create a fair coin
faircoin = MonteCarlo.Dice(name_of_list_of_faces)

#create a weighted coin
weightedcoin = MonteCarlo.Dice(name_of_list_of_faces)

#change the weighted coin's weight for side H to 5
weightedcoin.change_weight('H',5)

#Takes a parameter of how many times the die is to be rolled defaults to 1. 
faircoin.roll_dice(1):

#Returns a copy of the private die data frame.
faircoin.show_dice():
    
#create a game with 2 dice, one fair and one unfair
game1 = MonteCarlo.Game([faircoin, weightedcoin])

#play a game with 1000 rolls
game1.play(1000)

#Returns the results from rolling the various dice from the most recent play in a wide dataframe
game1.results('wide')

#pass the game to Analyzer to calculate combinations such as jackpots
analyzer1 = MonteCarlo.Analyzer(game1)

#determine how many jackpots, i.e. situations with all faces matching
analyzer1.jackpot()

#determine how many times a given face is rolled in each event and returns a wide 
#data frame of results with an index of the roll number, face values as columns, and count values in the cells.
analyzer1.face_counts()

#Compute the distinct order-independent combinations of faces rolled, along with their counts and returns a data frame with a MultiIndex of distinct combinations and a column for the associated counts. '''
analyzer1.combo_counts()

#Compute the distinct order-dependent permutations of faces rolled, along with their counts and returns a data frame with a MultiIndex of distinct permutations and a column for the associated counts. '''
analyzer1.permutation_count()

```

# API description

```python
class Dice:
    '''The dice class creates dice with n number of sides, changes the weight to specific sides as needed, rolls the dice and Returns a copy of the private die data frame.'''
    def __init__(self, faces: np.ndarray):
        '''Initializer takes a numpy array of faces as an argument. Data type may be strings or numbers, and values must be distinct. A weight of 1 is internally
        initializes for each face.'''
    def change_weight(self, face_value, new_weight):
        '''Takes two arguments: the face value to be changed and the new weight. Checks to see if the face is a valid value and if the weight is a valid  type.'''
    def roll_dice(self, times_rolled=1):
        '''Takes a parameter of how many times the die is to be rolled; defaults to 1. Returns a Python list of outcomes and does not internally store these results.'''
        
class Game:
    '''This is the game class, which rolls one or more similar dice one or more times. Each die in a given game has the same number of sides and associated faces, but each die object may have
its own weights. Game objects only keep the results of their most recent play. '''
    def __init__(self,dice_list):
        '''Initializer takes a list of already instantiated similar dice '''
        
    def play(self, roll_number):
        '''Takes an integer parameter to specify how many times the dice should be rolled and saves the result of the play to a private data frame in wide format'''   
        
    def results(self,data_format):
        '''Returns the results from rolling the various dice from the most recent play.'''

class Analyzer:
    '''An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it.'''
    def __init__(self, current_game):
        '''Initializer takes a game object as its input parameter and throws a `ValueError` if the passed value is not a Game object. '''
        
    def jackpot(self):
        '''Computes how many times the game resulted in a jackpot with all faces the same, and returns an integer for the number of jackpots. '''
        
    def face_counts(self):
        '''Computes how many times a given face is rolled in each event and returns a wide data frame of results with an index of the roll number, face values as columns, and count values in the cells.'''        
        
    def combo_count(self):
        '''Computes the distinct combinations of faces rolled, along with their counts and returns a data frame with a MultiIndex of distinct combinations and a column for the associated counts. '''

    def permutation_count(self):
        '''Computes the distinct permutations of faces rolled, along with their counts and returns a data frame with a MultiIndex of distinct permutations and a column for the associated counts. '''

```python
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)