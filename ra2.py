import mysql.connector
import ollama

# MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',               # 🔁 your username
    'password': '', # 🔁 your password
    'database': 'ra'        # 🔁 your DB name
}

# Schema description (for LLM context)
SCHEMA = """
Table:customer_behavior_metrics
Columns:
customer_id               | int    |NOT NULL | PRIMARY KEY  
online_purchases          | int    |NOT NULL
in_store_purchases        | int    |NOT NULL 
avg_items_per_transaction | double |NOT NULL
avg_transaction_value     | double |NOT NULL
purchase_frequency        | text   |NOT NULL //can be "Daily", "Weekly", "Monthly" or "Yearly"
avg_purchase_value        | double |NOT NULL
last_purchase_date        | date   |NOT NULL
days_since_last_purchase  | int    |NOT NULL
total_items_purchased     | int    |NOT NULL
total_transactions        | int    |NOT NULL
avg_spent_per_category    | double |NOT NULL
max_single_purchase_value | double |NOT NULL
min_single_purchase_value | double |NOT NULL

Table:customer_info
Columns :
customer_id        | int  |PRIMARY KEY |NOT NULL
age                | int  |NOT NULL
gender             | text |NOT NULL //can be "Female","Male" or "Other"
income_bracket     | text |NOT NULL // can be "Low", "Medium" or "High"
marital_status     | text |NOT NULL //can be "Single", "Married"or "Divorced"
number_of_children | int  |NOT NULL 
education_level    | text |NOT NULL //can be "High School", "Bachelor's", "Master's" or "PhD"
occupation         | text |NOT NULL // can be "Self-Employed", "Employed", "Unemployed" or "Retired"
loyalty_program    | text |NOT NULL //can be "Yes" or "No"
membership_years   | int  |NOT NULL
churned            | text |NOT NULL // can be "Yes" or "No"

"""

# Convert natural language to SQL using Mistral (Ollama)
def get_sql_from_question(question):
    prompt = f"""
You are a helpful assistant that converts natural language questions into SQL queries.
Follow these conditions:
**Response should strictly ONLY contain the SQL query.**
**NO additional statements should be present.**
**Go through the schema carefully before generating the SQL query.**
**When only one attribute is asked to return ,it should be returned along with the PRIMARY KEY of that Table**
**When the question refers to "data" all attributes of the table must be printed.**
**The values in attributes should be returned in the same order as they are present in the schema.**
**Answers should be within the scope of the schema provided.**
**If the question is not answerable with the given schema, respond with "No answer".**
**Go through the schema carefully before generating the SQL query.**


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
