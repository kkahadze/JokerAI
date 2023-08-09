from .decision_bot_abstract import DecisionBotAbstract
from models.model_structure_1 import Net
import torch
from sklearn.preprocessing import StandardScaler

class DecisionBot1(DecisionBotAbstract):
    def __init__(self, number, model=None, scaling_model=None):
        self.model = model
        self.scaling_model = scaling_model
        super().__init__(number)

    def reset(self):
        super().reset()

    def prompt_model(self, observation):
        return self.get_highest_in_distribution(observation)
    
    # def get_second_highest_in_distribution(self, observation):
    #     # return self.model.predict)call(observation, 2)

    def get_highest_in_distribution(self, observation):
        output = self.predict_call(observation)
        return output
    
    def predict_call(self, observation):
        # Prepare the input tensor
        observation['deciding_player'] = self.number
        input_tensor = self.prepare_input(observation)
        # Initialize the model with the same architecture
        net = Net(18)  # replace n_features with the number of input features

        # Load the state dictionary
        net.load_state_dict(torch.load('../models/' + str(self.model) + '.pth'))

        # Make sure to call model.eval() method before inferencing to set the dropout and batch normalization layers to evaluation mode
        net.eval()

        with torch.no_grad():
            output = net(input_tensor)
        
        return output.argmax().item()
    

