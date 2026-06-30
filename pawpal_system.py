"""PawPal+ system: Owner, Pet, Task, Scheduler.

This file contains the core domain model for the PawPal+ app. It provides
owner and pet state, task representation, and a light scheduler for day
planning.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Task:
    id: str
    title: str
    duration: int  # minutes
    priority: int = 1
    pet_id: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    earliest: Optional[datetime] = None
    latest: Optional[datetime] = None
    recurrence: Optional[str] = None  # e.g. 'daily', 'weekly'
    notes: Optional[str] = None
    status: str = "pending"

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        if self.duration <= 0:
            raise ValueError("Task duration must be a positive integer")

    def conflicts_with(self, other: "Task") -> bool:
        """Return True if this task's scheduled time overlaps another's."""
        if self.scheduled_at is None or other.scheduled_at is None:
            return False

        self_end = self.scheduled_at + timedelta(minutes=self.duration)
        other_end = other.scheduled_at + timedelta(minutes=other.duration)
        return not (self_end <= other.scheduled_at or other_end <= self.scheduled_at)

    def is_complete(self) -> bool:
        """Return True when the task status is marked as done."""
        return self.status.lower() == "done"

    def mark_complete(self, on_date: Optional[date] = None) -> Optional["Task"]:
        """Mark the task as completed and optionally create the next recurring instance."""
        self.status = "done"

        if self.recurrence not in {"daily", "weekly"}:
            return None

        if on_date is None:
            on_date = date.today()

        if self.recurrence == "daily":
            next_date = on_date + timedelta(days=1)
        else:
            next_date = on_date + timedelta(days=7)

        next_earliest = (
            datetime.combine(next_date, self.earliest.time())
            if self.earliest is not None
            else datetime.combine(next_date, time(0, 0))
        )
        next_latest = (
            datetime.combine(next_date, self.latest.time())
            if self.latest is not None
            else None
        )

        return Task(
            id=f"{self.id}-next",
            title=self.title,
            duration=self.duration,
            priority=self.priority,
            pet_id=self.pet_id,
            scheduled_at=None,
            earliest=next_earliest,
            latest=next_latest,
            recurrence=self.recurrence,
            notes=self.notes,
            status="pending",
        )

    def occurrences_for(self, on_date: date) -> List[datetime]:
        """Return concrete datetime occurrences of this task for a given date."""
        results: List[datetime] = []

        if self.recurrence == "daily" and self.earliest:
            results.append(datetime.combine(on_date, self.earliest.time()))
        elif self.recurrence == "weekly" and self.earliest:
            if self.earliest.weekday() == on_date.weekday():
                results.append(datetime.combine(on_date, self.earliest.time()))
        elif self.scheduled_at and self.scheduled_at.date() == on_date:
            results.append(self.scheduled_at)
        elif self.earliest and self.earliest.date() == on_date:
            results.append(self.earliest)

        return results


@dataclass
class Pet:
    name: str
    species: str
    age: int
    activity_level: str = "medium"
    feeding_constraints: List[Tuple[time, time]] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a Task to this pet, setting its pet_id if absent."""
        if task.pet_id is None:
            task.pet_id = self.name
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task from this pet by its identifier."""
        self.tasks = [task for task in self.tasks if task.id != task_id]

    def preferred_times(self) -> List[Tuple[time, time]]:
        """Return preferred time windows for this pet's care tasks."""
        if self.feeding_constraints:
            return self.feeding_constraints

        species = self.species.lower()
        if species == "dog":
            return [(time(7, 0), time(9, 0)), (time(17, 0), time(19, 0))]
        if species == "cat":
            return [(time(8, 0), time(10, 0)), (time(18, 0), time(20, 0))]

        return [(time(9, 0), time(17, 0))]

    def needs_today(self, on_date: date) -> List[str]:
        """List care need titles for tasks occurring on the given date."""
        return [task.title for task in self.tasks if task.occurrences_for(on_date) and not task.is_complete()]

    def tasks_for_date(self, on_date: date) -> List[Task]:
        """Return Task objects for this pet that occur on the given date."""
        return [task for task in self.tasks if task.occurrences_for(on_date)]


@dataclass
class Owner:
    name: str
    availability: List[Tuple[time, time]] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to this owner's collection of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet from the owner by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def all_tasks(self) -> List[Task]:
        """Return all Task objects for every pet owned by this owner."""
        return [task for pet in self.pets for task in pet.tasks]

    def tasks_by_priority(self, reverse: bool = False) -> List[Task]:
        """Return all tasks sorted by priority (optionally reversed)."""
        return sorted(self.all_tasks(), key=lambda task: task.priority, reverse=reverse)

    def tasks_for_date(self, on_date: date) -> List[Task]:
        """Return all tasks across pets that occur on the given date."""
        return [task for task in self.all_tasks() if task.occurrences_for(on_date)]

    def is_available(self, window_start: datetime, window_end: datetime) -> bool:
        """Return True if owner is available for the given datetime window."""
        if window_end <= window_start:
            return False

        if not self.availability:
            return True

        for start_time, end_time in self.availability:
            available_start = datetime.combine(window_start.date(), start_time)
            available_end = datetime.combine(window_start.date(), end_time)
            if available_start <= window_start and window_end <= available_end:
                return True

        return False

    def update_preferences(self, prefs: Dict[str, Any]) -> None:
        """Merge provided preferences into the owner's preference map."""
        self.preferences.update(prefs)


