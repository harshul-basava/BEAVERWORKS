import argparse
import os
from endpoints.data_parser import DataParser
from endpoints.heuristic_interface import HeuristicInterface
from endpoints.training_interface import TrainInterface
from endpoints.inference_interface import InferInterface
from plot_logs import Plot

from gameplay.scorekeeper import ScoreKeeper
from gameplay.ui import UI
from gameplay.enums import ActionCost
from model_training.rl_training import train
from tkmacosx import Button
from PIL import ImageTk, Image
import tkinter as tk


class Main(object):
    """
    Base class for the SGAI 2023 game
    """
    def __init__(self, mode, log):
        self.data_fp = os.getenv("SGAI_DATA", default='data')
        self.data_parser = DataParser(self.data_fp)

        shift_length = 720
        capacity = 10
        self.scorekeeper = ScoreKeeper(shift_length, capacity)

        if mode == 'heuristic':   # Run in background until all humanoids are processed
            # TODO investigate why this just kills everything (follow humanoid to prediction to actions to scorekeeper)
            simon = HeuristicInterface(None, None, None, display = False)
            while len(self.data_parser.unvisited) > 0:
                if self.scorekeeper.remaining_time <= 0:
                    print('Ran out of time')
                    break
                else:
                    humanoid = self.data_parser.get_random()
                    action = simon.get_model_suggestion(humanoid, self.scorekeeper.at_capacity())
                    if action == ActionCost.SKIP:
                        self.scorekeeper.skip(humanoid)
                    elif action == ActionCost.SQUISH:
                        self.scorekeeper.squish(humanoid)
                    elif action == ActionCost.SAVE:
                        self.scorekeeper.save(humanoid)
                    elif action == ActionCost.SCRAM:
                        self.scorekeeper.scram(humanoid)
                    elif action == ActionCost.REVEAL:
                        self.scorekeeper.reveal(humanoid)
                    else:
                        raise ValueError("Invalid action suggested")
            if log:
                self.scorekeeper.save_log()
            print("RL equiv reward:",self.scorekeeper.get_cumulative_reward())
            print(self.scorekeeper.get_score())
        elif mode == 'train':  # RL training script
            env = TrainInterface(None, None, None, self.data_parser, self.scorekeeper, display=False,)
            train(env)
            if log:
                self.scorekeeper.save_log('rl')
                Plot.plot_actions('log.csv')
        elif mode == 'infer':  # RL training script
            simon = InferInterface(
                root=None,
                w=None,
                h=None,
                data_parser=self.data_parser,
                scorekeeper=self.scorekeeper,
            )
            while len(simon.data_parser.unvisited) > 0:
                if simon.scorekeeper.remaining_time <= 0:
                    break
                else:
                    humanoid = self.data_parser.get_random()
                    simon.act(humanoid)
            self.scorekeeper = simon.scorekeeper
            if log:
                self.scorekeeper.save_log('rl')
                Plot.plot_actions('log.csv')
            print("RL equiv reward:",self.scorekeeper.get_cumulative_reward())
            print(self.scorekeeper.get_score())
        else: # Launch UI gameplay
            self.root.geometry("1280x800")
            self.image = ImageTk.PhotoImage(Image.open(f"ui_elements/graphics/Team_Husk.png"))
            label1 = tk.Label(self.root, image=self.image)
            label1.place(x=0, y=0)
            self.mode_1 = ImageTk.PhotoImage(Image.open(f"ui_elements/graphics/Mode1.png").resize((283, 92), Image.LANCZOS))
            self.mode_2 = ImageTk.PhotoImage(Image.open(f"ui_elements/graphics/Mode2.png").resize((283, 92), Image.LANCZOS))

            easy = Button(self.root, image=self.mode_1, width=280, height=90, command=lambda: self.show_probs(False), highlightbackground="#F8EDE0")
            hard = Button(self.root, image=self.mode_2, width=280, height=90, command=lambda: self.show_probs(True), highlightbackground="#F8EDE0")

            easy.place(x=30, y=128)
            hard.place(x=315, y=128)

            self.root.mainloop()
            # try:
            self.ui = UI(self.data_parser, self.scorekeeper, self.data_fp, log=log, suggest=False, probs=self.probs)
            self.scorekeeper.save_log("player", self.diff)
            # except:
            #     print("Error: no selection made")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python3 main.py',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-m', '--mode', type=str, default = 'user', choices = ['user','heuristic','train','infer'],)
    parser.add_argument('-l', '--log', type=bool, default = False)
    # parser.add_argument('-a', '--automode', action='store_true', help='No UI, run autonomously with model suggestions')
    # parser.add_argument('-d', '--disable', action='store_true', help='Disable model help')

    args = parser.parse_args()
    Main(args.mode, args.log)
