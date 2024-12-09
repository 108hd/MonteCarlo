import numpy as np
import pandas as pd
from collections import Counter

class Dice:
    '''The dice class creates dice with n number of sides, changes the weight to 
    specific sides as needed, rolls the dice and Returns a copy of the private die data frame.'''
    def __init__(self, faces: np.ndarray):
        '''Initializer takes a numpy array of faces as an argument. Data type may be
        strings or numbers, and values must be distinct. A weight of 1 is internally
        initializes for each face.'''
        # Ensures array of faces is numpy
        if not isinstance(faces, np.ndarray):
            raise TypeError("Input must be a numpy array")
        
        # Ensures datatype is string or number
        datatypes = (np.number, np.str_)
        if not any(np.issubdtype(faces.dtype, dtype) for dtype in datatypes):
            raise TypeError("Array datatype must be either strings or numbers")
       
        # Ensures array values are distinct
        unique_faces = set(faces)
        if len(unique_faces) != len(faces):
            raise ValueError("Array values must be unique")  
        
        self.faces = faces
        # Weight of each is 1
        # Faces and weights in private dataframe 
        self._die = pd.DataFrame({
            "faces": self.faces,
            "weights": np.ones(len(faces))
        })

    # Ensure face value is valid
    def change_weight(self, face_value, new_weight):
        '''Takes two arguments: the face value to be changed and the new
        weight. Checks to see if the face is a valid value and if the weight is a valid  type.'''
        if face_value not in self.faces:
            raise ValueError("Face must be a valid value")
    
        # Ensure new weight is valid datatype
        if not isinstance(new_weight, (int, float)):
            raise TypeError("Weight must be either integer or float")
        
        # Update the weight in the DataFrame
        self._die.loc[self._die['faces'] == face_value, 'weights'] = new_weight

    def roll_dice(self, times_rolled=1):
        '''Takes a parameter of how many times the die is to be rolled;
        defaults to 1. Returns a Python list of outcomes and does not internally store
        these results.'''
        results = []
        for _ in range(times_rolled):
            result = self._die['faces'].sample(weights=self._die['weights']).values[0]
            results.append(result)
        return results
        
    def show_dice(self):
        '''Returns a copy of the private die data frame.'''
        return self._die.copy()

class Game:
    '''This is the game class, which rolls one or more similar dice one or more times. Each die in 
    a given game has the same number of sides and associated faces, but each die object may have
    its own weights. Game objects only keep the results of their most recent play. '''
    def __init__(self,dice_list):
        '''Initializer takes a list of already instantiated similar dice '''
        self.dice_list = dice_list
            #dice list would be like Dice 1, Dice 2, Dice 3, etc.  
    def play(self, roll_number):
        '''Takes an integer parameter to specify how many times the dice should be 
        rolled and saves the result of the play to a private data frame in wide format'''
        self.roll_number = roll_number
        if not isinstance(roll_number, int):
            raise TypeError("Roll number must be an integer")

        dice_rolls = []
        for dice in self.dice_list:
            dice_rolls.append(dice.roll_dice(roll_number))
        self.named = pd.DataFrame(dice_rolls).transpose()
        self.named.index.name = "roll_number"
            
    def results(self,data_format):
        '''Returns the results from rolling the various dice from the most recent play.'''
        
        if data_format not in ["wide", "narrow"]:
            return ValueError("must be wide or narrow format")
        if data_format == 'wide':
            return self.named.copy()
        elif data_format == 'narrow':
            temp = pd.melt(self.named.reset_index(), id_vars = ["roll_number"], 
            var_name = "Die_number", value_name = "Value")
            temp = temp.set_index(['roll_number', 'Die_number'])
            return temp.copy()

class Analyzer:
    '''An Analyzer object takes the results of a single game and computes
    various descriptive statistical properties about it.'''
    def __init__(self, current_game):
        self.current_game = current_game
        '''Initializer takes a game object as its input parameter and throws a 
        `ValueError` if the passed value is not a Game object. '''
        if not isinstance(current_game, Game):
            raise ValueError("must be a Game object")
    def jackpot(self):
        '''Computes how many times the game resulted in a jackpot with all faces the same,
        and returns an integer for the number of jackpots. '''
        res = self.current_game.results('wide')
        Jackpot = 0
        for i in range(len(res)):
            val = (res.iloc[i].nunique())
            if val == 1:
                Jackpot += 1    
        return Jackpot

    def face_counts(self):
        '''Computes how many times a given face is rolled in each event and returns a wide 
        data frame of results with an index of the roll number, face values as
        columns, and count values in the cells.'''
        res = self.current_game.results('wide')
        new_dict = {}
        for face in self.current_game.dice_list[0].faces:
            new_dict[face]=0
        dict_list = []
        for i in range(len(res)):
            dict2 = new_dict.copy()
            for k in res.iloc[i]:
                dict2[k] += 1
            dict_list.append(dict2)
        return pd.DataFrame(dict_list)
        
    
    def combo_count(self):
        '''Computes the distinct combinations of faces rolled, along with their counts and
        returns a data frame with a MultiIndex of distinct combinations and a column for 
        the associated counts. '''
        res = self.current_game.results('wide')
        tuple_list = []
        for row in range(len(res)):
            mylist = sorted(list(res.iloc[row]))
            mylist = tuple(mylist)
            tuple_list.append(mylist)
        my_combo = Counter(tuple_list)
        df_combo = pd.DataFrame.from_dict(my_combo, orient='index', columns=['count'])
        df_combo.index = pd.MultiIndex.from_tuples(df_combo.index)

        return df_combo

    def permutation_count(self):
        '''Computes the distinct permutations of faces rolled, along with their counts and
        returns a data frame with a MultiIndex of distinct permutations and a column for 
        the associated counts. '''
        res = self.current_game.results('wide')
        tuple_list = []
        for row in range(len(res)):
            mylist = (list(res.iloc[row]))
            mylist = tuple(mylist)
            tuple_list.append(mylist)
        my_perm = Counter(tuple_list)
        df_perm = pd.DataFrame.from_dict(my_perm, orient='index', columns=['count'])
        df_perm.index = pd.MultiIndex.from_tuples(df_perm.index)
        
        return df_perm