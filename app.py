from flask import Flask, request, render_template
from ra2 import sql_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    question = ''
    if request.method == 'POST':
        question = request.form['question']
        result = sql_pipeline(question)
    return render_template('index.html', result=result, question=question)

if __name__ == '__main__':
    app.run(debug=True)
