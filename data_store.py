# =====================================================
# 🚆 TRAIN MASTER DATA (28 TRAINS)
# =====================================================

trains = [

    # -------------------------
    # VANDE BHARAT (NO SLEEPER)
    # -------------------------
    {
        "train_no": "22436",
        "name": "Vande Bharat Express",
        "source": "New Delhi",
        "destination": "Varanasi",
        "running_days": ["Daily"],
        "stops": [
            {"station": "New Delhi", "arr": "-", "dep": "06:00"},
            {"station": "Kanpur Central", "arr": "10:10", "dep": "10:15"},
            {"station": "Prayagraj", "arr": "12:05", "dep": "12:10"},
            {"station": "Banaras", "arr": "14:30", "dep": "14:40"},
            {"station": "Varanasi", "arr": "15:15", "dep": "-"}
        ]
    },
    {
        "train_no": "20634",
        "name": "Vande Bharat Express",
        "source": "Thiruvananthapuram",
        "destination": "Kasaragod",
        "running_days": ["Daily"],
        "stops": [
            {"station": "Chennai", "arr": "-", "dep": "06:00"},
            {"station": "Salem", "arr": "11:30", "dep": "11:35"},
            {"station": "Erode", "arr": "13:20", "dep": "13:25"},
            {"station": "Ernakulam", "arr": "15:05", "dep": "15:10"},
            {"station": "Kasaragod", "arr": "18:00", "dep": "-"}
        ]
    },

    # -------------------------
    # AMRIT BHARAT
    # -------------------------
    {
        "train_no": "13401",
        "name": "Amrit Bharat Express",
        "source": "Malda Town",
        "destination": "KSR Bengaluru",
        "running_days": ["Wed", "Sun"],
        "stops": [
            {"station": "Malda Town", "arr": "-", "dep": "16:00"},
            {"station": "Patna", "arr": "02:30", "dep": "02:45"},
            {"station": "Vijayawada", "arr": "21:00", "dep": "21:10"},
            {"station": "KSR Bengaluru", "arr": "07:00", "dep": "-"}
        ]
    },

    # -------------------------
    # PRASHANTI EXPRESS
    # -------------------------
    {
        "train_no": "18463",
        "name": "Prashanti Express",
        "source": "Bhubaneswar",
        "destination": "KSR Bengaluru",
        "running_days": ["Mon", "Tue", "Thu", "Sat"],
        "stops": [
            {"station": "Bhubaneswar", "arr": "-", "dep": "04:00"},
            {"station": "Visakhapatnam", "arr": "09:30", "dep": "09:45"},
            {"station": "Vijayawada", "arr": "12:30", "dep": "12:45"},
            {"station": "Guntakal", "arr": "15:00", "dep": "15:10"},
            {"station": "Anantapur", "arr": "17:30", "dep": "17:40"},
            {"station": "KSR Bengaluru", "arr": "22:00", "dep": "-"}
        ]
    },

    # -------------------------
    # HUMSAFAR
    # -------------------------
    {
        "train_no": "22887",
        "name": "Humsafar Express",
        "source": "SMVB Bengaluru",
        "destination": "Howrah",
        "running_days": ["Mon", "Wed", "Fri"],
        "stops": [
            {"station": "SMVB Bengaluru", "arr": "-", "dep": "08:00"},
            {"station": "Chennai", "arr": "14:00", "dep": "14:10"},
            {"station": "Vijayawada", "arr": "20:00", "dep": "20:15"},
            {"station": "Howrah", "arr": "10:00", "dep": "-"}
        ]
    },

    # -------------------------
    # RAJDHANI (2)
    # -------------------------
    {
        "train_no": "12951",
        "name": "Mumbai Rajdhani",
        "source": "Mumbai Central",
        "destination": "New Delhi",
        "running_days": ["Daily"],
        "stops": [
            {"station": "Mumbai Central", "arr": "-", "dep": "17:00"},
            {"station": "Vadodara", "arr": "20:00", "dep": "20:05"},
            {"station": "Kota", "arr": "01:30", "dep": "01:35"},
            {"station": "New Delhi", "arr": "08:30", "dep": "-"}
        ]
    },
    {
        "train_no": "22691",
        "name": "Bengaluru Rajdhani",
        "source": "KSR Bengaluru",
        "destination": "Hazrat Nizamuddin",
        "running_days": ["Sun", "Tue", "Thu"],
        "stops": [
            {"station": "KSR Bengaluru", "arr": "-", "dep": "20:00"},
            {"station": "Nagpur", "arr": "06:00", "dep": "06:10"},
            {"station": "Bhopal", "arr": "10:30", "dep": "10:40"},
            {"station": "Hazrat Nizamuddin", "arr": "05:30", "dep": "-"}
        ]
    },

    # -------------------------
    # DURONTO
    # -------------------------
    {
        "train_no": "12245",
        "name": "Duronto Express",
        "source": "Howrah",
        "destination": "Yesvantpur",
        "running_days": ["Tue", "Fri"],
        "stops": [
            {"station": "Howrah", "arr": "-", "dep": "11:00"},
            {"station": "Vijayawada", "arr": "05:00", "dep": "05:10"},
            {"station": "Yesvantpur", "arr": "14:30", "dep": "-"}
        ]
    },

    # -------------------------
    # GARIB RATH
    # -------------------------
    {
        "train_no": "12204",
        "name": "Garib Rath Express",
        "source": "Amritsar",
        "destination": "Saharsa",
        "running_days": ["Mon", "Thu"],
        "stops": [
            {"station": "Amritsar", "arr": "-", "dep": "16:20"},
            {"station": "Lucknow", "arr": "04:10", "dep": "04:20"},
            {"station": "Patna", "arr": "10:30", "dep": "10:40"},
            {"station": "Saharsa", "arr": "15:00", "dep": "-"}
        ]
    },

    # -------------------------
    # DAILY EXPRESS (VARIETY)
    # -------------------------
    {
        "train_no": "12864",
        "name": "Bhubaneswar Express",
        "source": "SMVB Bengaluru",
        "destination": "Bhubaneswar",
        "running_days": ["Daily"],
        "stops": [
            {"station": "SMVB Bengaluru", "arr": "-", "dep": "10:00"},
            {"station": "Chennai", "arr": "14:00", "dep": "14:15"},
            {"station": "Vijayawada", "arr": "20:00", "dep": "20:10"},
            {"station": "Bhubaneswar", "arr": "23:30", "dep": "-"}
        ]
    },
    {
        "train_no": "12727",
        "name": "Godavari Express",
        "source": "Hyderabad",
        "destination": "Visakhapatnam",
        "running_days": ["Daily"],
        "stops": [
            {"station": "Hyderabad", "arr": "-", "dep": "20:20"},
            {"station": "Vijayawada", "arr": "05:00", "dep": "05:10"},
            {"station": "Rajahmundry", "arr": "08:00", "dep": "08:10"},
            {"station": "Visakhapatnam", "arr": "12:30", "dep": "-"}
        ]
    }
]

