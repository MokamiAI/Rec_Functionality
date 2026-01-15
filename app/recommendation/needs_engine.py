# app/recommendation/needs_engine.py

import os
import requests
from typing import List, Dict


# =====================================================
# SUPABASE CONNECTION
# =====================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}


# =====================================================
# FETCH RECOMMENDATION PRODUCTS (RULES)
# =====================================================

def fetch_recommendation_products() -> List[Dict]:
    url = f"{SUPABASE_URL}/rest/v1/recommendation_products?is_active=eq.true"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()


# =====================================================
# RULE APPLICABILITY CHECK
# =====================================================

def rule_applies(rule: dict, profile: dict) -> bool:
    age = profile["age"]
    income = profile["monthly_income"]

    if rule.get("min_age") and age < rule["min_age"]:
        return False
    if rule.get("max_age") and age > rule["max_age"]:
        return False
    if rule.get("min_monthly_income") and income < rule["min_monthly_income"]:
        return False
    if rule["requires_dependants"] and profile["dependants"] == 0:
        return False
    if rule["requires_car"] and not profile["owns_car"]:
        return False
    if rule["requires_home"] and not profile["owns_home"]:
        return False

    return True


# =====================================================
# CONFIDENCE CALCULATION (FROM TABLE)
# =====================================================

def calculate_confidence(rule: dict, profile: dict) -> int:
    score = rule["base_confidence"]

    # Dependants bonus
    score += profile["dependants"] * rule.get("confidence_per_dependant", 0)

    # Income bonus
    threshold = rule.get("confidence_income_threshold")
    bonus = rule.get("confidence_income_bonus", 0)
    if threshold and profile["monthly_income"] >= threshold:
        score += bonus

    return min(score, 100)


# =====================================================
# PERSONALISED WHY-IT-MATTERS
# =====================================================

def personalise_why_it_matters(profile: dict) -> List[str]:
    reasons = []

    age = profile["age"]
    income = profile["monthly_income"]

    # Age-based
    if age <= 25:
        reasons.append("Well suited to your age group")
    elif 26 <= age <= 40:
        reasons.append("Relevant for your current life stage")
    else:
        reasons.append("Important protection as responsibilities grow")

    # Budget-based
    if income <= 10_000:
        reasons.append("Designed to fit a tight budget")
    elif income <= 30_000:
        reasons.append("Fits comfortably within your budget")
    else:
        reasons.append("Provides strong cover without straining your budget")

    return reasons


# =====================================================
# COVER & PREMIUM CALCULATION
# =====================================================

def calculate_cover_and_premium(rule: dict, profile: dict):
    annual_income = profile["monthly_income"] * 12

    if rule.get("fixed_cover_amount") is not None:
        cover = rule["fixed_cover_amount"]
    elif rule.get("cover_multiplier") is not None:
        cover = annual_income * rule["cover_multiplier"]
    else:
        cover = None

    if rule.get("fixed_premium_amount") is not None:
        premium = rule["fixed_premium_amount"]
    elif rule.get("premium_rate") is not None and cover is not None:
        premium = round(cover * rule["premium_rate"], 2)
    else:
        premium = None

    return cover, premium


# =====================================================
# NEEDS-BASED RECOMMENDATION ENGINE
# =====================================================

def recommend_policies(profile: dict) -> List[Dict]:
    rules = fetch_recommendation_products()
    personalised_reasons = personalise_why_it_matters(profile)

    recommendations = []

    for rule in rules:
        if not rule_applies(rule, profile):
            continue

        confidence = calculate_confidence(rule, profile)

        if confidence < rule["min_confidence_to_show"]:
            continue

        cover, premium = calculate_cover_and_premium(rule, profile)

        recommendations.append({
            "policy_type": rule["policy_type"],
            "provider_name": rule["provider_name"],
            "confidence_score": confidence,
            "priority_band": rule["priority_band"],
            "recommended_cover": cover,
            "estimated_monthly_premium": premium,
            "best_for": rule["best_for"],
            "why_it_matters": [
                *rule["base_why_it_matters"],
                *personalised_reasons
            ]
        })

    return recommendations
