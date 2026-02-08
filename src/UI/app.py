# -*- coding: utf-8 -*-
"""
StudyMate Web UI Application

Flask-based local web server for the StudyMate desktop application.
"""

from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# ============== Routes ==============

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')


@app.route('/api/agenda')
def get_agenda():
    """Get today's agenda items"""
    # TODO: Connect to Planner logic
    return jsonify({
        'items': [
            {'id': 1, 'title': 'Chapter 3: Introduction to Calculus', 'course': 'Mathematics', 'completed': False, 'estimated_minutes': 45},
            {'id': 2, 'title': 'Chapter 4: Derivatives', 'course': 'Mathematics', 'completed': False, 'estimated_minutes': 60},
            {'id': 3, 'title': 'Unit 2: Cell Biology', 'course': 'Biology 101', 'completed': True, 'estimated_minutes': 30},
        ]
    })


@app.route('/api/stats')
def get_stats():
    """Get quick stats for dashboard"""
    # TODO: Connect to CourseManager and Planner logic
    return jsonify({
        'active_plans': 2,
        'upcoming_deadlines': [
            {'course': 'Mathematics', 'days': 7, 'due_date': '2026-02-15', 'hours_left': 12},
            {'course': 'Biology 101', 'days': 14, 'due_date': '2026-02-22', 'hours_left': 5},
            {'course': 'Physics', 'days': 21, 'due_date': '2026-03-01', 'hours_left': 18},
        ]
    })


@app.route('/api/courses')
def get_courses():
    """Get all courses"""
    # TODO: Connect to CourseManager
    return jsonify({
        'courses': [
            {'id': 'c1', 'name': 'Mathematics', 'units': 12, 'plans': 1},
            {'id': 'c2', 'name': 'Biology 101', 'units': 8, 'plans': 1},
        ]
    })


@app.route('/api/plans')
def get_plans():
    """Get all active plans"""
    # TODO: Connect to Planner
    return jsonify({
        'plans': [
            {'id': 'p1', 'course': 'Mathematics', 'progress': 45, 'due_date': '2026-02-15', 'status': 'on_track'},
            {'id': 'p2', 'course': 'Biology 101', 'progress': 80, 'due_date': '2026-01-30', 'status': 'ahead'},
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
