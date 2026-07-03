from datetime import date, datetime, time, timedelta
import pytest

from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_duration_validation():
    with pytest.raises(ValueError):
        Task(id="bad", title="Bad task", duration=0)


def test_pet_add_and_tasks_for_date():
    p = Pet(name="Fuzz", species="cat", age=2)
    today = date.today()
    t = Task(
        id="p1",
        title="Feed",
        duration=10,
        priority=3,
        pet_id="Fuzz",
        earliest=datetime.combine(today, time(8, 0)),
        recurrence="daily",
    )
    p.add_task(t)
    tasks = p.tasks_for_date(today)
    assert any(task.id == "p1" for task in tasks)


def test_owner_all_tasks_and_tasks_for_date():
    owner = Owner(name="Sam", availability=[(time(8, 0), time(20, 0))])
    a = Pet(name="A", species="dog", age=4)
    b = Pet(name="B", species="cat", age=3)
    owner.add_pet(a)
    owner.add_pet(b)

    today = date.today()
    t1 = Task(
        id="o1",
        title="Walk",
        duration=20,
        priority=4,
        pet_id="A",
        earliest=datetime.combine(today, time(9, 0)),
        recurrence="daily",
    )
    t2 = Task(
        id="o2",
        title="Feed",
        duration=10,
        priority=5,
        pet_id="B",
        earliest=datetime.combine(today, time(8, 0)),
        recurrence="daily",
    )
    a.add_task(t1)
    b.add_task(t2)

    all_tasks = owner.all_tasks()
    assert len(all_tasks) == 2
    tasks_today = owner.tasks_for_date(today)
    ids = {t.id for t in tasks_today}
    assert "o1" in ids and "o2" in ids


def test_scheduler_build_plan():
    owner = Owner(name="Lee", availability=[(time(8, 0), time(20, 0))])
    p1 = Pet(name="P1", species="dog", age=5)
    p2 = Pet(name="P2", species="cat", age=2)
    owner.add_pet(p1)
    owner.add_pet(p2)

    today = date.today()
    t_high = Task(
        id="t_high",
        title="HighPriority",
        duration=15,
        priority=10,
        pet_id="P1",
        earliest=datetime.combine(today, time(8, 0)),
        recurrence="daily",
    )
    t_low = Task(
        id="t_low",
        title="LowPriority",
        duration=30,
        priority=1,
        pet_id="P2",
        earliest=datetime.combine(today, time(8, 30)),
        recurrence="daily",
    )

    p1.add_task(t_high)
    p2.add_task(t_low)

    scheduler = Scheduler(owner=owner)
    plan = scheduler.build_plan(today)

    assert isinstance(plan, list)
    assert any(item["task"].id == "t_high" for item in plan)
    assert any(item["task"].id == "t_low" for item in plan)

    # high priority should come before low priority
    ids_order = [item["task"].id for item in plan]
    assert ids_order.index("t_high") < ids_order.index("t_low")


def test_task_mark_complete_changes_status():
    t = Task(id="complete1", title="Do it", duration=5)
    assert not t.is_complete()
    t.mark_complete()
    assert t.is_complete()


def test_pet_add_task_increases_count():
    p = Pet(name="Tester", species="other", age=1)
    initial = len(p.tasks)
    new_task = Task(id="nt1", title="New", duration=10)
    p.add_task(new_task)
    assert len(p.tasks) == initial + 1


def test_scheduler_sort_and_filter_tasks():
    owner = Owner(name="Sam", availability=[(time(8, 0), time(20, 0))])
    pet = Pet(name="Mochi", species="cat", age=4)
    owner.add_pet(pet)

    today = date.today()
    task1 = Task(
        id="t1",
        title="Morning walk",
        duration=20,
        priority=3,
        pet_id="Mochi",
        earliest=datetime.combine(today, time(10, 0)),
    )
    task2 = Task(
        id="t2",
        title="Feed breakfast",
        duration=10,
        priority=5,
        pet_id="Mochi",
        earliest=datetime.combine(today, time(8, 0)),
    )
    task3 = Task(
        id="t3",
        title="Medication",
        duration=10,
        priority=4,
        pet_id="Mochi",
        earliest=datetime.combine(today, time(9, 0)),
    )
    task3.mark_complete()

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    scheduler = Scheduler(owner=owner)
    sorted_ids = [task.id for task in scheduler.sort_by_time(on_date=today)]
    assert sorted_ids == ["t2", "t3", "t1"]

    filtered = scheduler.filter_tasks(pet_name="Mochi", completed=False, on_date=today)
    assert [task.id for task in filtered] == ["t1", "t2"]


