#!/usr/bin/python3
""" Test delete feature """
from models.engine.file_storage import FileStorage
from models.state import State

fs = FileStorage()
fs.reload()  # Reload existing data

# All States
all_states = fs.all(State)
print(f"All States (initial): {len(all_states.keys())}")
for state_key in all_states.keys():
    print(all_states[state_key])

# Create a new State
new_state = State()
new_state.name = "California"
fs.new(new_state)
fs.save()
print(f"New State: {new_state}")

# All States
all_states = fs.all(State)
print(f"All States (after adding new state): {len(all_states.keys())}")
for state_key in all_states.keys():
    print(all_states[state_key])

# Create another State
another_state = State()
another_state.name = "Nevada"
fs.new(another_state)
fs.save()
print(f"Another State: {another_state}")

# All States
all_states = fs.all(State)
print(f"All States (after adding another state): {len(all_states.keys())}")
for state_key in all_states.keys():
    print(all_states[state_key])

# Delete the new State
fs.delete(new_state)
fs.save()
print(f"Deleted State: {new_state}")

# All States
all_states = fs.all(State)
print(f"All States (after deletion): {len(all_states.keys())}")
for state_key in all_states.keys():
    print(all_states[state_key])
