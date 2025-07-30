# filename: nl_to_sql_no_pandas.py

import mysql.connector
import ollama

# MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': '',               # 🔁 your username
    'password': '', # 🔁 your password
    'database': ''        # 🔁 your DB name
}

# Schema description (for LLM context)
SCHEMA = """
Table: employees
Columns:
- id (INT)
- name (VARCHAR)
- age (INT)
- department (VARCHAR)
- salary (FLOAT)

Table: dept
Columns:
- deptID (INT)
- deptname (VARCHAR)


"""

# Convert natural language to SQL using Mistral (Ollama)
def get_sql_from_question(question):
    prompt = f"""
You are a helpful assistant that converts natural language questions into SQL queries.
Response should strictly ONLY contain the SQL query.
NO additional statements should be present.

**When the question refers to "data" all attributes of the table must be printed.**

Use this schema:

{SCHEMA}

Translate the question into SQL:
Question: {question}
SQL:"""

    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content'].strip()

# Run SQL on MySQL and print raw output
def run_sql_query(sql):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql)

        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        cursor.close()
        conn.close()

        # Print headers
        print("\n🧾 Result:")
        print(" | ".join(column_names))
        print("-" * 40)

        # Print each row
        for row in rows:
            print(" | ".join(str(col) for col in row))

    except Exception as e:
        print(f"\n❌ SQL Execution Error: {e}")

# Main program loop
if __name__ == "__main__":
    print("🔍 Natural Language to SQL (Ollama + MySQL)")
    question = input("Enter your question: ")

    print("\n🧠 Generating SQL query...")
    sql = get_sql_from_question(question)
    print("\n💡 Generated SQL:")
    print(sql)

    print("\n📊 Running query on MySQL...")
    run_sql_query(sql)
