import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'thi0se stfranig shuld be ex34tremlyu haed to gue1s'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	WEBODM_MAIL_SUBJECT_PREFIX = '[WebODM]'
	WEBODM_MAIL_SENDER = 'WebODM Admin <dmb2@clevelandmetroparks.com>'
	WEBODM_ADMIN = os.environ.get('WEBODM_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'postgresql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@localhost/dev_webodm'
	
class TestingConfig(Config):
	TESTING = True
	DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'postgresql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@localhost/test_webodm'

class ProductionConfig(Config):	
	DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
	DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'postgresql://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@localhost/webodm'

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
