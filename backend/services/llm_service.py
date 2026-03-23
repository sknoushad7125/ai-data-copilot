import requests

HF_API_KEY = "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"

MODEL_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"


def generate_answer(context_chunks, question):
    context = "\n".join(context_chunks)

    prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer clearly:
"""

    response = requests.post(
        MODEL_URL,
        headers={
            "Authorization": f"Bearer {HF_API_KEY}"
        },
        json={
            "inputs": prompt
        }
    )

    result = response.json()

    # handle HF response format
    if isinstance(result, list):
        return result[0]["generated_text"]

    return str(result)


# ---------- SQL GENERATION ----------
def generate_sql(query):
    prompt = f"""
You are a PostgreSQL expert.

Table: sales
Columns:
- id
- customer_name
- revenue

Rules:
- Return ONLY SQL query
- No explanation

User Question:
{query}
"""

    response = requests.post(
        MODEL_URL,
        headers={
            "Authorization": f"Bearer {HF_API_KEY}"
        },
        json={
            "inputs": prompt
        }
    )

    result = response.json()

    if isinstance(result, list):
        return result[0]["generated_text"]

    return str(result)


# ---------- CLEAN SQL ----------
def clean_sql(sql):
    sql = sql.strip()

    if "```" in sql:
        sql = sql.split("```")[1]

    return sql.replace("sql", "").strip()


# ---------- SAFETY ----------
def is_safe_query(sql):
    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT"]

    for word in dangerous:
        if word in sql.upper():
            return False

    return True
