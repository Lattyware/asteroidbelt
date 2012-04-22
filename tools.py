#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

"""
Copyright © 2012: Gareth Latty <gareth@lattyware.co.uk>

    This file is part of Asteroid Belt.

    Asteroid Belt is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Asteroid Belt is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Asteroid Belt. If not, see <http://www.gnu.org/licenses/>.

In-game tools.
"""

from pyglet import resource
from pyglet import window

from graphics import centre_image
import entities
from physics import Vector

class Tool(object):
	def __init__(self, order, name, description, space):
		self.order = order
		self.name = name
		self.description = description
		self.image = centre_image(resource.image(self.name.lower()+".png"))
		self.space = space

	def selection(self, selection, constraints):
		raise NotImplementedError

	def end_selecting(self):
		return None

class Drill(Tool):
	def __init__(self, *args):
		super(Drill, self).__init__(0, "Drill",
			"A drill allows you to mine an asteroid for resources.", *args)

	def selection(self, selection, constraints):
		asteroid = selection[0][0]
		asteroid.populated = True
		return None

class Umbilical(Tool):
	def __init__(self, *args):
		super(Umbilical, self).__init__(1, "Umbilical",
		  "An umbilical cord allows you to transport large items to other asteroids.", *args)

	def selection(self, selection, constraints):
		if len(selection) == 2:
			((asteroid_1, clicked_1), (asteroid_2, clicked_2)) = selection
			pos_1 = Vector(*clicked_1)
			pos_2 = Vector(*clicked_2)
			print(pos_1, pos_2, pos_1-pos_2, (pos_1-pos_2).magnitude)
			if (pos_1-pos_2).magnitude < 300:
				constraints.add(entities.Strut(asteroid_1, asteroid_2, tuple(pos_1-asteroid_1.position), tuple(pos_2-asteroid_2.position), self.space))
			return None
		else:
			return self

class Strut(Tool):
	def __init__(self, *args):
		super(Strut, self).__init__(2, "Strut",
		                            "A support strut stabilises two asteroids.", *args)

	def selection(self, selection, constraints):
		if len(selection) == 2:
			((asteroid_1, clicked_1), (asteroid_2, clicked_2)) = selection
			pos_1 = Vector(*clicked_1)
			pos_2 = Vector(*clicked_2)
			print(pos_1, pos_2, pos_1-pos_2, (pos_1-pos_2).magnitude)
			if (pos_1-pos_2).magnitude < 200:
				constraints.add(entities.Strut(asteroid_1, asteroid_2, tuple(pos_1-asteroid_1.position), tuple(pos_2-asteroid_2.position), self.space))
			return None
		else:
			return self

class Rocket(Tool):
	def __init__(self, *args):
		super(Rocket, self).__init__(3, "Rocket",
		    "A rocket will move an asteroid.", *args)

	def selection(self, selection, constraints):
		asteroid, position = selection[0]
		vec = asteroid.position-Vector(*position)
		mag = vec.magnitude
		asteroid.body.apply_impulse(vec*(1/mag)*1000, (0, 0))
		return None

class Nuke(Tool):
	def __init__(self, *args):
		super(Nuke, self).__init__(4, "Nuke",
		    "A nuclear bomb will destroy an asteroid.", *args)

	def selection(self, selection, constraints):
		return None
