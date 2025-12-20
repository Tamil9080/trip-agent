import os
import json
import google.generativeai as genai
from typing import List
from .models import Activity

class AIClient:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Updated to use the latest flash model which usually has good availability
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def fetch_activities(self, city: str) -> List[Activity]:
        prompt = f"""
        Generate a list of 20 distinct tourist activities for {city}.
        For each activity, provide:
        1. Name
        2. Estimated Cost in INR (numeric value only, assume 1 USD = 85 INR). Use 0 for free activities.
        3. Duration in hours (numeric value, e.g., 1.5 or 2)
        4. Category (one of: culture, sightseeing, food, relaxation, shopping, art, entertainment)
        
        Return the response ONLY as a valid JSON list of objects with keys: "name", "cost", "duration", "category".
        Do not include markdown formatting like ```json.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Clean up potential markdown formatting
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            data = json.loads(text)
            
            activities = []
            for item in data:
                activities.append(Activity(
                    name=item['name'],
                    cost=float(item['cost']),
                    duration_hours=float(item['duration']),
                    category=item['category'].lower(),
                    city=city
                ))
            return activities
        except Exception as e:
            print(f"Error fetching from AI: {e}")
            return []
