# app/recommendation/needs_engine.py

def recommend_policies(profile: dict) -> list[dict]:
    """
    Needs-based insurance recommendation engine.
    Determines what insurance a person SHOULD have
    based on their life profile.
    """

    recommendations = []

    monthly_income = profile["monthly_income"]
    annual_income = monthly_income * 12
    dependants = profile["dependants"]

    # -------------------------------------------------
    # LIFE INSURANCE
    # -------------------------------------------------
    if dependants > 0:
        cover = annual_income * 10  # industry heuristic

        recommendations.append({
            "policy_type": "Life Insurance",
            "recommended_cover": cover,
            "estimated_monthly_premium": round(cover * 0.0015, 2),
            "description": (
                "You have dependants who rely on your income. "
                "Life insurance ensures they are financially protected "
                "if you pass away."
            )
        })

    # -------------------------------------------------
    # FUNERAL COVER (ALMOST ALWAYS REQUIRED)
    # -------------------------------------------------
    funeral_cover = 50_000 + (dependants * 25_000)

    recommendations.append({
        "policy_type": "Funeral Cover",
        "recommended_cover": funeral_cover,
        "estimated_monthly_premium": round(funeral_cover * 0.002, 2),
        "description": (
            "Funeral cover pays out quickly to cover burial costs, "
            "reducing financial stress for your family."
        )
    })

    # -------------------------------------------------
    # DISABILITY INSURANCE
    # -------------------------------------------------
    if profile["employment_type"] in ("employed", "self-employed"):
        cover = annual_income * 5

        recommendations.append({
            "policy_type": "Disability Insurance",
            "recommended_cover": cover,
            "estimated_monthly_premium": round(cover * 0.002, 2),
            "description": (
                "Disability insurance protects your income if illness "
                "or injury prevents you from working."
            )
        })

    # -------------------------------------------------
    # VEHICLE INSURANCE
    # -------------------------------------------------
    if profile["owns_car"]:
        recommendations.append({
            "policy_type": "Vehicle Insurance",
            "recommended_cover": "Market value of the vehicle",
            "estimated_monthly_premium": round(monthly_income * 0.03, 2),
            "description": (
                "Vehicle insurance protects you against accidents, theft, "
                "and damage to your car."
            )
        })

    # -------------------------------------------------
    # HOME & CONTENTS INSURANCE
    # -------------------------------------------------
    if profile["owns_home"]:
        recommendations.append({
            "policy_type": "Home & Contents Insurance",
            "recommended_cover": "Replacement value of home and contents",
            "estimated_monthly_premium": round(monthly_income * 0.02, 2),
            "description": (
                "Home and contents insurance protects your property "
                "and belongings against fire, theft, and other risks."
            )
        })

    return recommendations
