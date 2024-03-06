# Copyright (C) 2018-20 Arc676/Alessandro Vinciguerra <alesvinciguerra@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation (version 3)

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from random import randint

from lingua_franca.parse import extract_number
from ovos_workshop.decorators import intent_handler
from ovos_workshop.intents import IntentBuilder
from ovos_workshop.skills import OVOSSkill

__author__ = 'Arc676/Alessandro Vinciguerra'


class NumberGuessSkill(OVOSSkill):
    def initialize(self):
        self.playing = False
        self.lowerBound = 0
        self.upperBound = 100

    def get_numerical_response(self, dialog):
        while self.playing:
            val = self.get_response(dialog)
            try:
                return int(extract_number(val))
            except ValueError:
                self.speak_dialog("invalid.input")
            except:
                self.speak_dialog("input.error")

    @intent_handler(
        IntentBuilder("").require("NumberGuess").optionally("Play").optionally(
            "Suggest"))
    def handle_start_game_intent(self, message):
        self.playing = True
        self.speak_dialog("start.game")

        # get lower bound
        self.lowerBound = self.get_numerical_response("get.lower")
        # get upper bound
        self.upperBound = self.get_numerical_response("get.upper")

        answer = randint(self.lowerBound, self.upperBound)
        userGuess = self.lowerBound - 1
        while userGuess != answer:
            userGuess = self.get_numerical_response("guess")
            if userGuess < answer:
                self.speak_dialog("too.low")
            elif userGuess > answer:
                self.speak_dialog("too.high")
        self.speak_dialog("correct")
        self.playing = False

    def stop(self):
        if self.playing:
            self.playing = False
            self.lowerBound, self.upperBound = 0, 100
            return True
        return False
