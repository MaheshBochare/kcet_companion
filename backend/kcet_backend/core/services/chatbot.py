# core/services/chatbot_engine.py

import os
import re
from groq import Groq
from django.db.models import Q

from core.models import (
    College, Branch, Category, CollegeBranch,
    Cutoff, SeatMatrix
)

# --------------------
# LLM Client
# --------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# --------------------
# Regex Extractors
# --------------------
CATEGORY_REGEX = r"\b(1G|1K|1R|2AG|2AK|2AR|2BG|2BK|2BR|3AG|3AK|3AR|3BG|3BK|3BR|GM|GMK|GMR|SCG|SCK|SCR|STG|STK|STR)\b"
BRANCH_REGEX   = r"\b(CSE|ECE|EEE|MECH|CIVIL|IT|AI|DS|ML|AIML|ISE|AIDS)\b"
COLLEGE_REGEX  = r"\bE\d{3}\b"


def extract_entities(text: str) -> dict:
    text = text.upper()
    return {
        "category": re.search(CATEGORY_REGEX, text).group(0) if re.search(CATEGORY_REGEX, text) else None,
        "branch":   re.search(BRANCH_REGEX, text).group(0) if re.search(BRANCH_REGEX, text) else None,
        "college":  re.search(COLLEGE_REGEX, text).group(0) if re.search(COLLEGE_REGEX, text) else None,
    }


# --------------------
# Database Lookups
# --------------------
def find_college_branch(college_code, branch_code):
    return CollegeBranch.objects.filter(
        college__college_code=college_code,
        branch__branch_code=branch_code
    ).first()


def lookup_cutoff(college_branch, category):
    return Cutoff.objects.filter(
        college_branch=college_branch,
        category__category_code=category
    ).order_by("-year__year_code").first()


def lookup_seats(college_branch, category):
    return SeatMatrix.objects.filter(
        college_branch=college_branch,
        category__category_code=category
    ).order_by("-year__year_code").first()


# --------------------
# Final Answer Builder
# --------------------
def answer_using_database(message: str) -> dict:
    entities = extract_entities(message)

    college_code = entities["college"]
    branch_code  = entities["branch"]
    category     = entities["category"]

    if not all([college_code, branch_code, category]):
        return {
            "text": "Please specify college code, branch and category clearly (e.g. E041 CSE GM).",
            "details": entities
        }

    cb = find_college_branch(college_code, branch_code)
    if not cb:
        return {"text": "College–Branch combination not found.", "details": entities}

    cutoff = lookup_cutoff(cb, category)
    seats  = lookup_seats(cb, category)

    response = f"**{cb.code_branch} | {category}**\n\n"

    if cutoff:
        response += f"• Latest Cutoff Rank: **{cutoff.cutoff_rank}**\n"
    else:
        response += "• Cutoff data not available\n"

    if seats:
        response += f"• Available Seats: **{seats.available_seats}** / {seats.total_seats}\n"
    else:
        response += "• Seat data not available\n"

    return {
        "text": response.strip(),
        "details": {
            "college_branch": cb.code_branch,
            "category": category,
            "cutoff": cutoff.cutoff_rank if cutoff else None,
            "available_seats": seats.available_seats if seats else None
        }
    }


# --------------------
# LLM Helper
# --------------------
def groq_answer(system_prompt, user_prompt):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )
    return completion.choices[0].message.content
