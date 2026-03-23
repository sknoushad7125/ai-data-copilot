import requests

def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer clearly.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def generate_sql(query):
    prompt = f"""
You are a PostgreSQL expert.

Database Schema:

Table: sales
Columns:
- id (integer)
- customer_name (text)
- revenue (integer)

Rules:
- Only use the given table and columns
- Do NOT hallucinate columns
- Return ONLY SQL query
- No explanation
- Use LIMIT when needed

Examples:
Q: top 3 customers by revenue
A: SELECT customer_name, revenue FROM sales ORDER BY revenue DESC LIMIT 3;

Q: average revenue
A: SELECT AVG(revenue) FROM sales;

Now convert:

User Question:
{query}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"].strip()


def clean_sql(sql):
    sql = sql.strip()

    # remove ```sql blocks if present
    if "```" in sql:
        sql = sql.split("```")[1]

    return sql.replace("sql", "").strip()

def is_safe_query(sql):
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT"]

    for word in dangerous:
        if word in sql.upper():
            return False

    return True
