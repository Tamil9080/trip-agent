import os
import json
from groq import Groq
from typing import List, Optional
from .models import Activity, Accommodation

class GroqClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def fetch_accommodation(self, city: str, nightly_budget: float) -> Optional[Accommodation]:
        prompt = f"""
        Suggest a specific hotel or accommodation in {city} that costs approximately {nightly_budget} INR per night.
        Provide:
        1. Name
        2. Cost per night in INR (numeric)
        3. Rating (e.g., "4.5/5" or "3 stars")
        4. Short Address or Area
        
        Return ONLY a valid JSON object with keys: "name", "cost", "rating", "address".
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful travel assistant that outputs only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
            )
            
            data = json.loads(chat_completion.choices[0].message.content)
            return Accommodation(
                name=data['name'],
                cost_per_night=float(data['cost']),
                rating=data['rating'],
                address=data['address']
            )
        except Exception as e:
            print(f"Error fetching accommodation: {e}")
            return None

    def fetch_activities(self, city: str) -> List[Activity]:
        prompt = f"""
        Generate a list of 20 distinct tourist activities for {city}.
        For each activity, provide:
        1. Name
        2. Estimated Cost in INR (numeric value only, assume 1 USD = 85 INR). Use 0 for free activities.
        3. Duration in hours (numeric value, e.g., 1.5 or 2)
        4. Category (one of: culture, sightseeing, food, relaxation, shopping, art, entertainment)
        
        Return the response ONLY as a valid JSON object with a key "activities" containing the list.
        Example: {{ "activities": [ {{ "name": "...", "cost": 100, "duration": 2, "category": "food" }} ] }}
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful travel assistant that outputs only valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
            )
            
            response_content = chat_completion.choices[0].message.content
            data = json.loads(response_content)
            
            # Handle potential wrapper keys
            activity_list = []
            if "activities" in data:
                activity_list = data["activities"]
            elif isinstance(data, list):
                activity_list = data
            else:
                # Try to find the first list value
                for key, value in data.items():
                    if isinstance(value, list):
                        activity_list = value
                        break
            
            activities = []
            for item in activity_list:
                activities.append(Activity(
                    name=item['name'],
                    cost=float(item['cost']),
                    duration_hours=float(item['duration']),
                    category=item['category'].lower(),
                    city=city
                ))
            return activities
        except Exception as e:
            print(f"Error fetching from Groq: {e}")
            return []
