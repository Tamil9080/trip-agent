import streamlit as st
import time
import os
import sys
from dotenv import load_dotenv

# Add project root to python path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.planner import TravelPlanner
from src.groq_client import GroqClient
from src.data import get_hotels_for_city

load_dotenv()

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    /* Main App Background - Deep Dark Blue/Grey */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* Sidebar - Slightly lighter dark */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F0F6FC !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    h1 {
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 1px solid #30363D;
        background: linear-gradient(90deg, #7C3AED, #DB2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* General Text */
    p, li, div {
        color: #C9D1D9;
    }
    
    /* Buttons - Vibrant Gradient */
    .stButton>button {
        background: linear-gradient(45deg, #7C3AED, #DB2777);
        color: white !important;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #A78BFA !important; /* Soft Purple */
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8B949E !important;
    }
    
    /* Expander/Cards */
    div[data-testid="stExpander"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 8px;
    }
    
    /* Custom Accommodation Card */
    .accommodation-card {
        background-color: #161B22;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363D;
        border-left: 6px solid #DB2777; /* Pink accent */
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 24px;
    }
    
    .acc-title {
        color: #F0F6FC !important;
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .acc-details {
        color: #8B949E !important;
        margin: 5px 0;
    }
    
    .acc-price-box {
        margin-top: 15px;
        background-color: #1F2937;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #374151;
    }
    
    .acc-total {
        color: #A78BFA !important;
        font-weight: bold;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✈️ AI Travel Planner Agent")
st.markdown("Generate a personalized travel itinerary within your budget constraints.")

# Sidebar for inputs
with st.sidebar:
    st.header("Configuration")
    
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password")
        if not api_key:
            st.info("💡 Get free key: [Groq Console](https://console.groq.com/keys)")

    st.divider()
    
    st.header("Trip Details")
    # If API key is present, allow text input for any city
    if api_key:
        city = st.text_input("Enter City", value="Paris")
    else:
        city = st.selectbox("Select City", ["Paris", "Tokyo", "New York"])
        
    # Hotel Selection
    available_hotels = get_hotels_for_city(city)
    selected_hotel = None
    
    if available_hotels:
        st.subheader("Accommodation")
        # Create options with price
        hotel_map = {f"{h.name} - ₹{h.cost_per_night}/night": h for h in available_hotels}
        options = ["Let AI Decide"] + list(hotel_map.keys())
        
        selection = st.selectbox("Choose Hotel", options)
        
        if selection != "Let AI Decide":
            selected_hotel = hotel_map[selection]

    days = st.slider("Number of Days", min_value=1, max_value=7, value=3)
    budget = st.number_input("Total Budget (₹)", min_value=1000, value=20000, step=1000)
    
    st.subheader("Preferences")
    available_prefs = ["culture", "sightseeing", "food", "relaxation", "shopping", "art", "entertainment"]
    preferences = st.multiselect("Select Interests", available_prefs, default=["culture", "food"])
    
    plan_button = st.button("Plan My Trip", type="primary")

if plan_button:
    planner = TravelPlanner()
    
    # Container for logs
    log_container = st.container()
    with log_container:
        st.info("Agent Status: Initializing...")
        
    logs = []
    def log_callback(msg):
        logs.append(msg)
        # Update the log container in real-time
        with log_container:
            for log in logs:
                st.text(f"🤖 {log}")
            time.sleep(0.2) 

    try:
        custom_activities = None
        accommodation = None
        
        if api_key:
            client = GroqClient(api_key)
            
            # 1. Fetch Accommodation
            if selected_hotel:
                accommodation = selected_hotel
                log_callback(f"Using selected accommodation: {accommodation.name}")
            else:
                with st.spinner(f'Finding accommodation in {city}...'):
                    # Estimate 40% of budget for accommodation
                    target_nightly_rate = (budget * 0.4) / days
                    accommodation = client.fetch_accommodation(city, target_nightly_rate)
                
            # 2. Fetch Activities
            with st.spinner(f'Fetching activities for {city} using Groq (Llama 3)...'):
                custom_activities = client.fetch_activities(city)
                
                if not custom_activities:
                    st.error("Failed to fetch activities. Please check your API key and try again.")
                    st.stop()
        else:
            # Fallback if no API key but hotel selected
            if selected_hotel:
                accommodation = selected_hotel
        
        with st.spinner('AI Agent is planning your trip...'):
            itinerary = planner.plan_trip(city, days, budget, preferences, on_log=log_callback, custom_activities=custom_activities, accommodation=accommodation)
        
        st.success("Trip Planned Successfully!")
        
        # Summary Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cost", f"₹{itinerary.total_cost}", delta=f"{budget - itinerary.total_cost} remaining")
        col2.metric("Total Duration", f"{sum(d.total_duration for d in itinerary.days)} Hours")
        col3.metric("Status", "Within Budget ✅" if itinerary.total_cost <= budget else "Over Budget ⚠️")

        st.divider()
        
        # Display Accommodation
        if itinerary.accommodation:
            st.subheader("🏨 Suggested Accommodation")
            acc = itinerary.accommodation
            with st.container():
                st.markdown(f"""
                <div class="accommodation-card">
                    <h3 class="acc-title">{acc.name}</h3>
                    <p class="acc-details">📍 {acc.address}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #30363D; padding-top: 10px;">
                        <span style="color: #C9D1D9;">⭐ <b>Rating:</b> {acc.rating}</span>
                        <span style="color: #C9D1D9;">💰 <b>Cost:</b> ₹{acc.cost_per_night:,.2f}/night</span>
                    </div>
                    <div class="acc-price-box">
                        <p class="acc-total">Total for {days} nights: ₹{acc.cost_per_night * days:,.2f}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.divider()
        
        # Display Itinerary
        st.subheader(f"📅 Your {days}-Day Itinerary for {city}")
        
        for day in itinerary.days:
            with st.expander(f"Day {day.day_number} - ₹{day.total_cost} ({day.total_duration}h)", expanded=True):
                if not day.activities:
                    st.write("*Free day / No activities scheduled*")
                else:
                    for act in day.activities:
                        col_a, col_b, col_c = st.columns([3, 1, 1])
                        with col_a:
                            st.markdown(f"**{act.name}**")
                            st.caption(f"Category: {act.category.title()}")
                        with col_b:
                            st.write(f"₹{act.cost}")
                        with col_c:
                            st.write(f"{act.duration_hours}h")
                            
    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("👈 Configure your trip in the sidebar and click 'Plan My Trip' to start.")
