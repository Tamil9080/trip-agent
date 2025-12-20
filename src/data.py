from .models import Activity

# Mock data for demonstration (Prices in INR)
ACTIVITIES_DB = [
    # Paris
    Activity("Eiffel Tower Visit", 2550.0, 3.0, "sightseeing", "Paris"),
    Activity("Louvre Museum", 1700.0, 4.0, "culture", "Paris"),
    Activity("Seine River Cruise", 1275.0, 1.5, "relaxation", "Paris"),
    Activity("Notre Dame Cathedral", 0.0, 1.0, "sightseeing", "Paris"),
    Activity("Montmartre Walk", 0.0, 2.0, "sightseeing", "Paris"),
    Activity("Versailles Palace", 2125.0, 5.0, "culture", "Paris"),
    Activity("French Cooking Class", 8500.0, 3.0, "food", "Paris"),
    Activity("Wine Tasting", 4250.0, 2.0, "food", "Paris"),
    
    # Tokyo
    Activity("Senso-ji Temple", 0.0, 2.0, "culture", "Tokyo"),
    Activity("Tokyo Skytree", 2125.0, 2.0, "sightseeing", "Tokyo"),
    Activity("Sushi Making Class", 6800.0, 2.5, "food", "Tokyo"),
    Activity("Shibuya Crossing", 0.0, 0.5, "sightseeing", "Tokyo"),
    Activity("Meiji Shrine", 0.0, 1.5, "culture", "Tokyo"),
    Activity("TeamLab Planets", 2550.0, 3.0, "art", "Tokyo"),
    Activity("Akihabara Shopping", 4250.0, 3.0, "shopping", "Tokyo"),
    
    # New York
    Activity("Statue of Liberty", 2125.0, 4.0, "sightseeing", "New York"),
    Activity("Central Park Walk", 0.0, 2.0, "relaxation", "New York"),
    Activity("Broadway Show", 12750.0, 3.0, "entertainment", "New York"),
    Activity("Empire State Building", 3400.0, 2.0, "sightseeing", "New York"),
    Activity("Metropolitan Museum of Art", 2550.0, 4.0, "culture", "New York"),
    Activity("Pizza Tour", 5100.0, 2.5, "food", "New York"),
]

def get_activities_for_city(city: str) -> list[Activity]:
    return [a for a in ACTIVITIES_DB if a.city.lower() == city.lower()]
