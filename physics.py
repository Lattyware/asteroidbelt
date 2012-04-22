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

Just some helper classes.
"""

import math as maths
from collections import namedtuple

Size = namedtuple("Size", ["width", "height"])

class Vector(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __getitem__(self, item):
		if item == 0:
			return self.x
		if item == 1:
			return self.y
		raise IndexError("Index out of range.")

	@property
	def magnitude_sq(self):
		return self.x**2+self.y**2

	@property
	def magnitude(self):
		return maths.sqrt(self.magnitude_sq)

	def __sub__(self, other):
		return Vector(self.x-other.x, self.y-other.y)

	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)

	def __mul__(self, scalar):
		return Vector(self.x*scalar, self.y*scalar)

	def __lt__(self, other):
		return self.magnitude_sq < other.magnitude_sq

	def __gt__(self, other):
		return self.magnitude_sq > other.magnitude_sq

	def __repr__(self):
		return "Vector("+str(self.x)+", "+str(self.y)+")"

	def closest(self, others):
		minimum = None
		for other in others:
			if not minimum or (self-other) < minimum:
				minimum = other
		return minimum
