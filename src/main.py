import sys
import argparse
from src.planner import TravelPlanner

def main():
    print("--- AI Travel Planner Agent ---")
    
    parser = argparse.ArgumentParser(description='Travel Planner Agent')
    parser.add_argument('--city', type=str, help='City to visit')
    parser.add_argument('--days', type=int, help='Number of days')
    parser.add_argument('--budget', type=float, help='Total budget')
    parser.add_argument('--prefs', type=str, help='Comma separated preferences')
    
    args = parser.parse_args()
    
    # Inputs
    try:
        if args.city and args.days and args.budget:
            city = args.city
            days = args.days
            budget = args.budget
            preferences = [p.strip() for p in args.prefs.split(",")] if args.prefs else []
        else:
            city = input("Enter city (Paris, Tokyo, New York): ").strip()
            days = int(input("Enter number of days: "))
            budget = float(input("Enter total budget (INR): "))
            prefs_input = input("Enter activity preferences (comma separated, e.g., culture, food): ")
            preferences = [p.strip() for p in prefs_input.split(",")] if prefs_input else []
    except ValueError:
        print("Invalid input. Please enter numbers for days and budget.")
        return

    planner = TravelPlanner()
    
    try:
        final_itinerary = planner.plan_trip(city, days, budget, preferences)
        
        print("\n" + "="*30)
        print(f"FINAL ITINERARY FOR {city.upper()}")
        print("="*30)
        
        for day in final_itinerary.days:
            print(f"\nDay {day.day_number}:")
            if not day.activities:
                print("  (Free day / No activities scheduled)")
            for act in day.activities:
                print(f"  - {act.name} ({act.category}): ₹{act.cost}, {act.duration_hours}h")
            print(f"  Daily Total: ₹{day.total_cost} | {day.total_duration}h")
            
        print("-" * 30)
        print(f"Total Trip Cost: ₹{final_itinerary.total_cost}")
        print(f"Budget: ₹{budget}")
        if final_itinerary.total_cost <= budget:
            print("Status: Within Budget ✅")
        else:
            print("Status: Over Budget ⚠️")
            
    except Exception as e:
        print(f"Error planning trip: {e}")

if __name__ == "__main__":
    main()
