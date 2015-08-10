import unittest
from app.models import User, AnonymousUser, Role, Permission
from app import create_app, db
from flask import current_app

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue( u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):        
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dpg'))

    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        u = User(email='john@example.com', password='cat')
        self.assertTrue(u.can(Permission.UPLOAD))
        self.assertFalse(u.can(Permission.ADMINISTER))
        self.assertTrue(u.role.name == 'User')

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.UPLOAD))
        self.assertFalse(u.is_administrator())

    def test_administrator(self):
        admin_email = current_app.config['WEBODM_ADMIN']
        u1 = User.query.filter_by(email=admin_email).first()
        u2 = User(email = 'john1@example.com', password = 'dog')
        self.assertTrue(u1.is_administrator())
        self.assertFalse(u2.is_administrator())
