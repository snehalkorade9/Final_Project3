"""This test the homepage"""

import pytest
from _pytest.fixtures import fixture
from flask import url_for, request, render_template
from flask_login import login_required
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash

import app
from app import db, User, create_app, auth
from app.db import db

@pytest.fixture()
def create_user(application):
        with application.app_context():
            # new record
            user = User('sk@njit.edu', generate_password_hash('Test123#'))
            db.session.add(user)
            db.session.commit()


@auth.route('/login', methods=['POST', 'GET'])
def test_validate_user1(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#'
        ), follow_redirects=True)
        print(rv.data)
        assert b"Welcome1" in rv.data


@auth.route('/login', methods=['POST', 'GET'])
def test_invalidate_user(client, application, create_user):
    with application.app_context():
        rv = client.post('/login', data=dict(
            email='sk123@njit.edu',
            password='Test123#'
        ), follow_redirects=True)
        print(rv.data)
        assert b"Invalid username or password" in rv.data


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
