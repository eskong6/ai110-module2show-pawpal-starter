"""PawPal+ system skeleton: Owner, Pet, Task, Schedule.

This file contains minimal class skeletons (dataclasses for value objects)
used by the app. Methods are left unimplemented as placeholders for logic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Owner:
	name: str
	# availability: list of (start_time, end_time) tuples for a typical day
	availability: List[Tuple[time, time]] = field(default_factory=list)
	# preferences such as max_daily_time, priority_overrides
	preferences: Dict[str, Any] = field(default_factory=dict)

	def is_available(self, window_start: datetime, window_end: datetime) -> bool:
		"""Return True if owner is available for the given datetime window.

		Placeholder implementation.
		"""
		raise NotImplementedError()

	def update_preferences(self, prefs: Dict[str, Any]) -> None:
		"""Merge/update owner preferences.
		"""
		raise NotImplementedError()


@dataclass
class Pet:
	name: str
	species: str
	age: int
	activity_level: str = "medium"
	# feeding_constraints: e.g. preferred feeding times or durations
	feeding_constraints: List[Tuple[time, time]] = field(default_factory=list)

	def preferred_times(self) -> List[Tuple[time, time]]:
		"""Return preferred time windows for pet care tasks.

		Placeholder implementation.
		"""
		raise NotImplementedError()

	def needs_today(self, on_date: date) -> List[str]:
		"""Return a list of care needs for the pet on the given date.

		Placeholder implementation.
		"""
		raise NotImplementedError()


@dataclass
class Task:
	id: str
	title: str
	duration: int  # minutes
	priority: int = 1
	earliest: Optional[datetime] = None
	latest: Optional[datetime] = None
	recurrence: Optional[str] = None  # e.g. 'daily', 'weekly'
	notes: Optional[str] = None

	def conflicts_with(self, other: "Task") -> bool:
		"""Return True if this task conflicts with another task.

		Placeholder implementation.
		"""
		raise NotImplementedError()

	def occurrences_for(self, on_date: date) -> List[datetime]:
		"""Return concrete datetime occurrences for the task on a date.

		Placeholder implementation.
		"""
		raise NotImplementedError()


class Schedule:
	"""Schedule holds a day's planned items and contains light scheduling APIs.

	Items are stored as simple dicts: {"task": Task, "start": datetime,
	"end": datetime, "status": str} to keep the design compact.
	"""

	def __init__(self, on_date: date):
		self.date: date = on_date
		self.items: List[Dict[str, Any]] = []
		self.owner_snapshot: Dict[str, Any] = {}

	def generate(self, tasks: List[Task], owner: Owner, pet: Pet) -> List[Dict[str, Any]]:
		"""Generate a plan for the date from tasks and constraints.

		Returns the list of scheduled items (may be empty).
		"""
		raise NotImplementedError()

	def add_task(self, task: Task) -> None:
		"""Add a task to the internal task list (not yet scheduled).
		"""
		raise NotImplementedError()

	def update_task(self, task_id: str, **attrs: Any) -> None:
		"""Update attributes of a task tracked by the schedule.
		"""
		raise NotImplementedError()

	def remove_task(self, task_id: str) -> None:
		"""Remove a task from the schedule's task collection.
		"""
		raise NotImplementedError()

	def mark_done(self, task_id: str) -> None:
		"""Mark a scheduled item as completed.
		"""
		raise NotImplementedError()


__all__ = ["Owner", "Pet", "Task", "Schedule"]

