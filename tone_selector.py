def select_tone(intent: str) -> str:
    tones = {
        "shipping": "friendly",
        "refund": "apologetic",
        "complaint": "apologetic",
        "other": "professional"
    }
    return tones.get(intent, "professional")
