import logging
import os

from click.testing import CliRunner

from app import create_database

runner = CliRunner()

def test_create_database():
    response = runner.invoke(create_database)
    assert response.exit_code == 0
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    dbdir = os.path.join(root, '../database')
    # make a directory if it doesn't exist
    assert os.path.exists(dbdir) == True


def test_log_folder_creation():
    """check if info.log is created"""
    root = os.path.dirname(os.path.abspath(__file__))
    print (os.path.join(root, "/flask_auth_logging/app/logs"))
    assert os.path.exists(os.path.join(root, "../logs")) == True

def test_log_file_creation1():
    """check if info.log is created"""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logdir = os.path.join(root, '.\logs','errors.log')
    print(logdir)
    assert os.path.exists(logdir) == True