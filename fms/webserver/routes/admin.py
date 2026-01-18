# blue print
from flask import Blueprint, redirect, url_for, flash
from flask_dance.contrib.google import google

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_index():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()

    # authenticate
    if user_info['email'] != "f18098123@gmail.com":
        flash("You do not have access to the admin panel.", "error")
        return redirect(url_for("index"))

    return f"Admin Panel - Hello, {user_info['name']} ({user_info['email']})!"

@admin_bp.route('/requests'):
def view_requests():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    user_info = resp.json()
    # authenticate
    if user_info['email'] != "f18098123@gmail.com":
        flash("You do not have access to the admin panel.", "error")
        return redirect(url_for("index"))
    
    # Check for pending role requests
