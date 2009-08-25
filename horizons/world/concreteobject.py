# ###################################################
# Copyright (C) 2009 The Unknown Horizons Team
# team@unknown-horizons.org
# This file is part of Unknown Horizons.
#
# Unknown Horizons is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# ###################################################

import horizons.main

from horizons.util import WorldObject

class ConcretObject(WorldObject):
	"""Class for concrete objects like Units or Buildings.
	"Concrete" here means "you can touch it", e.g. a Branch Office is a ConcreteObject,
	a Settlement isn't.
	All such objects have positions, so Islands are no ConcreteObjects for technical reasons.

	Assumes that object has a member _instance.
	"""
	def __init__(self, **kwargs):
		super(ConcretObject, self).__init__(**kwargs)

	def act(self, action, facing_loc=None, repeating=False):
		if facing_loc is None:
			facing_loc = self._instance.getFacingLocation()
		if not self.has_action(action):
			action = 'idle'
		self._instance.act(action+"_"+str(self._action_set_id), facing_loc, repeating)

	def has_action(self, action):
		"""Checks if this unit has a certain action.
		@param anim: animation id as string"""
		return (action in horizons.main.action_sets[self._action_set_id])

	def remove(self):
		self._instance.getLocationRef().getLayer().deleteInstance(self._instance)
		self._instance = None
		horizons.main.session.scheduler.rem_all_classinst_calls(self)
		super(ConcretObject, self).remove()