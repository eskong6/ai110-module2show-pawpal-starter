from datetime import date, datetime, time, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler


def main() -> None:
    owner = Owner(
        name="Jordan",
        availability=[(time(8, 0), time(20, 0))],
        preferences={"max_daily_time": 180},
    )

    mochi = Pet(name="Mochi", species="cat", age=4)
    panda = Pet(name="Panda", species="dog", age=6)

    owner.add_pet(mochi)
    owner.add_pet(panda)

    today = date.today()

    tasks = [
        Task(
            id="t3",
            title="Medication",
            duration=10,
            priority=4,
            pet_id="Panda",
            earliest=datetime.combine(today, time(12, 0)),
            latest=datetime.combine(today, time(13, 0)),
            recurrence="daily",
        ),
        Task(
            id="t1",
            title="Morning walk",
            duration=30,
            priority=3,
            pet_id="Panda",
            earliest=datetime.combine(today, time(8, 30)),
            latest=datetime.combine(today, time(10, 0)),
            recurrence="daily",
        ),
        Task(
            id="t2",
            title="Feed breakfast",
            duration=15,
            priority=5,
            pet_id="Mochi",
            earliest=datetime.combine(today, time(8, 0)),
            latest=datetime.combine(today, time(9, 0)),
            recurrence="daily",
        ),
        Task(
            id="t4",
            title="Brush teeth",
            duration=10,
            priority=2,
            pet_id="Mochi",
            earliest=datetime.combine(today, time(8, 0)),
            latest=datetime.combine(today, time(8, 30)),
            recurrence="daily",
        ),
    ]

    for task in tasks:
        if task.pet_id == "Mochi":
            mochi.add_task(task)
        else:
            panda.add_task(task)

    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time(today)
    pending_mochi_tasks = scheduler.filter_tasks(pet_name="Mochi", completed=False, on_date=today)

    print("Tasks sorted by time")
    print("====================")
    for task in sorted_tasks:
        print(f"- {task.title} at {task.earliest.strftime('%H:%M')}")

    print("\nPending tasks for Mochi")
    print("========================")
    for task in pending_mochi_tasks:
        print(f"- {task.title}")

    warnings = scheduler.detect_conflicts(today)
    if warnings:
        print("\nConflict warnings")
        print("=================")
        for warning in warnings:
            print(f"- {warning}")

    plan = scheduler.build_plan(today)

    print("Today's Schedule")
    print("=================")
    if not plan:
        print("No tasks scheduled for today.")
        return

    for item in plan:
        start = item["start"].strftime("%H:%M")
        end = item["end"].strftime("%H:%M")
        task = item["task"]
        print(
            f"{start} - {end}: {task.title} ({task.duration} min) [priority: {task.priority}] for {item['pet_name']}"
        )

    print("\nPlan explanation:")
    for line in scheduler.explain_plan(today):
        print(f"- {line}")


if __name__ == "__main__":
    main()
