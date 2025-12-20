# AI Travel Planner Agent

A Python-based agent that generates travel itineraries based on budget, time, and preferences. It uses a planning loop with constraints to ensure the trip fits within the user's budget.

## Features

- **Day-by-Day Planning**: Allocates activities to days based on duration.
- **Budget Management**: Automatically re-plans if the initial itinerary exceeds the budget.
- **Preference Matching**: Prioritizes activities matching user preferences (e.g., culture, food).
- **Constraint Checking**: Ensures daily activity hours don't exceed limits.

## Project Structure

- `src/main.py`: Entry point and CLI interface.
- `src/planner.py`: Core logic for planning and re-planning.
- `src/models.py`: Data structures for Trip, Day, and Activity.
- `src/data.py`: Mock database of cities and activities.

## Usage

### Command Line Interface (CLI)

Run the agent interactively:

```bash
python -m src.main
```

Or provide arguments directly:

```bash
python -m src.main --city Paris --days 3 --budget 17000 --prefs culture,food
```

### Web Interface (Streamlit)

To use the graphical interface:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

### Using AI Features (Optional)

To enable planning for **any city** using real-time AI data:

1.  **Get a Free API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  **Create Key**: Click on "Create API key" (it's free for personal use).
3.  **Enter Key**: Paste this key into the "Gemini API Key" field in the web app sidebar.

## Example Output

```text
--- AI Travel Planner Agent ---
Planning trip to Paris for 3 days with budget $200.0...
Budget exceeded ($240.0 > $200.0). Re-planning (Attempt 1)...

==============================
FINAL ITINERARY FOR PARIS
==============================

Day 1:
  - Seine River Cruise (relaxation): $15.0, 1.5h
  - Louvre Museum (culture): $20.0, 4.0h
...
Total Trip Cost: $140.0
Budget: $200.0
Status: Within Budget ✅
```
