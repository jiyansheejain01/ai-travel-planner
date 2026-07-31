
# ---------------------------------------------------------------------------
# Sample data for standalone preview — replace with real planner output
# ---------------------------------------------------------------------------
SAMPLE_TRIP = {
    'title': 'Kyoto explorer',
    'destination': 'Kyoto, Japan',
    'dates': 'Apr 2 – Apr 8, 2027',
    'duration': '6 days',
    'travelers': '2 travelers',
    'budget': '¥80,000 budget',
    'trip_type': 'cultural + relaxed',
    'interests': ['temples', 'local food', 'nature walks', 'photography'],
    'summary': (
        "A relaxed cultural week centered on Kyoto's temples and gardens, with day trips to "
        "Fushimi Inari and Arashiyama, home-style dining, and slower mornings built in around "
        "cherry blossom season."
    ),
    'planner_status': 'Complete',
    'confidence': '91%',
    'planning_time': '18.4s',
    'agents_used': '6 of 11',
}
 
SAMPLE_AGENTS = [
    {'name': 'Planner agent', 'status': 'done', 'time': '2.1s', 'confidence': '96%',
     'summary': 'Extracted trip intent, dates, and traveler details.'},
    {'name': 'Flight agent', 'status': 'done', 'time': '4.6s', 'confidence': '89%',
     'summary': 'Found 12 options, ranked by price and layovers.'},
    {'name': 'Hotel agent', 'status': 'done', 'time': '3.8s', 'confidence': '93%',
     'summary': 'Shortlisted 8 stays near central Kyoto.'},
    {'name': 'Weather agent', 'status': 'done', 'time': '1.2s', 'confidence': '98%',
     'summary': 'Mild, clear week with light rain on day 4.'},
    {'name': 'Budget agent', 'status': 'done', 'time': '2.4s', 'confidence': '90%',
     'summary': 'Plan sits 6% under the ¥80,000 budget.'},
    {'name': 'Itinerary agent', 'status': 'done', 'time': '4.3s', 'confidence': '88%',
     'summary': 'Sequenced 6 days around opening hours and travel time.'},
]
 
SAMPLE_FUTURE_AGENTS = ['restaurant agent', 'attractions agent', 'transport agent', 'events agent', 'memory agent']
 
SAMPLE_DAYS = {
    'Day 1': [
        {'title': 'Arrival + check-in', 'time': '15:20', 'duration': '1h', 'setting': 'indoor', 'cost': '¥0', 'note': ''},
    ],
    'Day 2': [
        {'title': 'Fushimi Inari trail walk', 'time': '07:30', 'duration': '2h', 'setting': 'outdoor', 'cost': '¥0',
         'note': 'Arrive early to beat the crowds along the upper trail.'},
        {'title': 'Gion tea ceremony', 'time': '13:00', 'duration': '1.5h', 'setting': 'indoor', 'cost': '¥3,200',
         'note': 'Booked with an English-speaking host.'},
    ],
    'Day 3': [
        {'title': 'Arashiyama bamboo grove', 'time': '09:00', 'duration': '2h', 'setting': 'outdoor', 'cost': '¥500', 'note': ''},
    ],
    'Day 4': [
        {'title': 'Nishiki Market food tour', 'time': '11:00', 'duration': '2h', 'setting': 'indoor', 'cost': '¥4,000', 'note': ''},
    ],
}
 
SAMPLE_FLIGHT = {'airline_route': 'ANA · BLR → KIX', 'times': '01:40 → 15:20 · 1 stop · economy',
                  'price': '¥58,400', 'alt_count': 3}
SAMPLE_HOTEL = {'name': 'Machiya Higashiyama Inn', 'rating_distance': '4.6 rating · 0.6km from Gion',
                 'price': '¥9,800 / night', 'alt_count': 5}
SAMPLE_WEATHER = [
    {'day': 'Day 1', 'condition': 'sun', 'temp': '19°C'},
    {'day': 'Day 2', 'condition': 'sun', 'temp': '18°C'},
    {'day': 'Day 3', 'condition': 'cloud', 'temp': '17°C'},
    {'day': 'Day 4', 'condition': 'rain', 'temp': '16°C'},
    {'day': 'Day 5', 'condition': 'sun', 'temp': '19°C'},
]
 
SAMPLE_BUDGET = {
    'categories': [
        {'name': 'Flights', 'amount': '¥28,900', 'pct': 36},
        {'name': 'Hotels', 'amount': '¥17,600', 'pct': 22},
        {'name': 'Food', 'amount': '¥14,400', 'pct': 18},
        {'name': 'Transport', 'amount': '¥9,600', 'pct': 12},
        {'name': 'Attractions', 'amount': '¥6,400', 'pct': 8},
        {'name': 'Misc', 'amount': '¥3,200', 'pct': 4},
    ],
    'total': '¥80,100',
    'remaining': '¥4,900',
}
 
SAMPLE_PLACES = [
    {'name': 'Fushimi Inari'}, {'name': 'Kinkaku-ji'}, {'name': 'Arashiyama Grove'},
    {'name': 'Nishiki Market'}, {'name': '% Arabica cafe'},
    {'name': "Philosopher's Path", 'hidden_gem': True},
]
 
SAMPLE_RECOMMENDATIONS = [
    'Visit Fushimi Inari before 8am to avoid tour groups.',
    'A 7-day bus pass saves about ¥1,800 over single fares.',
    'Pack a light rain layer for day 4.',
]
 
SAMPLE_ALERTS = [
    {'type': 'warning', 'text': 'Light rain expected day 4 — outdoor plans may shift.'},
    {'type': 'success', 'text': 'Plan is within budget across all categories.'},
]
 
SAMPLE_TIMELINE = [
    'request received', 'details extracted', 'weather · flights · hotels',
    'budget calculated', 'itinerary generated',
]
 
 