class Scheduler:
    def __init__(self, owner: Owner, default_start: time = time(8, 0), default_end: time = time(20, 0)):
        self.owner = owner
        self.default_start = default_start
        self.default_end = default_end
        self.plans: Dict[date, List[Dict[str, Any]]] = {}
        """Initialize a Scheduler for the given owner and daily bounds."""

    def retrieve_tasks(self, on_date: date) -> List[Task]:
        """Retrieve tasks for the owner that have occurrences on the date."""
        return [task for task in self.owner.all_tasks() if task.occurrences_for(on_date)]

    def sorted_tasks(self, on_date: date) -> List[Task]:
        """Return tasks for the date sorted by priority, then duration and title."""
        tasks = self.retrieve_tasks(on_date)
        return sorted(tasks, key=lambda task: (-task.priority, task.duration, task.title))

    def sort_by_time(self, on_date: Optional[date] = None) -> List[Task]:
        """Return tasks sorted by their start time, then by title for readability.

        If a task has an earliest datetime, that value is used; otherwise the
        scheduled time is used. Tasks without either time fall back to a late
        default value so they still sort predictably.
        """
        tasks = self.retrieve_tasks(on_date) if on_date is not None else self.owner.all_tasks()
        return sorted(
            tasks,
            key=lambda task: (
                task.earliest.time() if task.earliest else task.scheduled_at.time() if task.scheduled_at else time(23, 59),
                task.title,
            ),
        )

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        on_date: Optional[date] = None,
    ) -> List[Task]:
        """Return tasks filtered by pet name, completion status, and optional date.

        Passing None for a filter leaves that criterion unchanged, which keeps the
        method simple and easy to reuse in the CLI or UI.
        """
        tasks = self.retrieve_tasks(on_date) if on_date is not None else self.owner.all_tasks()

        if pet_name:
            tasks = [task for task in tasks if task.pet_id == pet_name]

        if completed is not None:
            tasks = [task for task in tasks if task.is_complete() is completed]

        return tasks

    def detect_conflicts(self, on_date: Optional[date] = None) -> List[str]:
        """Return lightweight warning messages for tasks that start at the same time.

        This is a simple, readable check for obvious scheduling collisions. It
        avoids heavier overlap logic while still surfacing conflicts clearly.
        """
        tasks = self.retrieve_tasks(on_date) if on_date is not None else self.owner.all_tasks()
        warnings: List[str] = []

        for index, first in enumerate(tasks):
            for second in tasks[index + 1 :]:
                if first.pet_id is None or second.pet_id is None:
                    continue

                first_start = first.earliest or first.scheduled_at
                second_start = second.earliest or second.scheduled_at
                if first_start is None or second_start is None:
                    continue

                if first_start == second_start:
                    warnings.append(
                        f"Conflict: {first.title} ({first.pet_id}) and {second.title} ({second.pet_id}) both start at {first_start.strftime('%H:%M')}."
                    )

        return warnings

    def daily_time_bounds(self, on_date: date) -> Tuple[datetime, datetime]:
        """Return the scheduling window (start,end) for the owner on the date."""
        if self.owner.availability:
            start_time, end_time = self.owner.availability[0]
            return datetime.combine(on_date, start_time), datetime.combine(on_date, end_time)

        return datetime.combine(on_date, self.default_start), datetime.combine(on_date, self.default_end)

    def build_plan(self, on_date: date) -> List[Dict[str, Any]]:
        """Construct a simple sequential plan of tasks for the given date."""
        window_start, window_end = self.daily_time_bounds(on_date)
        current = window_start
        schedule: List[Dict[str, Any]] = []

        for task in self.sorted_tasks(on_date):
            if task.is_complete():
                continue

            if task.earliest and task.earliest.date() == on_date and task.earliest > current:
                task_start = task.earliest
            elif task.scheduled_at and task.scheduled_at.date() == on_date:
                task_start = task.scheduled_at
            else:
                task_start = current

            task_end = task_start + timedelta(minutes=task.duration)

            if task.latest and task.latest.date() == on_date and task_end > task.latest:
                continue

            if task_end > window_end:
                continue

            if not self.owner.is_available(task_start, task_end):
                continue

            schedule.append(
                {
                    "task": task,
                    "start": task_start,
                    "end": task_end,
                    "status": task.status,
                    "pet_name": task.pet_id or "Unknown",
                }
            )
            current = task_end

        self.plans[on_date] = schedule
        return schedule

    def add_task(self, pet_name: str, task: Task) -> None:
        """Add a Task to the named pet owned by the scheduler's owner."""
        pet = next((pet for pet in self.owner.pets if pet.name == pet_name), None)
        if pet is None:
            raise KeyError(f"Pet '{pet_name}' not found")
        pet.add_task(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a Task by id from whichever pet currently has it."""
        removed = False
        for pet in self.owner.pets:
            if any(task.id == task_id for task in pet.tasks):
                pet.remove_task(task_id)
                removed = True
        if not removed:
            raise KeyError(f"Task '{task_id}' not found")

    def mark_task_done(self, task_id: str, on_date: Optional[date] = None) -> Optional[Task]:
        """Find a task by id, mark it completed, and create the next recurring instance if needed."""
        for task in self.owner.all_tasks():
            if task.id == task_id:
                next_task = task.mark_complete(on_date=on_date)
                if next_task is not None:
                    pet = next((pet for pet in self.owner.pets if pet.name == task.pet_id), None)
                    if pet is not None:
                        pet.add_task(next_task)
                return next_task
        raise KeyError(f"Task '{task_id}' not found")

    def explain_plan(self, on_date: date) -> List[str]:
        """Return a human-readable explanation for the computed plan on date."""
        plan = self.plans.get(on_date, [])
        return [
            f"{item['start'].strftime('%H:%M')} — {item['task'].title} ({item['task'].duration} min) [priority: {item['task'].priority}] for {item['pet_name']}"
            for item in plan
        ]


__all__ = ["Owner", "Pet", "Task", "Scheduler"]

