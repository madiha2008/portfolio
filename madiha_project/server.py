"""
Madiha Portfolio - Backend Server
Flask server on port 5001 with admin panel
"""

import os
import sys
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

sys.path.insert(0, os.path.dirname(__file__))
import database as db

app = Flask(__name__, static_folder=None)
CORS(app)

FRONTEND_PATH = os.path.dirname(__file__)

# Initialize database
db.init_database()


# ============ Static File Routes ============

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_PATH, 'index.html')


@app.route('/admin')
def serve_admin():
    return send_from_directory(FRONTEND_PATH, 'admin.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(FRONTEND_PATH, filename)


# ============ API Routes ============

# Profile
@app.route('/api/profile', methods=['GET'])
def get_profile():
    profile = db.get_profile()
    return jsonify(profile) if profile else jsonify({'error': 'Not found'}), 404


# Skills
@app.route('/api/skills', methods=['GET'])
def get_skills():
    return jsonify(db.get_all_skills())


@app.route('/api/skills', methods=['POST'])
def add_skill():
    data = request.get_json()
    skill_id = db.add_skill(
        data.get('name'),
        data.get('emoji', '⚡'),
        data.get('color', '#ff6b9d'),
        data.get('proficiency', 50)
    )
    return jsonify({'id': skill_id, 'message': '✅ Skill added!'}), 201


# Projects
@app.route('/api/projects', methods=['GET'])
def get_projects():
    return jsonify(db.get_all_projects())


@app.route('/api/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    project_id = db.add_project(
        data.get('title'),
        data.get('description'),
        data.get('technologies'),
        data.get('image_url', 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400')
    )
    return jsonify({'id': project_id, 'message': '✅ Project added!'}), 201


# Contact Messages
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.get_json()
    if not all([data.get('name'), data.get('email'), data.get('message')]):
        return jsonify({'error': 'All fields required'}), 400
    
    message_id = db.save_contact_message(
        data.get('name'),
        data.get('email'),
        data.get('message')
    )
    return jsonify({'id': message_id, 'message': '💌 Message received!'}), 201


@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(db.get_all_messages())


@app.route('/api/messages/<int:message_id>/read', methods=['PUT'])
def mark_read(message_id):
    db.mark_message_read(message_id)
    return jsonify({'message': '✅ Marked as read'})


@app.route('/api/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    db.delete_message(message_id)
    return jsonify({'message': '🗑 Message deleted'})


# Visitor Counter
@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    count = db.get_visitor_count()
    return jsonify({'count': count})


@app.route('/api/visitors/increment', methods=['POST'])
def increment_visitors():
    count = db.increment_visitor_count()
    return jsonify({'count': count})


# ============ Error Handlers ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '404 - Not Found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': '500 - Server Error'}), 500


# ============ Main ============

if __name__ == '__main__':
    print("=" * 55)
    print("  🎀 Madiha Firdous - Portfolio Server")
    print("=" * 55)
    print(f"  📁 Frontend: {FRONTEND_PATH}")
    print(f"  🌐 Portfolio: http://localhost:5001")
    print(f"  👑 Admin:     http://localhost:5001/admin")
    print("=" * 55)
    print("\n  Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
