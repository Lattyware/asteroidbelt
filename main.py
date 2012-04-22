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

A game for Ludum Dare #23, produced in 48 hours.
"""

from __future__ import division

import sys

from pyglet import app
from pyglet import window
from pyglet import resource
from pyglet import clock
from pyglet import options
from pyglet import gl

from scenes import Intro
from physics import Size

class Game(window.Window):
	"""Handles the running of the game."""
	
	def __init__(self, first, *args):
		"""
		:param first: The first scene to begin on.
		"""
		try:
			super(Game, self).__init__(*args, config = gl.Config(sample_buffers=1, samples=4))
		except window.NoSuchConfigException:
			print("Anti-aliasing not supported. It won't look quite so good, but who cares, the graphics suck anyway.")
			super(Game, self).__init__(*args)
		resource.path.append("assets")
		resource.reindex()
		self.scene = first
		clock.schedule_interval(self.update, 1/60)

	@property
	def scene(self):
		return self._scene

	@scene.setter
	def scene(self, scene):
		next = scene
		while next:
			scene = next
			next._load(Size(self.width, self.height), self)
			next = next.next
		self._scene = scene

	def on_draw(self):
		self.clear()
		self.scene.draw()

	def update(self, frame_time):
		self.scene.update(frame_time)
		if self.scene.next:
			if self.scene.next is True:
				self.end()
			self.scene = self.scene.next

	def on_mouse_press(self, x, y, button, modifiers):
		self.scene.mouse_pressed(x, y, button, modifiers)

	def on_key_press(self, symbol, modifiers):
		self.scene.key_pressed(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		self.scene.key_released(symbol, modifiers)

	def on_mouse_motion(self, x, y, dx, dy):
		self.scene.mouse_motion(x, y, dx, dy)

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.scene.mouse_drag(x, y, dx, dy, buttons, modifiers)

	def end(self):
		sys.exit()

#options['debug_gl'] = False
window = Game(Intro(), 1024, 768, "Asteroid Belt - Lattyware's Ludum Dare #23 Entry")
app.run()

