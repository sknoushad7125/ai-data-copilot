import time

def log_query(query, route, response_time):
    log = {
        "query": query,
        "route": route,
        "response_time": response_time
    }

    print("LOG:", log)

total_queries = 0

def log_query(query, route, response_time):
    global total_queries
    total_queries += 1

    log = {
        "query": query,
        "route": route,
        "response_time": round(response_time, 3),
        "total_queries": total_queries
    }

    print("LOG:", log)
