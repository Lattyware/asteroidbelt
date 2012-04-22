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

Interface related stuff.
"""

from pyglet import sprite
from pyglet import text

class Button(object):
	def __init__(self, x, y, image, description, callback, group, batch):
		self.sprite = sprite.Sprite(image, x, y, batch=batch, group=group)
		self.x1 = self.sprite.x-self.sprite.width/2
		self.y1 = self.sprite.y-self.sprite.height/2
		self.x2 = self.x1+self.sprite.width
		self.y2 = self.y1+self.sprite.height
		self.callback = callback
		self.document = text.document.UnformattedDocument(description)
		self.document.set_style(0, 0, {"color": (255, 255, 255, 255), "background_color": (0, 0, 0, 100)})
		self.description = text.layout.TextLayout(self.document, 200, None, True, batch=batch, group=group)
		self.description.x = x+self.sprite.width/2+10
		self.description.y = y
		self.on_mouse_leave()

	def disable(self):
		self.sprite.color = (200, 200, 200)

	def using(self):
		self.sprite.color = (255, 0, 0)

	def normal(self):
		self.sprite.color = (255, 255, 255)

	def point_over(self, x, y):
		return self.x1 < x < self.x2 and self.y1 < y < self.y2

	def on_mouse_over(self):
		self.document.set_style(0, 0, {"color": (255, 255, 255, 255), "background_color": (0, 0, 0, 100)})

	def on_mouse_leave(self):
		self.document.set_style(0, 0, {"color": (0, 0, 0, 0), "background_color": (0, 0, 0, 0)})

	def on_click(self, x, y, button, modifiers):
		pass

