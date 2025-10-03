# Collector design

Interface needs:
 - keep track of a list of fish
 - progress fish through a series of a few states (camera, sedation, measurement, release)
 - we can have up to three fish at once
 - buttons to progress fish from one stage to the next
 - simple UI that visually shows the stages and a fish ID / count
 - simple UI that shows length, width, breadth and has input for it
 - basic validation on input ranges
 - button to keep track of start and stop
 - ability to undo moving a fish out of staging
 - a second page to edit existing fish
 - another option for notes about the fish, welfare notes, sampling notes, ...
 - Ability to set input bounds for data validation

Backend:
 - backed by simple parquet, csv, sqlite, or duckdb
 - ideally in python but a simple JS option would work too

Frontend:
 - the state will be a JSON object with maybe 50 rows. I'll want to come up with some simple averages there and some plots but not a ton of state in this app.
 - very simple JS framework, potentially svelte or just vanilla JS. open to vue or some other reccommendation
 - most of the logic will be client side

Future pages:
 - A UI to show weight vs. length vs. k-factor relationships
 - A new collection setup screen
 - A way to start a new collection
 - A way to load an existing collection database and continue
 - Add timings for how long each stage is taking
 - Add reminders for tank cleaning
 - Add goals for number of fish collected
 - Add page to view average time per stage

My initial thoughts:

Frontend:
 - HTML for visualization
 - state is kept in JS and persisted on save
 - fish history is reloaded on release
 - can there be a browser cache to keep the Pen ID and Site name and Sampling info the same

Backend:
 - needs to load list of fish and data
 - needs to accept 

# Monitor design
Requirements
 - surface live information about ranker scores
 - surface live information about crops
 - surface live information about fish positioning
 - should run on camera and we could load it via ssh port forwarding

 # My skillset
 - very basic and legacy react (before hooks)
 - have build minimal svelte app
 = strong python
 - good adaptability when code is compehasible

# Use case
 - internal only tool
 - low support
 - needs to be simple and basic and not production grade code
 - simple is safer
 - simpler has less bugs
