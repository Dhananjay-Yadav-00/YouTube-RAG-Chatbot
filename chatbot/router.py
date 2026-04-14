def route_question(question):
    q = question.lower()

    if "time" in q or "when" in q:
        return "POSTING_TIME"
    if "title" in q:
        return "TITLE"
    if "topic" in q or "missing" in q:
        return "CONTENT_GAP"
    if "plan" in q:
        return "ACTION_PLAN"
    if "why" in q or "engagement" in q or "views" in q:
        return "PERFORMANCE"
    return "GENERAL"
