# Asteroid Belt - Lattyware's Ludum Dare #23 entry.

This is my entry for Ludum Dare #23 - Asteroid Belt, a game on the theme of
'Tiny World' produced in 48 hours.

## Gameplay

You play as a man fed up of living on an asteroid, find your way to the edge
of the asteroid belt, and to a real planet.

## What was going to be the gameplay

You play as a race of people living on an asteroid belt. While you manage to
survive, the lack of natural resources and the small asteroids make for poor
living conditions. You look towards a habitable planet in your solar system,
where you can settle.

Your aim is to build a spaceship and fly there, however, to be successful you
will need to build your spaceship from resources scattered across asteroids,
clear a path through the asteroids for it, and aim it correctly.

Asteroids contain a number of resources. Your home planet contains no resources,
as they have been consumed by past generations of your people. All that remains
is the rocket pad you have built. Other asteroids contain a variety of
resources:

* Water - Used to grow food and sustain your people.
* Oil - Used to make plastics. 
* Uranium - Used to produce power.
* Aluminium - Used to make light metalic items.
* Titanium - Used to make strong metalic items.

You will begin with meagre stockpiles of these resources, allowing you to build
a variety of items to get to, and interact with asteroids:

* Drill - Used to get to resources.
* Push - Used to move an asteroid.
* Nuclear Bomb - Used to destroy an asteroid.

Watch out - asteroids are inherantly unstable, and you only collect resources
from asteroids which are connected to your home asteroid. Good luck!

## Notes

Well, at the last minute the gameplay mechnaics fell apart - a lot of the
gameplay for the actual game is done, but not enough to be playable, so I
canibalised it into this. It's nothing great, but it is technically a game.

As usual, this isn't as polished as I'd like - 48 hours is not a long time, so
please don't judge me too harshly. Likewise, the code isn't as elegant or well
documented as I'd like - but this is to be expected.

I switched to pyglet from sfml2 for this due to sfml2 not being very easy to
install as a dependancy - it all requires compiling from git repos, and the
python bindings require cython - it becomes a big pain, so I decided to use
something else until they are ready. Still like SFML, it's a great library, but
it's simply not as easy to distribute. Unfortunately this means I'm stuck on
Python 2.x, when I'd rather be on 3.x, but so it goes.

I also decided to use pymunk for physics - I hadn't used it before, but it's a
nice library - if a little sparse in the documentation.

## TODO

* Tools
* Resources
* People
* More resources.
* More tools.
* Moving starfield.
* Ensure that the home asteroid is not next to the target.
* Ensure that the home asteroid points away from the target.

## Requirements:

* [Python 2.7.3](http://www.python.org/)
* [pyglet 1.1.4](http://www.pyglet.org/)
* [pymunk 2.1.0](https://code.google.com/p/pymunk/)

## Usage:

If you want to play the game only, I highly advice getting a binary version of
the game from [my website](http://www.lattyware.co.uk/projects/ld23). These have
the dependancies packaged with them, and are easier to simply get and play. Then
simply run the executable. Under linux, simply check the executable bit has been
set (`chmod +x ld23`) and then do `./ld23`. Under Windows double click
`ld23.exe`.

To run the game from source, run `main.py` with Python. Under most linux
distributions, simply `python2 main.py` or `python main.py` depending on what
the main version of python for your distribution is. Under windows, you will
probably need to add python to your system path - see [the official python
documentation](http://docs.python.org/faq/windows.html#how-do-i-run-a-python-program-under-windows)
for more.

## Author:

* Name: Gareth Latty
* Email: <gareth@lattyware.co.uk>
* Website: <http://www.lattyware.co.uk>
* Twitter: [@lattyware](https://twitter.com/#!/lattyware)
* Blog: <http://blog.lattyware.co.uk>

Please feel free to contact me, I'm always happy to hear from people.

## Things I Used:

* [PyCharm](http://www.jetbrains.com/pycharm/) as my IDE. It's a great
Python IDE, and while Python, as a language, does a great job at reducing the
need for an IDE, PyCharm fills in the gaps most text editors don't - good
project management, SCM integration, refactoring tools, etc... If you are
looking for a Python IDE, I reccomend it.

* [Arch Linux](https://www.archlinux.org/) is my operating system of choice.
Great distro if you want a lot of control over your system.

## Licence:

Copyright © 2012: Gareth Latty <gareth@lattyware.co.uk>

This game's source code is provided under the GPLv3 licence, see LICENCE or
<http://www.gnu.org/licenses/> for more.

All other assets are provided under a
Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) licence -
see <https://creativecommons.org/licenses/by-sa/3.0/>.