from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage (data will be lost when server restarts)
enrolled_students = []
queries = []
feedback_list = []
ratings = []

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Serve the frontend"""
    return render_template('index.html')

@app.route('/admin')
def admin():
    """Serve the admin dashboard"""
    return render_template('admin.html')

# ==================== ENROLLMENT API ====================

@app.route('/api/enroll', methods=['POST'])
def enroll_student():
    """Enroll a new student"""
    data = request.json
    email = data.get('email', '').lower().strip()
    
    if not email:
        return jsonify({'success': False, 'message': 'Email is required'}), 400
    
    # Check if already enrolled
    if any(s['email'] == email for s in enrolled_students):
        return jsonify({'success': False, 'message': 'This email is already enrolled'}), 400
    
    student = {
        'id': len(enrolled_students) + 1,
        'email': email,
        'enrolled_at': datetime.now().isoformat(),
        'status': 'active'
    }
    enrolled_students.append(student)
    
    return jsonify({
        'success': True, 
        'message': 'Enrollment successful!', 
        'data': student
    }), 201

# ==================== QUERIES API ====================

@app.route('/api/submit-query', methods=['POST'])
def submit_query():
    """Submit a student query/question"""
    data = request.json
    email = data.get('email', '').lower().strip()
    question = data.get('question', '').strip()
    
    if not email or not question:
        return jsonify({'success': False, 'message': 'Email and question are required'}), 400
    
    query = {
        'id': len(queries) + 1,
        'email': email,
        'question': question,
        'submitted_at': datetime.now().isoformat(),
        'status': 'pending'
    }
    queries.append(query)
    
    return jsonify({
        'success': True, 
        'message': 'Query submitted successfully!', 
        'data': query
    }), 201

# ==================== FEEDBACK API ====================

@app.route('/api/submit-feedback', methods=['POST'])
def submit_feedback():
    """Submit student feedback"""
    data = request.json
    email = data.get('email', '').lower().strip()
    feedback = data.get('feedback', '').strip()
    
    if not email or not feedback:
        return jsonify({'success': False, 'message': 'Email and feedback are required'}), 400
    
    feedback_entry = {
        'id': len(feedback_list) + 1,
        'email': email,
        'feedback': feedback,
        'submitted_at': datetime.now().isoformat()
    }
    feedback_list.append(feedback_entry)
    
    return jsonify({
        'success': True, 
        'message': 'Feedback submitted successfully!', 
        'data': feedback_entry
    }), 201

# ==================== RATING API ====================

@app.route('/api/submit-rating', methods=['POST'])
def submit_rating():
    """Submit user rating"""
    data = request.json
    rating = data.get('rating')
    
    if rating is None or rating < 1 or rating > 5:
        return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
    
    rating_entry = {
        'id': len(ratings) + 1,
        'rating': int(rating),
        'submitted_at': datetime.now().isoformat()
    }
    ratings.append(rating_entry)
    
    return jsonify({
        'success': True, 
        'message': 'Rating submitted successfully!', 
        'data': rating_entry
    }), 201

# ==================== ADMIN STATS API ====================

@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    avg_rating = sum(r['rating'] for r in ratings) / len(ratings) if ratings else 0
    
    return jsonify({
        'total_students': len(enrolled_students),
        'total_queries': len(queries),
        'total_feedback': len(feedback_list),
        'total_ratings': len(ratings),
        'average_rating': round(avg_rating, 2)
    }), 200

# ==================== ADMIN STUDENTS API ====================

@app.route('/api/admin/students', methods=['GET'])
def get_students():
    """Get all enrolled students"""
    return jsonify(enrolled_students), 200

# ==================== ADMIN QUERIES API ====================

@app.route('/api/admin/queries', methods=['GET'])
def get_queries_admin():
    """Get all student queries"""
    return jsonify(queries), 200

# ==================== ADMIN FEEDBACK API ====================

@app.route('/api/admin/feedback', methods=['GET'])
def get_feedback_admin():
    """Get all student feedback"""
    return jsonify(feedback_list), 200

# ==================== ADMIN RATINGS API ====================

@app.route('/api/admin/ratings', methods=['GET'])
def get_ratings_admin():
    """Get all user ratings"""
    return jsonify(ratings), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'success': False, 'message': 'Route not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'success': False, 'message': 'Server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("WE FOR YOU - Backend Server Started")
    print("="*70)
    print("Frontend:     http://127.0.0.1:5000/")
    print("Admin Panel:  http://127.0.0.1:5000/admin")
    print("="*70 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)