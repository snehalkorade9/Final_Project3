"""This test the homepage"""

import pytest
from _pytest.fixtures import fixture
from flask import url_for, request, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash

import app
from app import db, User, create_app, auth, songs
from app.db import db

@pytest.fixture()
def create_user(application):
        with application.app_context():
            # new record
            user = User('sk@njit.edu', generate_password_hash('Test123#'))
            user.is_admin = 1
            db.session.add(user)
            db.session.commit()
            user = User('sk1@njit.edu', generate_password_hash('Test123#'))
            db.session.add(user)
            db.session.commit()

@pytest.fixture()
def logged_in_user(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#'     #testing password
        ), follow_redirects=True)

@pytest.fixture()
def logged_in_non_admin_user(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk1@njit.edu',
            password='Test123#'     #testing password
        ), follow_redirects=True)

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


@auth.route('/login', methods=['POST', 'GET'])
def test_valid_user_login(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#',
            #testing password
        ), follow_redirects=True)
        assert rv.request.path == "/dashboard"
        assert b"Welcome1" in rv.data


@auth.route('/login', methods=['POST', 'GET'])
def test_invalid_user_login(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk123@njit.edu',
            password='Test123#'
        ), follow_redirects=True)
        print(rv.data)
        assert rv.request.path == "/login"
        assert b"Invalid username or password" in rv.data


@auth.route('/register', methods=['POST', 'GET'])
def test_register_user(client, application, create_user):
    response = client.get("/register")
    assert response.status_code == 200
    with application.app_context():
        rv = client.post('/register', data=dict(
            email='sk2@njit.edu',
            password='Test123#',
            confirm='Test123#'
        ), follow_redirects=True)
        print("rv.request.path", rv.request.path)
        assert rv.status_code == 200
        assert rv.request.path == "/login"
        assert b"Congratulations" in rv.data


@auth.route('/dashboard')
def test_access_dashboard(client, application, logged_in_user):
    with application.app_context():
        #user = User.query.get(User.id)
        response = client.get("/dashboard")
        assert response.status_code == 200


@auth.route('/dashboard')
def test_deny_access_dashboard(client, application):
    with application.app_context():
        #user = User.query.get(User.id)
        response = client.get("/dashboard")
        assert response.status_code == 302


@songs.route('/songs/upload')
def test_allow_upload_file(client, application, logged_in_user):
    with application.app_context():
        response = client.get("/songs/upload")
        #print("loggen in", response.data)
        assert response.status_code == 200


@songs.route('/songs/upload')
def test_deney_access_upload_file(client, application, logged_in_non_admin_user):
    with application.app_context():
        response = client.get("/songs/upload")
        #print("loggen in", response.data)
        assert response.status_code == 403