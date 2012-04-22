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

In-game stuff.
"""

from __future__ import division

from random import randint
from random import uniform
from itertools import chain
from itertools import repeat
from collections import Counter
import math as maths

from pyglet import graphics
from pyglet import gl
from pyglet import resource
from pyglet import sprite

from pymunk import Body
from pymunk import Circle
from pymunk import moment_for_circle
from pymunk import constraint

from physics import Vector
from graphics import centre_image

class Stars(object):
	def __init__(self, size, batch, group):
		n = size.width*size.height//1000
		positions = tuple(chain.from_iterable(self.positions(n, size)))
		batch.add(n, gl.GL_POINTS, group, ('v2i', positions))

	def positions(self, n, size):
		for i in range(n):
			yield randint(0, size.width), randint(0, size.height)

class Asteroid(object):

	TYPES = {
		"water": 5,
		"oil": 3,
		"uranium": 1,
		"aluminium": 10,
		"titanium": 10,
	}

	def __init__(self, x, y, size, batch, group, space):
		x, y = x-size/2, y-size/2
		points = randint(15, 20)
		self.batch = batch
		self.body = Body(size, moment_for_circle(size, 0, size))
		self.body.position = x, y
		self.shape = Circle(self.body, 1.1*size)
		self.shape.elasticity = 0.35
		self.shape.friction = 0.1
		self.group = PhysicsBodyGroup(group, self)
		colour = list(chain.from_iterable(repeat(self.grey(), points)))
		self.points = list(self.construct_points(points, size))
		self.vertex_list = batch.add(
			points, gl.GL_POLYGON, self.group,
			('v2i', list(chain.from_iterable(self.points))),
			('c3B', colour)
		)
		self.body.angle = randint(0, int(maths.radians(360)/points))
		self.type = self._weighted_random_choice(Asteroid.TYPES)
		self.sprite = sprite.Sprite(centre_image(resource.image("raw_"+self.type+".png")), 0, 0, batch=batch, group=self.group)
		self.sprite.visible = False
		self._populated = False
		space.add(self.body, self.shape)

	def grey(self):
		grey = randint(75, 190)
		return grey, grey, grey

	def construct_points(self, n, size):
		angle = maths.radians(360)/n
		for a in (angle*i for i in range(n)):
			random_size = uniform(1, 1.3)*size
			yield int(random_size*maths.cos(a)), int(random_size*maths.sin(a))

	@property
	def position(self):
		return Vector(*self.body.position)

	@classmethod
	def populate(cls, min, max, world_size, batch, group, space):
		main = Segment(size=world_size)
		#return cls.verify(
		return [Asteroid(segment.centre.x, segment.centre.y, randint(min, max), batch, group, space) for segment in main.recursive_split(max*1.75)]#)

	@classmethod
	def verify(cls, asteroids):
		""" Ensure we have at least 1 of each asteroid. Don't want to screw
		people over.
		"""
		count = Counter(asteroid.type for asteroid in asteroids)
		for type in Asteroid.TYPES:
			if count[type] < 1:
				return False
		return asteroids

	def _weighted_random_choice(self, choices):
		max = sum(choices.values())
		pick = uniform(0, max)
		current = 0
		for key, value in choices.items():
			current += value
			if current > pick:
				return key

	@property
	def populated(self):
		return self._populated

	@populated.setter
	def populated(self, populated):
		if not populated == self._populated:
			self._populated = populated
			if populated:
				name = self.type
			else:
				name = "raw_"+self.type
			self.sprite.image = centre_image(resource.image(name+".png"))
			if self.type == "home": #HACK
				self.sprite.visible = True

	def point_over(self, x, y):
		sx, sy = self.position
		return (x-sx)**2+(y-sy)**2 < self.shape.radius**2

	def destroy(self):
		self.vertex_list.delete()
		del self

	def hovered(self, x, y):
		sx, sy = self.position
		x, y = (Vector(x-sx, y-sy)).closest(Vector(*point) for point in self.points)
		self.marker.x = x
		self.marker.y = y

class Segment(object):

	RAGGEDNESS = 0.5

	def __init__(self, width=None, height=None, x=0, y=0, size=None):
		if size:
			self.width = size.width
			self.height = size.height
		else:
			self.width = width
			self.height = height
		self.x = x
		self.y = y

	def split(self, minimum):
		ragged_factor = uniform(0, Segment.RAGGEDNESS)
		if self.width > self.height:
			width = self.width/2
			ragged_factor *= width
			if width-ragged_factor < minimum:
				return self
			return Segment(width+ragged_factor, self.height, self.x, self.y), Segment(width-ragged_factor, self.height, self.x+width+ragged_factor, self.y)
		else:
			height = self.height/2
			ragged_factor *= height
			if height-ragged_factor < minimum:
				return self
			return Segment(self.width, height+ragged_factor, self.x, self.y), Segment(self.width, height-ragged_factor, self.x, self.y+height+ragged_factor)

	def recursive_split(self, minimum):
		parts = self.split(minimum)
		try:
			first, second = parts
			for segment in first.recursive_split(minimum):
				yield segment
			for segment in second.recursive_split(minimum):
				yield segment
		except TypeError:
			yield parts

	@property
	def centre(self):
		return Vector(self.x+self.width/2, self.y+self.width/2)

class PhysicsBodyGroup(graphics.Group):
	def __init__(self, parent, body):
		super(PhysicsBodyGroup, self).__init__(parent=parent)
		self.body = body

	def set_state(self):
		gl.glPushMatrix()
		x, y = self.body.body.position
		gl.glTranslatef(x, y, 0)
		gl.glRotatef(maths.degrees(self.body.body.angle), 0, 0, 1)

	def unset_state(self):
		x, y = self.body.body.position
		gl.glTranslatef(-x, -y, 0)
		gl.glRotatef(-maths.degrees(self.body.body.angle), 0, 0, 1)
		gl.glPopMatrix()

	def __eq__(self, other):
		return (self.__class__ is other.__class__ and
		        self.texture == other.__class__)

class Person(object):
	def __init__(self, x, y, batch, group, space):
		self.speed = 10
		self.group = PhysicsBodyGroup(group, self)
		self.sprite = sprite.Sprite(centre_image(resource.image("pushing.png")), 0, 0, batch=batch, group=self.group)
		self.body = Body(2, moment_for_circle(2, 5, 14))
		self.body.position = x, y
		self.shape = Circle(self.body, 15)
		self.shape.elasticity = 0
		self.shape.friction = 0.5
		self.old = (0, 0)
		self.target = (x, y)
		space.add(self.body, self.shape)

	@classmethod
	def populate(cls, world_size, batch, group, space):
		return[Person(0, 0, batch, group, space) for _ in range(20)]

	def update(self):
		angle = -maths.atan2(*Vector(*self.target)-Vector(*self.body.position))
		self.body.angle = angle
		x, y = self.body.position
		self.body.apply_impulse((20*maths.sin(angle), -20*maths.cos(angle)))

class Strut(object):
	def __init__(self, asteroid_1, asteroid_2, pos_1, pos_2, space):
		self.constraint = constraint.PinJoint(asteroid_1.body, asteroid_2.body, pos_1, pos_2)
		self.space = space
		space.add(self.constraint)
		self.vertex_list = None

	def update(self, batch, group):
		if self.constraint.impulse > 1000:
			self.snap()
			return True
		if self.vertex_list:
			self.vertex_list.delete()
		ax, ay = self.constraint.a.position+Vector(*self.constraint.anchr1)
		bx, by = self.constraint.b.position+Vector(*self.constraint.anchr2)
		points = [int(x) for x in [ax, ay, bx, by]]
		self.vertex_list = batch.add(
			2, gl.GL_LINES, group,
			('v2i', tuple(points))
		)


	def snap(self):
		if self.vertex_list:
			self.vertex_list.delete()
		self.space.remove(self.constraint)

class Umbilical(object):
		def __init__(self, asteroid_1, asteroid_2, pos_1, pos_2, space):
			self.constraint = constraint.DampedSpring(asteroid_1.body, asteroid_2.body, pos_1, pos_2)
			self.space = space
			space.add(self.constraint)
			self.vertex_list = None

		def update(self, batch, group):
			if self.constraint.impulse > 1000:
				self.snap()
				return True
			if self.vertex_list:
				self.vertex_list.delete()
			ax, ay = self.constraint.a.position+Vector(*self.constraint.anchr1)
			bx, by = self.constraint.b.position+Vector(*self.constraint.anchr2)
			points = [int(x) for x in [ax, ay, bx, by]]
			self.vertex_list = batch.add(
				2, gl.GL_LINES, group,
				('v2i', tuple(points))
			)

		def snap(self):
			if self.vertex_list:
				self.vertex_list.delete()
			self.space.remove(self.constraint)
