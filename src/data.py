from .models import Activity, Accommodation

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

HOTELS_DB = [
    # Paris
    Accommodation("Hotel Ritz Paris", 85000.0, "5-star", "15 Place Vendôme, Paris"),
    Accommodation("Ibis Paris Tour Eiffel", 12000.0, "3-star", "2 Rue Cambronne, Paris"),
    Accommodation("Le Meurice", 95000.0, "5-star", "228 Rue de Rivoli, Paris"),
    
    # Tokyo
    Accommodation("Park Hyatt Tokyo", 75000.0, "5-star", "3-7-1-2 Nishi-Shinjuku, Tokyo"),
    Accommodation("APA Hotel Shinjuku", 8500.0, "3-star", "Shinjuku, Tokyo"),
    Accommodation("The Peninsula Tokyo", 80000.0, "5-star", "1-8-1 Yurakucho, Tokyo"),

    # New York
    Accommodation("The Plaza", 90000.0, "5-star", "768 5th Ave, New York"),
    Accommodation("Pod 51", 15000.0, "3-star", "230 E 51st St, New York"),
    Accommodation("Marriott Marquis", 35000.0, "4-star", "1535 Broadway, New York"),
]

def get_activities_for_city(city: str) -> list[Activity]:
    return [a for a in ACTIVITIES_DB if a.city.lower() == city.lower()]

def get_hotels_for_city(city: str) -> list[Accommodation]:
    return [h for h in HOTELS_DB if city.lower() in h.address.lower()]
