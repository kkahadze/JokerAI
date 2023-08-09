from .rule_based_bot import RuleBasedBot
from .utils import get_compliment
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler
from joblib import load

class DecisionBotAbstract(RuleBasedBot):
    def reset(self):
        super().reset()

    def call(self, observation):
        compliment = get_compliment(observation)

        call = self.prompt_model(observation)
        if compliment and compliment == call:
            call = self.get_second_highest_in_distribution(observation)
        
        self.desired = call
        self.decision_time_obs["desired"] = call
        self.decision_time_obs["deciding_player"] = self.number

        return self.desired
    
    def prepare_input(self, observation):
        # Specify the order of the columns
        column_order = ['dealt', 'first_to_play', 'dealer', 'wild_suit',
                        'player0desired', 'player1desired', 'player2desired', 'player3desired',
                        'hand1', 'hand2', 'hand3', 'hand4', 'hand5', 'hand6', 'hand7',
                        'hand8', 'hand9', 'deciding_player']
        
        # Initialize a new dictionary that follows the column order
        data = {}
        
        for col in column_order:
            if col.startswith("hand"):
                # Extract card index from column name
                idx = int(col.replace("hand", "")) - 1
                try:
                    # If card exists in the hand, use its value
                    data[col] = observation['hand'][idx]
                except IndexError:
                    # If the card doesn't exist, use a default value
                    data[col] = 0  # or another default value as appropriate
            else:
                # Use the value from the observation dictionary
                data[col] = observation[col]

        # Transform the dictionary into a DataFrame
        df = pd.DataFrame(data, index=[0])
        
        scaler = load('../models/' + self.scaling_model + '.joblib')

        normalized_data = scaler.transform(df)

        # Convert data to PyTorch tensor
        input_tensor = torch.FloatTensor(normalized_data)
        
        return input_tensor
