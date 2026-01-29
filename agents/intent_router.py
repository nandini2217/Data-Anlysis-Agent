def detect_intent(query: str):
    q = query.lower()

    if any(k in q for k in ["trend", "over time", "monthly", "yearly"]):
        return "trend"

    if any(k in q for k in ["compare", "vs", "difference"]):
        return "compare"

    if any(k in q for k in ["top", "highest", "best"]):
        return "top_k"

    if any(k in q for k in ["distribution", "spread"]):
        return "distribution"

    return "general"
