# creates a bar graphs showing the distribution of the last full game logged in log.csv
# probably will not run, since log.csv is 90k lines long 

import pandas
import matplotlib.pyplot as plt

class Plot:
    def __init__(self, file_path):
        self.file_path = file_path

    def plot_actions(self):

        df = pandas.read_csv(self.file_path, usecols=['local_run_id', 'action'])

        action_counts = df['action'].value_counts()

        plt.figure(figsize=(10, 6))
        action_counts.plot(kind='bar')
        plt.title('Actions taken in the last game')
        plt.xlabel('Action')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()
