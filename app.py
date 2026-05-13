"""
ETL Pipeline Dashboard — Flask App
Runs the pipeline on demand and shows results in browser.
"""
from flask import Flask, render_template, jsonify, request
import sqlite3, os, subprocess, json
import pandas as pd

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), 'data', 'ghana_finance.db')
LOG = os.path.join(os.path.dirname(__file__), 'data', 'etl.log')

def qry(sql):
    if not os.path.exists(DB):
        return pd.DataFrame()
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

@app.route('/')
def index():
    db_exists = os.path.exists(DB)
    return render_template('index.html', db_exists=db_exists)

@app.route('/run-pipeline', methods=['POST'])
def run_pipeline():
    try:
        result = subprocess.run(
            ['python', 'etl_pipeline.py'],
            capture_output=True, text=True,
            cwd=os.path.dirname(__file__), timeout=60
        )
        return jsonify({'success': result.returncode == 0,
                        'output': result.stdout + result.stderr})
    except Exception as e:
        return jsonify({'success': False, 'output': str(e)})

@app.route('/api/summary')
def summary():
    df = qry("SELECT * FROM macro_summary ORDER BY year")
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/full')
def full():
    df = qry("SELECT * FROM ghana_macro_indicators ORDER BY year")
    return jsonify(df.to_dict(orient='list'))

@app.route('/api/changes')
def changes():
    df = qry("SELECT * FROM yearly_changes ORDER BY year DESC LIMIT 15")
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/log')
def get_log():
    if os.path.exists(LOG):
        with open(LOG) as f:
            lines = f.readlines()[-40:]
        return jsonify({'log': ''.join(lines)})
    return jsonify({'log': 'No log file yet. Run the pipeline first.'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
