def route_query(query):
    query = query.lower()

    if "top" in query or "revenue" in query or "average" in query:
        return "sql"

    return "rag"
