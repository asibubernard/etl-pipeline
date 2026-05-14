"""
ETL Pipeline Dashboard — Flask App
"""
from flask import Flask, render_template, jsonify, request
import sqlite3, os, subprocess, sys
import pandas as pd

app = Flask(__name__)

# Always resolve paths relative to this file — works on Render, Railway, local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB  = os.path.join(BASE_DIR, 'data', 'ghana_finance.db')
LOG = os.path.join(BASE_DIR, 'data', 'etl.log')
PIPELINE = os.path.join(BASE_DIR, 'etl_pipeline.py')

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
        # Use sys.executable so we always use the same Python/venv as Flask
        result = subprocess.run(
            [sys.executable, PIPELINE],
            capture_output=True, text=True,
            cwd=BASE_DIR, timeout=90
        )
        success = result.returncode == 0
        output  = result.stdout + result.stderr
        return jsonify({'success': success, 'output': output})
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'output': 'Pipeline timed out after 90 seconds.'})
    except Exception as e:
        return jsonify({'success': False, 'output': str(e)})

@app.route('/api/full')
def full():
    df = qry("SELECT * FROM ghana_macro_indicators ORDER BY year")
    if df.empty:
        return jsonify({})
    return jsonify(df.to_dict(orient='list'))

@app.route('/api/summary')
def summary():
    df = qry("SELECT * FROM macro_summary ORDER BY year")
    return jsonify(df.to_dict(orient='records'))

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
