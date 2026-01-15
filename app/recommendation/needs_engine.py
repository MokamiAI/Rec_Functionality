# app/recommendation/needs_engine.py

from typing import List, Dict


# =====================================================
# PROVIDER RESOLUTION (SOUTH AFRICA)
# =====================================================

def resolve_provider(policy_type: str) -> str:
    """
    Returns a South African insurance provider
    relevant to the policy type.
    """
    mapping = {
        "Life Insurance": "Sanlam",
        "Funeral Cover": "AVBOB",
        "Accidental Cover": "Old Mutual",
        "Vehicle Insurance": "OUTsurance",
        "Home & Contents Insurance": "Santam"
    }
    return mapping.get(policy_type, "Insurance Provider")


# =====================================================
# CONFIDENCE SCORING (USER-INPUT BASED)
# =====================================================

def calculate_confidence(profile: dict, policy_type: str) -> int:
    score = 50

    income = profile["monthly_income"]
    dependants = profile["dependants"]
    owns_car = profile["owns_car"]
    owns_home = profile["owns_home"]

    if policy_type == "Life Insurance":
        if dependants > 0:
            score += 30
        if income >= 15_000:
            score += 10

    elif policy_type == "Funeral Cover":
        score += 30
        if dependants > 0:
            score += 10

    elif policy_type == "Accidental Cover":
        if income > 0:
            score += 25

    elif policy_type == "Vehicle Insurance":
        if owns_car:
            score += 40

    elif policy_type == "Home & Contents Insurance":
        if owns_home:
            score += 35
        if income >= 20_000:
            score += 5

    return min(score, 100)


# =====================================================
# PRIORITY BAND (CARD BADGE)
# =====================================================

def derive_priority_band(confidence_score: int) -> str:
    if confidence_score >= 85:
        return "best"
    elif confidence_score >= 70:
        return "medium"
    return "optional"


# =====================================================
# PERSONALISED WHY-IT-MATTERS
# =====================================================

def personalise_why_it_matters(profile: dict) -> List[str]:
    reasons = []

    age = profile["age"]
    income = profile["monthly_income"]

    # Age-based messaging
    if age <= 25:
        reasons.append("Well suited to your age group")
    elif 26 <= age <= 40:
        reasons.append("Relevant for your current life stage")
    else:
        reasons.append("Important protection as responsibilities grow")

    # Budget-based messaging
    if income <= 10_000:
        reasons.append("Designed to fit a tight budget")
    elif income <= 30_000:
        reasons.append("Fits comfortably within your budget")
    else:
        reasons.append("Provides strong cover without straining your budget")

    return reasons


# =====================================================
# NEEDS-BASED RECOMMENDATION ENGINE
# =====================================================

def recommend_policies(profile: dict) -> List[Dict]:
    recommendations = []

    monthly_income = profile["monthly_income"]
    annual_income = monthly_income * 12
    dependants = profile["dependants"]

    personalised_reasons = personalise_why_it_matters(profile)

    # -------------------------------------------------
    # LIFE INSURANCE
    # -------------------------------------------------
    if dependants > 0:
        cover = annual_income * 10
        confidence = calculate_confidence(profile, "Life Insurance")

        recommendations.append({
            "policy_type": "Life Insurance",
            "provider_name": resolve_provider("Life Insurance"),
            "confidence_score": confidence,
            "priority_band": derive_priority_band(confidence),
            "recommended_cover": cover,
            "estimated_monthly_premium": round(cover * 0.0015, 2),
            "best_for": [
                "People with dependants",
                "Households relying on a main income"
            ],
            "why_it_matters": [
                "Provides long-term financial protection",
                "Helps cover living costs, debt, and education",
                *personalised_reasons
            ]
        })

    # -------------------------------------------------
    # FUNERAL COVER (ALWAYS INCLUDED)
    # -------------------------------------------------
    funeral_cover = 50_000 + (dependants * 25_000)
    confidence = calculate_confidence(profile, "Funeral Cover")

    recommendations.append({
        "policy_type": "Funeral Cover",
        "provider_name": resolve_provider("Funeral Cover"),
        "confidence_score": confidence,
        "priority_band": derive_priority_band(confidence),
        "recommended_cover": funeral_cover,
        "estimated_monthly_premium": round(funeral_cover * 0.002, 2),
        "best_for": [
            "All households",
            "Families with dependants"
        ],
        "why_it_matters": [
            "Covers immediate funeral expenses",
            "Pays out quickly when cash is needed",
            *personalised_reasons
        ]
    })

    # -------------------------------------------------
    # ACCIDENTAL COVER
    # -------------------------------------------------
    if monthly_income > 0:
        cover = annual_income * 5
        confidence = calculate_confidence(profile, "Accidental Cover")

        recommendations.append({
            "policy_type": "Accidental Cover",
            "provider_name": resolve_provider("Accidental Cover"),
            "confidence_score": confidence,
            "priority_band": derive_priority_band(confidence),
            "recommended_cover": cover,
            "estimated_monthly_premium": round(cover * 0.002, 2),
            "best_for": [
                "Young professionals",
                "Active individuals"
            ],
            "why_it_matters": [
                "Covers accidental injury and disability",
                "Protects your income if you cannot work",
                *personalised_reasons
            ]
        })

    # -------------------------------------------------
    # VEHICLE INSURANCE
    # -------------------------------------------------
    if profile["owns_car"]:
        confidence = calculate_confidence(profile, "Vehicle Insurance")

        recommendations.append({
            "policy_type": "Vehicle Insurance",
            "provider_name": resolve_provider("Vehicle Insurance"),
            "confidence_score": confidence,
            "priority_band": derive_priority_band(confidence),
            "recommended_cover": "Market value of the vehicle",
            "estimated_monthly_premium": round(monthly_income * 0.03, 2),
            "best_for": [
                "Vehicle owners",
                "Daily commuters"
            ],
            "why_it_matters": [
                "Protects against accidents and theft",
                "Avoids large, unexpected repair costs",
                *personalised_reasons
            ]
        })

    # -------------------------------------------------
    # HOME & CONTENTS INSURANCE
    # -------------------------------------------------
    if profile["owns_home"]:
        confidence = calculate_confidence(profile, "Home & Contents Insurance")

        recommendations.append({
            "policy_type": "Home & Contents Insurance",
            "provider_name": resolve_provider("Home & Contents Insurance"),
            "confidence_score": confidence,
            "priority_band": derive_priority_band(confidence),
            "recommended_cover": "Replacement value of home and contents",
            "estimated_monthly_premium": round(monthly_income * 0.02, 2),
            "best_for": [
                "Homeowners",
                "Property investors"
            ],
            "why_it_matters": [
                "Protects your home and belongings",
                "Safeguards your biggest financial asset",
                *personalised_reasons
            ]
        })

    return recommendations
