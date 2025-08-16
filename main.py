import mysql.connector
import ollama
import json

with open('config.json') as f:
    db_config = json.load(f)

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
customer_id        | int  |NOT NULL |PRIMARY KEY
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

Table:product_info
Columns:
customer_id              | int    |NOT NULL  |PRIMARY KEY
product_id               | int    |NOT NULL
product_name             | text   |NOT NULL   //can be "Product A", "Product B", "Product C" or "Product D"
product_category         | text   |NOT NULL   //can be "Furniture","Toys","Groceries","Electronics"or "Clothing"
product_brand            | text   |NOT NULL
product_rating           | double |NOT NULL   //can be between 1 and 5
product_review_count     | int    |NOT NULL
product_stock            | int    |NOT NULL
product_return_rate      | double |NOT NULL
product_size             | text   |NOT NULL   //can be "Small", "Medium" or "Large"
product_weight           | double |NOT NULL
product_color            | text   |NOT NULL   //can be "Red", "Blue", "Green", "Black" or "White"
product_material         | text   |NOT NULL   //can be "Wood", "Plastic", "Metal" or "Glass"
product_manufacture_date | text   |NOT NULL   
product_expiry_date      | text   |NOT NULL
product_shelf_life       | int    |NOT NULL   //in days

Table:promotional_data
Columns:
customer_id               | int    |NOT NULL |PRIMARY KEY
promotion_id              | int    |NOT NULL   
promotion_type            | text   |NOT NULL  //can be "Buy One Get One Free","20% Off"or 'Flash Sale'
promotion_start_date      | text   |NOT NULL 
promotion_end_date        | text   |NOT NULL 
promotion_effectiveness   | text   |NOT NULL //can be "High","Low" or "Medium"
promotion_channel         | text   |NOT NULL //can be "In-store","Social Media" or "Online"
promotion_target_audience | text   |NOT NULL //can be "Returning Customers" or "New Customers"
avg_discount_used         | double |NOT NULL //can range from 0 to 1

Table: sales_data
Columns:
customer_id	             |int    |NOT NULL |PRIMARY KEY
total_sales	             |double |NOT NULL
total_discounts_received |double |NOT NULL
total_returned_items	 |int    |NOT NULL 
total_returned_value	 |double |NOT NULL

Table: transaction_data
Columns:
transaction_id	         |int    |NOT NULL |PRIMARY KEY
customer_id	             |int    |NOT NULL
product_id	             |int    |NOT NULL
promotion_id	         |int    |NOT NULL
transaction_date	     |text   |NOT NULL
transaction_hour	     |int    |NOT NULL
payment_method	         |text   |NOT NULL  //can be "Cash" ,"Credit Card","Mobile Payment" or "Debit Card"
quantity	             |int    |NOT NULL 
unit_price	             |double |NOT NULL
discount_applied	     |double |NOT NULL
preferred_store	         |text   |NOT NULL  // can be "Location A","Location B","Location C" or "Location D"
store_location	         |text   |NOT NULL  // can be "Location A","Location B","Location C" or "Location D"
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
**When the question refers to "total number" or "count" or synonyms of that,only the number should be returned.**
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

# ra2.py

# ... all your existing code ...

def sql_pipeline(question):
    sql = get_sql_from_question(question)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        return {'sql': sql, 'columns': column_names, 'rows': rows}
    except Exception as e:
        return {'sql': sql, 'error': str(e)}