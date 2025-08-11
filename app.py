from flask import Flask, request, render_template, jsonify
from main import sql_pipeline
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET', 'POST'])
def index(): 
    result = None
    question = ''
    processing_time = 0
    
    if request.method == 'POST':
        question = request.form['question']
        start_time = time.time()
        result = sql_pipeline(question)
        processing_time = round(time.time() - start_time, 2)
    
    return render_template(
        'index.html',
        result=result,
        question=question,
        processing_time=processing_time
    )

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Question is required'}), 400
    
    start_time = time.time()
    result = sql_pipeline(data['question'])
    processing_time = round(time.time() - start_time, 2)
    
    response = {
        'question': data['question'],
        'processing_time': processing_time,
        **result
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)