from flask import Flask, request, jsonify
from flask import send_from_directory
from main import app
from requests.exceptions import Timeout, RequestException
from timezonefinder import TimezoneFinder
# import sqlite3  # Commented out as we're transitioning to CSV
import requests
import json
import csv  # Already included for CSV handling
import os  # For environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')
csv_data = []



@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
  return send_from_directory('.',
                             'ai-plugin.json',
                             mimetype='application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
  return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')



@app.route('/')
def hello_world():
    return 'Hello, Jyotish World!'

@app.route('/add_text', methods=['POST'])
def add_text():
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    # Read existing data
    texts = read_csv('texts.csv')
    
    # Generate new id (you can improve this)
    new_id = len(texts) + 1
    
    # Append new data
    texts.append({"id": new_id, "title": title, "content": content})
    
    # Write back to CSV
    write_csv('texts.csv', ['id', 'title', 'content'], texts)
    
    return jsonify({'message': 'Text added successfully'}), 201

@app.route('/get_texts', methods=['GET'])
def get_texts():
    texts = read_csv('texts.csv')
    formatted_texts = [{"id": text["id"], "title": text["title"]} for text in texts]
    print("Function Return:", formatted_texts)
    return jsonify(formatted_texts)

@app.route('/update_text/<int:text_id>', methods=['PUT'])
def update_text(text_id):
    title = request.form.get('title')
    content = request.form.get('content')
    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400
    
    updated = update_csv_row('texts.csv', ['id', 'title', 'content'], text_id, {'title': title, 'content': content})
    
    if not updated:
        return jsonify({'error': 'Text not found'}), 404
    
    return jsonify({'message': 'Text updated successfully'}), 200

@app.route('/delete_text/<int:text_id>', methods=['DELETE'])
def delete_text(text_id):
    deleted = delete_csv_row('texts.csv', text_id)
    
    if not deleted:
        return jsonify({'error': 'Text not found'}), 404
    
    return jsonify({'message': 'Text deleted successfully'}), 200

@app.route('/ask_question', methods=['POST'])
def ask_question():
    data = request.json  # Assuming the data comes in JSON format
    birth_date = data.get('birth_date', None)
    birth_time = data.get('birth_time', None)
    birth_city = data.get('birth_city', None)
    
    if birth_date and birth_time and birth_city:
        try:
            # Convert date to YYYY-MM-DD format
            birth_date = datetime.strptime(birth_date, '%d/%m/%Y').strftime('%Y-%m-%d')
            # Convert time to HH:MM:SS format
            birth_time = datetime.strptime(birth_time, '%I:%M %p').strftime('%H:%M:%S')
        except ValueError:
            return jsonify({"success": False, "message": "Invalid date or time format"}), 400
        
        # Do something with the birth details
        return jsonify({"success": True, "message": "Received birth details"})
    else:
        return jsonify({"success": False, "message": "Missing birth details"}), 400