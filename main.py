import mysql.connector
import ollama
import json

with open('config.json') as f:
    db_config = json.load(f)

# Schema description (for LLM context)
SCHEMA = """
Table: customer_behavior_metrics
Columns:
- avg_items_per_transaction (DOUBLE)
- avg_purchase_value (DOUBLE)
- avg_spent_per_category (DOUBLE)
- avg_transaction_value (DOUBLE)
- customer_id (INT)
- days_since_last_purchase (INT)
- in_store_purchases (INT)
- last_purchase_date (TEXT)
- max_single_purchase_value (DOUBLE)
- min_single_purchase_value (DOUBLE)
- online_purchases (INT)
- purchase_frequency (TEXT)
- total_items_purchased (INT)
- total_transactions (INT)

Table: customer_info
Columns:
- age (INT)
- churned (TEXT)
- customer_id (INT)
- education_level (TEXT)
- gender (TEXT)
- income_bracket (TEXT)
- loyalty_program (TEXT)
- marital_status (TEXT)
- membership_years (INT)
- number_of_children (INT)
- occupation (TEXT)

Table: customer_interaction_data
Columns:
- app_usage (TEXT)
- customer_id (INT)
- customer_support_calls (INT)
- email_subscriptions (TEXT)
- social_media_engagement (TEXT)
- website_visits (INT)

Table: product_info
Columns:
- product_brand (TEXT)
- product_category (TEXT)
- product_color (TEXT)
- product_expiry_date (TEXT)
- product_id (INT)
- product_manufacture_date (TEXT)
- product_material (TEXT)
- product_name (TEXT)
- product_rating (DOUBLE)
- product_return_rate (DOUBLE)
- product_review_count (INT)
- product_shelf_life (INT)
- product_size (TEXT)
- product_stock (INT)
- product_weight (DOUBLE)

Table: promotional_data
Columns:
- avg_discount_used (DOUBLE)
- promotion_channel (TEXT)
- promotion_effectiveness (TEXT)
- promotion_end_date (TEXT)
- promotion_id (INT)
- promotion_start_date (TEXT)
- promotion_target_audience (TEXT)
- promotion_type (TEXT)

Table: sales_data
Columns:
- customer_id (INT)
- total_discounts_received (DOUBLE)
- total_returned_items (INT)
- total_returned_value (DOUBLE)
- total_sales (DOUBLE)

Table: transaction_data
Columns:
- customer_id (INT)
- discount_applied (DOUBLE)
- payment_method (TEXT)
- preferred_store (TEXT)
- product_id (INT)
- promotion_id (INT)
- quantity (INT)
- store_location (TEXT)
- transaction_date (TEXT)
- transaction_hour (INT)
- transaction_id (INT)
- unit_price (DOUBLE)
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
        conn = mysql.connector.connect(**db_config)
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