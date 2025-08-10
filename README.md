AI-Powered: Manufacturing Data Insights & Dynamic Reports via Natural Language

This project was developed as a part of RA_hackathon,by Team Code Crusaders.It enables users to ask database questions in natural language and automatically converts their queries into SQL using an LLM (powered by Ollama and Llama 3). The generated SQL is executed on a MySQL database, and the results are displayed in a user-friendly web interface built with Flask.

Key Features :

Natural Language Query: Enter plain English questions; the app translates them into accurate SQL queries.

LLM-powered Translation: Uses Ollama running Llama 3 to interpret questions based on your database schema.

MySQL Integration: Runs generated SQL queries directly on your MySQL database.

Web UI: Simple, clean Flask-powered website for asking questions and viewing results.

Customizable Schema: Easily adapt the schema section for your own database tables and columns.

Result Visualization: Displays raw result tables and the generated SQL for transparency.

How it works :

User enters a question in natural language (e.g., “Total number of customers?”) in the web app.

The backend sends the question and your schema to the LLM (Ollama), which returns only the SQL query.

The SQL gets executed on the connected MySQL database.

The results (and the SQL statement) are shown on the web UI.

Tech Stack :

Backend: Python, Flask, mysql-connector-python, Ollama API

Frontend: HTML, CSS (customizable for your needs)

LLM: Ollama (Llama 3 or compatible)

Database: MySQL

Getting Started :

Install dependencies from requirements.txt

Configure your MySQL connection in config.json

Start Ollama server and load the desired model

Run the Flask app and open your browser to begin asking questions!
