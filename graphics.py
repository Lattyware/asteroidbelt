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

Graphics related stuff.
"""

from __future__ import division

from pyglet.window import key
from pyglet import gl
from pyglet import graphics

from physics import Vector

def centre_image(image):
	"""Centre an image in-place and return it for convenience."""
	image.anchor_x = image.width // 2
	image.anchor_y = image.height // 2
	return image

class Camera(object):

	def __init__(self, size, world_size, speed, drag_speed):
		self.size = size
		self.world_size = world_size
		self._x = 0
		self._y = 0
		self.movement = Vector(0, 0)
		self.speed = speed
		self.drag_speed = drag_speed
		self.dragged = Vector(0, 0)

	def key_pressed(self, symbol):
		if symbol == key.UP:
			self.movement.y += self.speed
		if symbol == key.DOWN:
			self.movement.y -= self.speed
		if symbol == key.RIGHT:
			self.movement.x += self.speed
		if symbol == key.LEFT:
			self.movement.x -= self.speed

	def key_released(self, symbol):
		if symbol == key.UP:
			self.movement.y -= self.speed
		if symbol == key.DOWN:
			self.movement.y += self.speed
		if symbol == key.RIGHT:
			self.movement.x -= self.speed
		if symbol == key.LEFT:
			self.movement.x += self.speed

	def mouse_dragged(self, dx, dy):
		self.dragged.x = dx*self.drag_speed
		self.dragged.y = dy*self.drag_speed

	def clear(self):
		self._x = 0
		self._y = 0

	def update(self, frame_time):
		self.move(self.movement*frame_time)
		self.move(self.dragged)
		self.dragged = Vector(0, 0)

	def translate(self, x, y):
		return self.x+x, self.y+y

	def move(self, vector):
		self.x += vector.x
		self.y += vector.y

	@property
	def x(self):
		return self._x

	@x.setter
	def x(self, x):
		self._x = x
		self._x = max(self._x, 0)
		self._x = min(self._x, self.world_size.width-self.size.width)

	@property
	def y(self):
		return self._y

	@y.setter
	def y(self, y):
		self._y = y
		self._y = max(self._y, 0)
		self._y = min(self._y, self.world_size.height-self.size.height)

class CameraGroup(graphics.Group):
	def __init__(self, parent, camera):
		super(CameraGroup, self).__init__(parent=parent)
		self.camera = camera

	def set_state(self):
		gl.glPushMatrix()
		gl.glTranslatef(-self.camera.x, -self.camera.y, 0)

	def unset_state(self):
		gl.glTranslatef(self.camera.x, self.camera.y, 0)
		gl.glPopMatrix()

	def __eq__(self, other):
		return (self.__class__ is other.__class__ and
		        self.texture == other.__class__)
