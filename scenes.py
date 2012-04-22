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

Segments of the game.
"""

from __future__ import division

from random import choice
from random import triangular
from operator import attrgetter

from pyglet import sprite
from pyglet import resource
from pyglet import graphics
from pyglet import window

from pymunk import Body
from pymunk import Space
from pymunk import Segment
from pymunk import BB

from physics import Size
from physics import Vector
from entities import Stars
from entities import Asteroid
from graphics import centre_image
from graphics import Camera
from graphics import CameraGroup
from tools import Tool
from ui import Button
from entities import Person

class Scene(object):
	"""A base object for scenes in the game. A scene is a segment of the game -
	e.g: a menu or a level."""

	def _load(self, size, window):
		"""Called when the scene needs to be loaded. This will happen just
		before the scene is displayed to the user. This calls :func:`load`_.

		:param size: ``(width, height) collections.namedtuple - the size of the
					 rendering space.
		"""
		self.size = size
		self.window = window
		self.next = False
		self.load()

	def load(self):
		"""Called when the scene needs to be loaded. This will happen just
		before the scene is displayed to the user.
		"""
		raise NotImplementedError

	def update(self):
		"""Called to update the state of the scene."""
		raise NotImplementedError

	def draw(self):
		"""Called to draw the scene to screen."""
		raise NotImplementedError

	def mouse_pressed(self, x, y, button, modifiers):
		raise NotImplementedError

	def key_pressed(self, x, y, symbol, modifiers):
		raise NotImplementedError

	def mouse_motion(self, x, y, dx, dy):
		raise NotImplementedError

	def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		raise NotImplementedError

	def end(self, next=True):
		self.next = next

class Intro(Scene):

	FADE_SPEED = 75

	def load(self):
		centre = Vector(self.size.width/2, self.size.height/2)
		image = centre_image(resource.image("lattyware.png"))
		self.logo = sprite.Sprite(image, centre.x, centre.y)
		self.logo.opacity = 0
		self.fade = 0
		self.fade_in = True

	def update(self, frame_time):
		if self.fade_in:
			self.fade += frame_time*Intro.FADE_SPEED
			if self.fade >= 255:
				self.fade_in = False
				self.fade = 255
			self.logo.opacity = self.fade
		else:
			self.fade -= frame_time*Intro.FADE_SPEED
			if self.fade <= 0:
				self.end(Main())
			self.logo.opacity = self.fade

	def draw(self):
		self.logo.draw()

	def mouse_pressed(self, x, y, button, modifiers):
		self.end(Main())

	def key_pressed(self, x, y, symbol, modifiers):
		self.end(Main())

	def mouse_motion(self, x, y, dx, dy):
		pass

	def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass

class Main(Scene):

	FADE_SPEED = 75

	def load(self):
		self.world_size = Size(3000, 3000)

		self.camera = Camera(self.size, self.world_size, 1000, 10)

		self._tool = None
		self.tool = None

		self.batch = graphics.Batch()
		self.background = CameraGroup(graphics.OrderedGroup(0), self.camera)
		self.foreground = CameraGroup(graphics.OrderedGroup(1), self.camera)
		self.playerg = CameraGroup(graphics.OrderedGroup(2), self.camera)
		self.world_ui = CameraGroup(graphics.OrderedGroup(3), self.camera)
		self.ui = graphics.OrderedGroup(2)

		self.space = Space()
		self.space.gravity = (0.0, 0.0)
		buffer = 100
		borders = Body()
		borders.position = (0, 0)
		left = Segment(borders, (-buffer, -buffer), (-buffer, self.world_size.height+buffer), buffer)
		bottom = Segment(borders, (-buffer, -buffer), (self.world_size.width+buffer, -buffer), buffer)
		right = Segment(borders, (self.world_size.width+buffer, self.world_size.height+buffer),
			(self.world_size.width+buffer, -buffer), buffer)
		top = Segment(borders, (self.world_size.width+buffer, self.world_size.height+buffer),
			(-buffer, self.world_size.height+buffer), buffer)
		self.space.add_static(left, bottom, right, top)

		self.stars = Stars(self.world_size, self.batch, self.background)

		self.asteroids = Asteroid.populate(50, 100, self.world_size, self.batch, self.foreground, self.space)

		if not self.asteroids:
			print("None of a particular resource on this asteroid belt, that'd be unfair. Trying again.")
			self.end(Main())
			return

		self.home_world = choice([asteroid for asteroid in self.asteroids if asteroid.position.y > self.world_size.height/4*3])
		self.home_world.type = "home"
		self.home_world.populated = True

		x, y = self.home_world.position
		self.camera.move(Vector(x-self.size.width/2, y-self.size.height/2))

		# Let's make stuff a bit more interesting.
		for asteroid in self.asteroids:
			if not asteroid.type == "home":
				asteroid.body.apply_impulse((triangular(-20000, 20000, 0), triangular(-20000, 20000, 0)))

		x, y = self.home_world.position
		self.player = Person(x+150, y+150, self.batch, self.playerg, self.space)
		self.mouse = x+150, y+150

		centre = Vector(self.size.width/2, self.size.height/2)
		image = centre_image(resource.image("logo.png"))
		self.logo = sprite.Sprite(image, centre.x, centre.y, batch=self.batch, group=self.ui)
		self.logo.opacity = 255
		self.fade = True
		self.faded = False

		planet = centre_image(resource.image("planet.png"))
		x = self.world_size.width/2
		y = planet.height/2
		self.planet_sprite = sprite.Sprite(planet, x, y, batch=self.batch, group=self.world_ui)
		self.win_box = BB(x-200, y-200, x+200, y+200)

		#self.tools = sorted([tool(self.space) for tool in Tool.__subclasses__()], key=attrgetter("order"), reverse=True)
		#self.buttons = {tool: Button(30, 30+number*50, tool.image, tool.description, self.use_tool(tool), self.ui, self.batch) for number, tool in enumerate(self.tools)}

		self.constraints = set()

	def use_tool(self, tool):
		"""For callback usage."""
		def f():
		  self.tool = tool
		return f

	@property
	def tool(self):
		return self._tool

	@tool.setter
	def tool(self, tool):
		if tool:
			if self._tool and not self._tool == tool:
				self._tool.end_selecting()
				self.buttons[self._tool].normal()
				self.window.set_mouse_cursor(self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT))
				self.selecting = False
				self.selection = []
			self.window.set_mouse_cursor(self.window.get_system_mouse_cursor(self.window.CURSOR_CROSSHAIR))
			self.selecting = True
			self.buttons[tool].using()
		else:
			if self._tool:
				self._tool.end_selecting()
				self.buttons[self._tool].normal()
			self.window.set_mouse_cursor(self.window.get_system_mouse_cursor(self.window.CURSOR_DEFAULT))
			self.selecting = False
			self.selection = []
		self._tool = tool

	def key_pressed(self, symbol, modifiers):
		self.fade = True
		#self.camera.key_pressed(symbol)

	def key_released(self, symbol, modifiers):
		pass
		#self.camera.key_released(symbol)

	def mouse_pressed(self, x, y, key, modifiers):
		self.fade = True
		#for button in self.buttons.values():
		#	if button.point_over(x, y):
		#		button.callback()
		#		return
		if self.selecting:
			for asteroid in self.asteroids:
				clicked = self.camera.translate(x, y)
				if asteroid.point_over(*clicked):
					self.selection.append((asteroid, clicked))
					self.tool = self.tool.selection(self.selection, self.constraints)
					return
			self.tool = None
			return

	def mouse_motion(self, x, y, dx, dy):
		self.mouse = self.camera.translate(x, y)
		#for button in self.buttons.values():
	#		if button.point_over(x, y):
	#			button.on_mouse_over()
	#		else:
	#			button.on_mouse_leave()

	def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		if buttons & window.mouse.RIGHT:
			self.camera.mouse_dragged(dx, dy)

	def update(self, frame_time):
		self.constraints = {constraint for constraint in self.constraints if not constraint.update(self.batch, self.foreground)}
		if self.fade and not self.faded:
			self.logo.opacity -= Main.FADE_SPEED*frame_time
			if self.logo.opacity < 0:
				self.logo.opacity = 0
				del self.logo
				self.faded = True
		self.player.target = self.mouse
		self.player.update()
		x, y = self.player.body.position
		self.camera.x, self.camera.y = x-self.size.width/2, y-self.size.height/2
		self.camera.update(frame_time)
		self.space.step(1/60)
		if self.win_box.contains_vect(self.player.body.position):
			self.end(Win())

	def draw(self):
		self.batch.draw()

class Win(Scene):

	def load(self):
		self.batch = graphics.Batch()
		self.background = graphics.OrderedGroup(0)
		self.stars = Stars(Size(2000, 2000), self.batch, self.background)
		centre = Vector(self.size.width/2, self.size.height/2)
		image = centre_image(resource.image("win.png"))
		self.logo = sprite.Sprite(image, centre.x, centre.y)

	def update(self, frame_time):
		pass

	def draw(self):
		self.batch.draw()
		self.logo.draw()

	def mouse_pressed(self, x, y, button, modifiers):
		self.end(True)

	def key_pressed(self, x, y, symbol, modifiers):
		self.end(True)

	def mouse_motion(self, x, y, dx, dy):
		pass

	def mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass
