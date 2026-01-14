INTENT_CUTOFF  = ["CUTOFF", "RANK", "SEAT", "AVAILABLE"]
INTENT_COLLEGE = ["COLLEGE", "FEE", "FEES", "HOSTEL", "PLACEMENT"]
INTENT_RULES   = ["DOCUMENT", "COUNSELLING", "ELIGIBILITY", "PROCESS"]

def detect_intent(text):
    t = text.upper()
    if any(w in t for w in INTENT_CUTOFF):  return "cutoff"
    if any(w in t for w in INTENT_COLLEGE): return "college"
    if any(w in t for w in INTENT_RULES):   return "brochure"
    return "general"
