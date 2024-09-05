import unittest
from unittest.mock import patch
from flask import url_for
from app import app, mysql
import boto3
from moto import mock_s3
import os
from io import BytesIO


class FlaskAppTests(unittest.TestCase):
    @mock_s3
    def setUp(self):
        # Create a mock S3 bucket
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.s3.create_bucket(Bucket='firstbucket-yosi')
        
        # Configure the Flask test client
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing purposes
        app.config['MYSQL_DB'] = 'test_db'  # Use a test database
        app.config['MYSQL_USER'] = 'noamon22' #os.getenv('MYSQL_USER') #sys.argv[1] #db['mysql_user']
        app.config['MYSQL_PASSWORD'] = 'Tomeron@2024!!' #os.getenv('MYSQL_PASSWORD') #sys.argv[2] #db['mysql_password']
        self.app = app.test_client()
        
        # Set up a MySQL test database (in-memory or test-specific setup)
        with app.app_context():
           self.setup_test_db()

    def tearDown(self):
        # Cleanup after each test
        self.teardown_test_db()

    def setup_test_db(self):
        """Set up the test database."""
        with app.app_context():
            cur = mysql.connection.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS test_db")
        cur.execute("USE test_db")
        cur.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(100))")
        cur.execute("CREATE TABLE IF NOT EXISTS files (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), filename VARCHAR(100), upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        mysql.connection.commit()
        cur.close()

    def teardown_test_db(self):
        """Teardown the test database."""
        with app.app_context():
            cur = mysql.connection.cursor()
        cur.execute("DROP DATABASE IF EXISTS test_db")
        mysql.connection.commit()
        cur.close()
 

    def test_home_page(self):
        """Test that the home page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_signup(self):
        """Test user signup functionality."""
        response = self.app.post('/register', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have successfully signed up!', response.data)

    def test_login(self):
        """Test user login functionality."""
        # First, register a test user
        self.app.post('/register', data=dict(username='testuser', password='password123'), follow_redirects=True)
        # Now, attempt to log in with the same user
        response = self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload', response.data)

    @mock_s3
    def test_file_upload(self):
        """Test file upload functionality."""
        # First, log in a test user
        self.app.post('/register', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)

        # Now, simulate file upload
        data = {
            'file': (BytesIO(b'my file contents'), 'testfile.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        
        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File successfully uploaded', response.data)

        # Verify the file was uploaded to the mock S3 bucket
        response = self.s3.list_objects(Bucket='your-s3-bucket-name')
        self.assertEqual(len(response.get('Contents', [])), 1)
        self.assertEqual(response['Contents'][0]['Key'], 'testfile.txt')

    @mock_s3
    def test_view_files(self):
        """Test viewing uploaded files."""
        # First, log in a test user
        self.app.post('/register', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)

        # Simulate file upload
        data = {
            'file': (BytesIO(b'my file contents'), 'testfile.txt')
        }
        self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

        # Now, visit the files page
        response = self.app.get('/files')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'testfile.txt', response.data)

    @mock_s3
    def test_file_download(self):
        """Test file download functionality."""
        # Log in and upload a file
        self.app.post('/register', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)
        
        data = {
            'file': (BytesIO(b'my file contents'), 'testfile.txt')
        }
        self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

        # Test downloading the file from S3
        response = self.app.get('/uploads/testfile.txt', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'my file contents')


if __name__ == '__main__':
    unittest.main()
