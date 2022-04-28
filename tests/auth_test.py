"""This test the homepage"""

import pytest
from _pytest.fixtures import fixture
from flask import url_for, request

from app import db, User, create_app
from app.db import db

@pytest.fixture()
def logged_in_user(application):
        with application.app_context():
            # new record
            user = User('sk@njit.edu', 'Test123#')
            db.session.add(user)
            db.session.commit()

def logged_in_user1(client):
    return client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#'
        ), follow_redirects=True)

def test_validate_user1(client):
    rv = client.post('/login', data=dict(
            email='sk@njit.edu',
            password='Test123#'
        ), follow_redirects=True)
    print(rv.data)
    assert b'Welcome' in rv.data



def test_validate_user(client, logged_in_user):
    application = create_app()
    response = client.get("/login")
    assert response.status_code == 200
    response = client.post(("/login"),
        data={'email': 'sk@njit.edu', 'password': 'Test123#'})
    user = User.query.filter_by(email='sk@njit.edu').first()
    assert user.email == 'sk@njit.edu'
    #assert request.path == url_for('auth.dashboard')
    assert user.authenticated == True
    #response = client.get("/dashboard.html")
    #assert response.status_code == 200


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
