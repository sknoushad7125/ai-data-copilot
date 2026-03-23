from sqlalchemy import create_engine, text

engine = create_engine("postgresql://user:pass@localhost:5432/copilot")


def run_sql_query(query):
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [dict(row._mapping) for row in result]
