import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
import random

class player_sheet():
    def __init__(self, blank_sheet_path):
        self.player_sheet = pd.read_csv(blank_sheet_path)
        self.questions = list(self.player_sheet['Question'])
        self.score = list(self.player_sheet['Score'])

        self.personality_result_dict = {'Agreeableness': 0,
                                 'Openness': 0,
                                 'Neuroticism': 0,
                                 'Conscientiousness': 0,
                                 'Extraversion': 0}

    def check_for_missing_values(self):
        missing_val_idx = [i for i, val in enumerate(self.score) if val == 0]
        return missing_val_idx

    def update_player_sheet(self, model_val_array):
        if len(model_val_array) != len(self.player_sheet['Score']):
            raise ValueError(f"Length mismatch: Expected {len(self.player_sheet['Score'])}, but got {len(model_val_array)}")

        self.player_sheet.loc[:, 'Score'] = model_val_array
        self.score = list(self.player_sheet['Score'])

    def calculate_traits(self):
        for key, vals in self.personality_result_dict.items():
            indices = self.player_sheet[self.player_sheet['Trait'] == key].index
            scores = self.player_sheet.loc[indices, 'Score'].tolist()

            if len(scores) > 0:
                self.personality_result_dict[key] = sum(scores) / len(scores)
            else:
                self.personality_result_dict[key] = 0

    def plot_personality_type(self):
        labels = list(self.personality_result_dict.keys())
        values = list(self.personality_result_dict.values())

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

        values.append(values[0])
        angles = np.append(angles, angles[0])

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.fill(angles, values, color='blue', alpha=0.25)
        ax.plot(angles, values, color='blue', linewidth=2)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        plt.show()


### tests
# p1 = player_sheet('csv/BFI_44.csv')
# print(p1.questions)
# model_val_array = [random.randint(1, 5) for _ in range(44)]
# print(model_val_array)
# print(p1.update_player_sheet(model_val_array))
# print(p1.score)
# p1.calculate_traits()
# print(p1.personality_result_dict)
# p1.plot_personality_type()
# # print(p1.check_for_missing_values())
