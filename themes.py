# themes.py

# Updated dictionary of departments and keywords (from thematic analysis)
keywords = {
    "Transport & Travel": [
        "bus", "car", "road", "roads", "transport", "transportation", "ride", "route", "driver",
        "passengers", "commute", "shuttles", "travelling", "departed", "departure", "arrivals",
        "mobility", "scheduled", "delays", "punctuality", "traffic", "jam", "stops", "rerouted",
        "infrastructure", "transitions", "retarded", "crowding", "station", "vehicle", "vehicles",
        "moved", "traveling", "transported", "drivers", "bypass", "walking", "walk", "passenger",
        "landing", "tracks", "journey", "logistics", "international", "flights", "flight",
        "maps", "schedule", "timeline", "clock", "delay", "hurry", "missed", "operations", "travel",
        "update", "coordination", "timeliness", "planning", "rapid", "stuck", "taxi", "train",
        "transporting", "transit", "departures", "rides", "fleet",
        "highway", "transfers", "routes", "waiting", "luggage"
    ],

    "Accommodation & Facilities": [
        "accommodation", "facilities", "residences", "housing", "hotels", "hoteling", "rooms",
        "house", "homes", "sites", "locations", "residential", "setup", "availability", "space",
        "relaxing", "furniture", "utilities", "amenities", "bed", "bedding", "bedroom", "interior",
        "carpets", "floor", "equipment", "units", "spacious", "open", "quarters", "water",
        "electricity", "surfaces", "ventilation", "pillows", "lobby", "cleanliness", "air conditioning",
        "sanitation", "center", "laundry", "sinks", "bathroom", "bathrooms", "baths", "office",
        "built", "swimming", "stable", "shower", "resort", "pools", "lodging", "parking", "belongings",
        "wall", "windows", "door", "pool", "usability", "station", "linen", "mattress",
        "lighting", "washroom", "toiletries", "shampoo",
        "soap", "towels", "minibar", "decor", "chairs", "tables", "tiles", "wallpaper",
        "upholstery", "signage", "reception", "soundproofing", "layout"
    ],

    "Hotel Room Conditions & Cleanliness": [
        "room", "rooms", "cleanliness", "housekeeping", "tidy", "stains", "stained", "unclean",
        "dirt", "dusty", "smell", "odor", "bathrooms", "toilet", "bathroom", "bedding", "bed",
        "washed", "hygiene", "hygienic", "towels", "garbage", "neat", "windows", "sheets", "cleaning",
        "maintained", "spider", "insects", "bath", "pillows", "air", "ventilation",
        "broken", "damaged", "uncleanliness", "dirty", "poorly", "shower", "wall", "noise",
        "silence", "dust", "floor", "neatness", "sanitation", "clean", "sanitary", "spotless",
        "unkempt", "mold", "dustbin", "contamination", "sticky", "pests",
        "infestation", "mildew", "upkeep", "washing", "odors",
        "fresh", "polished", "smelly"
    ],

    "Staff Attitude & Support": [
        "staff", "employees", "officials", "officers", "support", "guided", "guiding", "cooperation",
        "cooperative", "teamwork", "kindness", "friendly", "friendliness", "warmth", "patient",
        "compassion", "courteous", "respectful", "caring", "communicated", "helpful", "attitude", "sincerity",
        "dedication", "behaved", "temperament", "humility", "accountability", "willingness", "listening",
        "approachable", "respect", "encouragement", "supporter", "assisted", "treatment", "service", "thankfulness",
        "interacting", "greeted", "greetings", "counseling", "devotion", "understanding", "cheerful",
        "tact", "assisting", "manners", "helping", "counselor", "training", "trained", "assistant",
        "receptionist", "team", "employee", "welcomed", "praised", "communicative", "proactive",
        "responsive", "rude", "supportive", "professional", "empathetic", "attentive", "knowledgeable",
        "honest", "enthusiastic", "skilled", "motivated"
    ],

    "Service Efficiency & Time Management": [
        "schedule", "scheduling", "timeliness", "timing", "deadlines", "delay", "delays", "waiting",
        "waited", "organizing", "management", "handling", "operation", "workflow", "responsiveness",
        "immediate", "quickly", "on-time", "execution", "repetition", "slowness", "inconsistency",
        "registration", "flow", "disruptions", "interruptions", "missed", "adherence", "smoothly",
        "performed", "chaos", "confusion", "complicated", "implementation",
        "process", "processes", "timely", "executed", "managing", "effectiveness",
        "efficiency", "deadline", "responses", "quick", "prompt", "stuck",
        "updated", "systematically", "performance", "task", "clock", "timetable",
        "plan", "response", "immediately", "repeated", "completed", "finishing",
        "pauses", "backlog", "punctual", "rushed", "slow", "efficient", "organized",
        "coordinated", "interrupted", "postponement", "queue",
        "continuity", "smooth", "speed", "hiccups", "downtime", "troubleshooting", "deployment"
    ],

    "Food Quality & Dining": [
        "food", "foods", "meal", "meals", "dish", "dishes", "taste", "tasty", "delicious", "flavors",
        "flavor", "freshness", "fresh", "cooked", "cooking", "breakfast", "dinner", "eating", "restaurant",
        "salty", "hygiene", "hot", "cold", "presentation", "smells", "ingredients", "baked", "portions",
        "nutrition", "served", "serving", "snack", "drinks", "seafood", "seasoning", "bland", "tasteless",
        "spicy", "fat", "diet", "dirty", "frozen", "spices", "meat", "eat", "dining", "tables", "menu",
        "cuisine", "culinary", "stale", "appetizing", "salads", "soups",
        "sauces", "garnishes", "desserts", "calories", "vegan", "gluten", "organic"
    ],

    "Event & Program Organization": [
        "event", "events", "organized", "organizing", "program", "organizers", "setup", "planning",
        "preparation", "process", "processes", "execution", "implemented", "schedule", "coordination",
        "participation", "register", "registration", "sessions", "teamwork", "performance", "administration",
        "conducted", "flow", "success", "management", "timeline", "logistics", "initiative", "implementation",
        "session", "structure", "systematic", "pre-planned", "agenda", "leadership", "executed",
        "contribution", "teams", "completed", "briefing", "rounds", "conferences",
        "organizational", "coordinated", "managed", "seminars", "involved", "participant", "participants",
        "organizations", "cooperation", "governance", "task", "activities", "scheduling",
        "hosting", "managing", "visitor", "group", "volunteers", "entertainment",
        "workshops", "speakers"
    ]
}

# Lowercase and strip all keywords for normalization
themes_topics = {
    topic: [kw.lower().strip() for kw in kw_list]
    for topic, kw_list in keywords.items()
}
