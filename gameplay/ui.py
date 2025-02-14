import math
import tkinter as tk
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.heuristic_interface import HeuristicInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from ui_elements.probability import Probability
from ui_elements.serum import Serum
from gameplay.enums import bgc

from os.path import join


class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, suggest, log, probs=True):
        #  Base window setup
        capacity = 10
        w, h = 1280, 800
        self.root = tk.Tk()

        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)
        self.root.configure(bg=bgc)

        self.button_menu = None

        self.humanoid = data_parser.get_random()
        
        self.log = log
        if suggest:
            self.machine_interface = HeuristicInterface(self.root, w, h)

        #  Add buttons and logo
        user_buttons = [("Skip", lambda: [scorekeeper.skip(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper), 
                                          self.prob.update(self.humanoid, probs)]),
                        ("Squish", lambda: [scorekeeper.squish(self.humanoid),
                                            self.update_ui(scorekeeper),
                                            self.get_next(
                                                data_fp,
                                                data_parser,
                                                scorekeeper),
                                            self.prob.update(self.humanoid, probs)]),
                        ("Save", lambda: [scorekeeper.save(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper),
                                          self.prob.update(self.humanoid, probs)]),
                        ("Scram", lambda: [scorekeeper.scram(self.humanoid),
                                           self.update_ui(scorekeeper),
                                           self.get_next(
                                               data_fp,
                                               data_parser,
                                               scorekeeper),
                                           self.prob.update(self.humanoid, probs)]),
                        ("Reveal", lambda: [scorekeeper.reveal(self.humanoid),
                                            self.update_ui_reveal(scorekeeper),
                                            self.disable_reveal()])]


        self.button_menu = ButtonMenu(self.root, user_buttons, probs)

        if suggest:
            machine_buttons = [("Suggest", lambda: [self.machine_interface.suggest(self.humanoid)]),
                               ("Act", lambda: [self.machine_interface.act(scorekeeper, self.humanoid),
                                                self.update_ui(scorekeeper),
                                                self.get_next(
                                                    data_fp,
                                                    data_parser,
                                                    scorekeeper),
                                                    self.prob.update(self.humanoid, probs)])]
            self.machine_menu = MachineMenu(self.root, machine_buttons)

        #  Display central photo
        self.game_viewer = GameViewer(self.root, w, h, data_fp, self.humanoid)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        # Display the countdown
    
        self.clock = Clock(self.root, w, h, scorekeeper.remaining_time)

        if not probs:
            self.button_menu.disable_reveal()
        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.root, w, h, capacity, probs)

        # display probabilities
        self.prob = Probability(self.root, w, h, self.humanoid, probs)

        #display serum count
        self.serums = Serum(self.root, w, h, scorekeeper.serum)

        self.root.mainloop()

    def update_ui(self, scorekeeper):
        
        self.clock.update_time(scorekeeper.remaining_time)
        self.serums.update(scorekeeper.serum)

        self.capacity_meter.update_fill(scorekeeper.get_current_capacity(), scorekeeper.logger[-1])

    def update_ui_reveal(self, scorekeeper):
        for label in self.prob.empties:
            label.destroy()

        self.prob.empties = []

        for bar in self.prob.fills:
            bar.destroy()

        self.prob.fills = []

        self.clock.update_time(scorekeeper.remaining_time)
        self.prob.render_Job(self.humanoid.job)
       
    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self, data_fp, data_parser, scorekeeper):
        remaining = len(data_parser.unvisited)

        # Ran out of humanoids? Disable skip/save/squish
        if remaining == 0 or scorekeeper.remaining_time <= 0:
            if self.log:
                scorekeeper.save_log()
            self.capacity_meter.update_fill(0)
            self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(scorekeeper.get_score())
        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.create_photo(fp)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())

    def disable_reveal(self):
        if self.button_menu:
            self.button_menu.disable_reveal()