def test_mark_complete_creates_next_occurrence_for_daily_task():
    today = date.today()
    task = Task(
        id="daily1",
        title="Water",
        duration=5,
        pet_id="Mochi",
        earliest=datetime.combine(today, time(8, 0)),
        recurrence="daily",
    )

    next_task = task.mark_complete(on_date=today)

    assert task.status == "done"
    assert next_task is not None
    assert next_task.recurrence == "daily"
    assert next_task.earliest == datetime.combine(today + timedelta(days=1), time(8, 0))


def test_sorting_chronological_order():
    """Verify tasks are returned in chronological order by earliest time."""
    owner = Owner(name="Test", availability=[(time(7, 0), time(22, 0))])
    pet = Pet(name="Buddy", species="dog", age=3)
    owner.add_pet(pet)

    today = date.today()
    # Create tasks out of order
    task_morning = Task(
        id="morning",
        title="Morning walk",
        duration=20,
        priority=2,
        pet_id="Buddy",
        earliest=datetime.combine(today, time(7, 0)),
    )
    task_afternoon = Task(
        id="afternoon",
        title="Afternoon nap",
        duration=30,
        priority=2,
        pet_id="Buddy",
        earliest=datetime.combine(today, time(14, 0)),
    )
    task_evening = Task(
        id="evening",
        title="Evening play",
        duration=15,
        priority=2,
        pet_id="Buddy",
        earliest=datetime.combine(today, time(18, 0)),
    )

    pet.add_task(task_afternoon)
    pet.add_task(task_evening)
    pet.add_task(task_morning)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(on_date=today)

    # Verify chronological order
    times = [task.earliest.time() for task in sorted_tasks]
    assert times == [time(7, 0), time(14, 0), time(18, 0)]


def test_conflict_detection_duplicate_times():
    """Verify scheduler detects and flags tasks with exact start-time conflicts."""
    owner = Owner(name="Alex", availability=[(time(8, 0), time(20, 0))])
    pet1 = Pet(name="Spot", species="dog", age=5)
    pet2 = Pet(name="Whiskers", species="cat", age=3)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    today = date.today()
    conflict_time = datetime.combine(today, time(9, 0))

    task_dog = Task(
        id="dog_task",
        title="Dog walk",
        duration=20,
        priority=3,
        pet_id="Spot",
        earliest=conflict_time,
    )
    task_cat = Task(
        id="cat_task",
        title="Cat feed",
        duration=10,
        priority=3,
        pet_id="Whiskers",
        earliest=conflict_time,
    )

    pet1.add_task(task_dog)
    pet2.add_task(task_cat)

    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts(on_date=today)

    # Should detect the conflict
    assert len(conflicts) > 0
    assert any("Conflict" in msg and "9:00" in msg for msg in conflicts)


def test_recurrence_weekly_task_creates_next():
    """Verify marking a weekly task complete creates next-week instance."""
    today = date.today()
    task = Task(
        id="weekly_grooming",
        title="Grooming",
        duration=45,
        pet_id="Fluffy",
        earliest=datetime.combine(today, time(10, 0)),
        recurrence="weekly",
    )

    next_task = task.mark_complete(on_date=today)

    assert task.status == "done"
    assert next_task is not None
    assert next_task.recurrence == "weekly"
    expected_date = today + timedelta(days=7)
    assert next_task.earliest == datetime.combine(expected_date, time(10, 0))
