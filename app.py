from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This version now uses the core PawPal+ classes so your owner, pets, and tasks persist in the session.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "scheduler" not in st.session_state or st.session_state.scheduler.owner is not st.session_state.owner:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.subheader("Owner and Pets")
st.caption("Create or update the owner and add pets to the session state.")

owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Save owner"):
    owner.name = owner_name
    st.session_state.owner = owner
    st.session_state.scheduler = Scheduler(owner)
    st.success(f"Owner updated to {owner.name}.")

pet_name = st.text_input("Pet name", value="Mochi")
pet_age = st.number_input("Pet age", min_value=0, max_value=30, value=2)
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not pet_name.strip():
        st.warning("Please enter a pet name.")
    else:
        pet = Pet(name=pet_name.strip(), species=species, age=int(pet_age))
        owner.add_pet(pet)
        st.session_state.owner = owner
        st.session_state.scheduler = Scheduler(owner)
        st.success(f"Added {pet.name} to {owner.name}'s pets.")

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species}, age {pet.age})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
st.caption("Add tasks and attach them to a pet using the domain model methods.")

available_pet_names = [pet.name for pet in owner.pets]
if available_pet_names:
    selected_pet_name = st.selectbox("Assign task to pet", available_pet_names)
else:
    selected_pet_name = None
    st.info("Add a pet before scheduling tasks.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.number_input("Priority", min_value=1, max_value=10, value=3)

if st.button("Add task"):
    if not available_pet_names:
        st.warning("Please add a pet before creating a task.")
    else:
        task = Task(
            id=f"{task_title.lower().replace(' ', '-')}-{len(owner.all_tasks()) + 1}",
            title=task_title,
            duration=int(duration),
            priority=int(priority),
            pet_id=selected_pet_name,
        )
        scheduler.add_task(selected_pet_name, task)
        st.session_state.owner = owner
        st.session_state.scheduler = scheduler
        st.success(f"Added task '{task.title}' for {selected_pet_name}.")

if owner.all_tasks():
    st.write("Current tasks:")
    task_rows = [
        {
            "pet": task.pet_id,
            "title": task.title,
            "duration": task.duration,
            "priority": task.priority,
        }
        for task in owner.all_tasks()
    ]
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a simple daily plan from the scheduler.")

if st.button("Generate schedule"):
    plan = scheduler.build_plan(date.today())
    if plan:
        st.success("Schedule generated.")
        for item in plan:
            st.write(f"- {item['start'].strftime('%H:%M')} to {item['end'].strftime('%H:%M')}: {item['task'].title} for {item['pet_name']}")
    else:
        st.info("No tasks were included in the schedule.")
