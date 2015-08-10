import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role
from StringIO import StringIO

class FlaskTestClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def teardown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, email, password):
        return self.client.post('/auth/login', data = {
            'email':email, 
            'password':password
        }, follow_redirects=True)

    # Test if the home page renders with an anonymous user
    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Stranger' in response.get_data(as_text=True))

    # Test login capabilities
    def test_register_and_login(self):
        #register new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username':'john',
            'password':'cat',
            'password2':'cat'
        })
        self.assertTrue(response.status_code == 302)

        #test invalid username/password
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password':'dog'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('Invalid username or password' in data)

        #login with a new account
        response = self.client.post(url_for('auth.login'), data={
            'email': 'john@example.com',
            'password':'cat'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search('Hi,\s+john!', data))
        self.assertTrue('Your Sequences' in data)

        #test change password
        response = self.client.post(url_for('auth.change_password'), data={
            'old_password' : 'cat',
            'new_password' : 'dog',
            'new_password2' : 'dog'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('Your password has been updated.' in data)

        #log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out.' in data)

    # Test sequence creation and deletion
    def test_sequence_and_photos(self):
        u = User(email='dmb2@clevelandmetroparks.com', username='dakota', password='cat')
        db.session.add(u)
        db.session.commit()
        self.login('dmb2@clevelandmetroparks.com', 'cat')

        # new sequence
        response = self.client.post(url_for('main.new'), data = {
            'label':'test',
            'file[]':(StringIO('my file contents'), 'jpg1.jpg')
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('test' in data)
        
        #test a Photo is created in db
        response = self.client.get(url_for('main.photo', username = u.username, label = 'test', filename = 'jpg1.jpg'))
        data = response.get_data(as_text=True)
        self.assertTrue('my file contents' in data)

        # test deletion
        response = self.client.post(url_for('main.delete', user = u.username, label = 'test'), follow_redirects = True)
        data = response.get_data(as_text=True)
        self.assertFalse('test' in data)