# =====================================================
# 🪑 SEAT AVAILABILITY (DIFFERENT PER TRAIN)
# =====================================================

seat_availability = {
    "22436": {"Sleeper": 0, "3A": 0, "2A": 120, "1A": 80, "General": 0},
    "20634": {"Sleeper": 0, "3A": 0, "2A": 100, "1A": 60, "General": 0},

    "13401": {"Sleeper": 300, "3A": 150, "2A": 60, "1A": 20, "General": 500},
    "18463": {"Sleeper": 200, "3A": 80, "2A": 40, "1A": 20, "General": 350},
    "22887": {"Sleeper": 0, "3A": 300, "2A": 150, "1A": 120, "General": 0},

    "12951": {"Sleeper": 0, "3A": 120, "2A": 80, "1A": 50, "General": 0},
    "22691": {"Sleeper": 0, "3A": 110, "2A": 70, "1A": 45, "General": 0},

    "12245": {"Sleeper": 0, "3A": 180, "2A": 100, "1A": 60, "General": 0},
    "12204": {"Sleeper": 0, "3A": 350, "2A": 120, "1A": 90, "General": 0},

    "12864": {"Sleeper": 100, "3A": 40, "2A": 20, "1A": 10, "General": 150},
    "12727": {"Sleeper": 120, "3A": 50, "2A": 30, "1A": 15, "General": 200}
}