import os, re, logging, hashlib
from django.core.cache import cache
from rapidfuzz import process
from django.db.models import Avg
from groq import Groq

from core.models import College, Branch, CollegeBranch, Cutoff, SeatMatrix
from core.services.intent import detect_intent
#from core.services.rag.rag_engine import answer_from_brochure

logger = logging.getLogger("chatbot")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_answer(question):
    from core.services.rag.rag_engine import answer_from_brochure
    return answer_from_brochure(question)



CATEGORY_REGEX = r"\b(1G|1K|1R|2AG|2AK|2AR|2BG|2BK|2BR|3AG|3AK|3AR|3BG|3BK|3BR|GM|GMK|GMR|SCG|SCK|SCR|STG|STK|STR)\b"
BRANCH_REGEX   = r"\b(CSE|ECE|EEE|MECH|CIVIL|IT|AI|DS|ML|AIML|ISE|AIDS)\b"
COLLEGE_REGEX  = r"\bE\d{3}\b"


def extract_entities(text: str):
    t = text.upper()
    return {
        "category": re.search(CATEGORY_REGEX, t).group(0) if re.search(CATEGORY_REGEX, t) else None,
        "branch":   re.search(BRANCH_REGEX, t).group(0) if re.search(BRANCH_REGEX, t) else None,
        "college":  re.search(COLLEGE_REGEX, t).group(0) if re.search(COLLEGE_REGEX, t) else None,
    }
def fuzzy_match(value, queryset, field):
    if not value: return None
    values = [getattr(o, field) for o in queryset]
    match, score, idx = process.extractOne(value, values)
    return queryset[idx] if score > 70 else None
def resolve_college(entities):
    if entities["college"]:
        return College.objects.filter(college_code=entities["college"]).first()
    if entities["college_name"]:
        names = list(College.objects.values_list("College_name", flat=True))
        match, score, idx = process.extractOne(entities["college_name"], names)
        if score > 65:
            return College.objects.get(College_name=names[idx])
    return None

def find_college_branch(college_code, branch_code):
    return CollegeBranch.objects.select_related("college","branch").filter(
        college_code=college_code,
        Branch_Code=branch_code
    ).first()



def lookup_cutoff(cb, category):
    return Cutoff.objects.filter(college_branch=cb, category__category_code=category)\
        .select_related("year").order_by("-year__year_code").first()


def lookup_seats(cb, category):
    return SeatMatrix.objects.filter(college_branch=cb, category__category_code=category)\
        .select_related("year").order_by("-year__year_code").first()


def groq_answer(system_prompt, user_prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role":"system","content":system_prompt},
                      {"role":"user","content":user_prompt}],
            temperature=0.3,
            max_tokens=600,
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.exception("LLM failure")
        return "AI service is temporarily unavailable."

def chatbot_engine(message, request):

    entities = extract_entities(message)
    memory = request.session.get("chatbot_context", {})
    for k in entities:
        if not entities[k] and k in memory:
            entities[k] = memory[k]

    intent = detect_intent(message)

    cache_key = hashlib.md5(f"{message}|{entities}".encode()).hexdigest()
    cached = cache.get(cache_key)
    if cached: return cached

    if intent == "cutoff":

        if not entities["branch"]:
            result = {"reply": "Which branch are you looking for?"}
        else:
            college_obj = resolve_college(entities)
            branch_obj = fuzzy_match(entities["branch"], Branch.objects.all(), "Branch_Code")

            if not college_obj or not branch_obj:
                result = {"reply": "Please specify valid college and branch."}
            else:
                cb = find_college_branch(college_obj.college_code, branch_obj.Branch_Code)

                if not entities["category"]:
                    avg = Cutoff.objects.filter(college_branch=cb).aggregate(avg=Avg("cutoff_rank"))["avg"]
                    result = {"reply": f"Average cutoff for {cb.college.College_name} {cb.branch.Branch_Name} is {int(avg)}"}
                else:
                    cutoff = lookup_cutoff(cb, entities["category"])
                    seats = lookup_seats(cb, entities["category"])
                    result = {"reply": f"""
📌 {cb.college.College_name} — {cb.branch.Branch_Name}
Category: {entities['category']}
Cutoff Rank: {cutoff.cutoff_rank if cutoff else 'N/A'}
Available Seats: {seats.available_seats if seats else 'N/A'}
"""}

    elif intent == "college":
        college_obj = resolve_college(entities)
        if not college_obj:
            result = {"reply": "College not found."}
        else:
            result = {"reply": f"""
🏫 {college_obj.College_name}
Location: {college_obj.location}
Fees: ₹{college_obj.firstyearfees}
Highest Package: ₹{college_obj.highestpackage}
"""}

    else:
        context = answer_from_brochure(message)
        result = {"reply": context}

    request.session["chatbot_context"] = entities
    cache.set(cache_key, result, 300)

    return result
