# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

# Today's Schedule

08:00 - 08:15: Feed breakfast (15 min) [priority: 5] for Mochi
12:00 - 12:10: Medication (10 min) [priority: 4] for Panda

Plan explanation:

- 08:00 — Feed breakfast (15 min) [priority: 5] for Mochi
- 12:00 — Medication (10 min) [priority: 4] for Panda

## 🧪 Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

### Test Coverage

The test suite includes **11 comprehensive tests** covering:

- **Sorting Correctness:** Verifies tasks are returned in chronological order by earliest time.
- **Recurrence Logic:** Confirms that marking daily and weekly tasks complete creates new instances for the next day/week.
- **Conflict Detection:** Verifies that the `Scheduler` flags tasks with exact start-time conflicts.
- **CRUD Operations:** Tests adding, removing, and filtering tasks by pet, completion status, and date.
- **Priority & Duration Sorting:** Ensures higher priority tasks are scheduled before lower ones.
- **Owner Availability:** Validates that tasks respect owner time windows.

### Sample Test Output

```
============================= test session starts ==============================
platform win32 -- Python 3.14.4, pytest-9.0.3, pluggy-1.6.0
collected 11 items

tests/test_pawpal.py::test_task_duration_validation PASSED               [  9%]
tests/test_pawpal.py::test_pet_add_and_tasks_for_date PASSED             [ 18%]
tests/test_pawpal.py::test_owner_all_tasks_and_tasks_for_date PASSED     [ 27%]
tests/test_pawpal.py::test_scheduler_build_plan PASSED                   [ 36%]
tests/test_pawpal.py::test_task_mark_complete_changes_status PASSED      [ 45%]
tests/test_pawpal.py::test_pet_add_task_increases_count PASSED           [ 54%]
tests/test_pawpal.py::test_scheduler_sort_and_filter_tasks PASSED        [ 63%]
tests/test_pawpal.py::test_mark_complete_creates_next_occurrence_for_daily_task PASSED [ 72%]
tests/test_pawpal.py::test_sorting_chronological_order PASSED            [ 81%]
tests/test_pawpal.py::test_conflict_detection_duplicate_times PASSED     [ 90%]
tests/test_pawpal.py::test_recurrence_weekly_task_creates_next PASSED    [100%]

============================= 11 passed in 0.53s ===============================
```

### Confidence Level

**⭐⭐⭐⭐⭐ (5/5 stars)**

All 11 tests pass consistently. The scheduler correctly handles:
- Sorting and ordering tasks chronologically
- Creating recurring task instances for daily and weekly patterns
- Detecting start-time conflicts between pets
- Filtering and prioritizing tasks
- Respecting owner availability constraints

The system is reliable for its intended use case as a small pet-care planner.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
| ------- | --------- | ----- |
| Sorting behavior | Scheduler.sort_by_time() | Sorts tasks by their start time and title so they appear in a predictable order. |
| Filtering behavior | Scheduler.filter_tasks() | Filters tasks by pet name, completion status, and optional date. |
| Conflict detection logic | Scheduler.detect_conflicts() | Returns lightweight warning messages when two tasks start at the same time. |
| Recurring task logic | Task.mark_complete() and Scheduler.mark_task_done() | Creates the next pending occurrence for daily or weekly tasks after completion. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or link to a demo video here -->
