"""
Configuration file for settings
"""

SECRET_KEY = '<SECRET KEY>'

ALLOWED_HOSTS = ['*']

DB_NAME = 'snipe'

DB_USERNAME = 'snipe'

DB_PASSWORD = 'snipe'

DB_HOST_NAME = 'localhost'

DB_PORT = '5432'

ADMINS_EMAIL_LIST = [
    # ('Name', 'email@example.com'),
]

# By default multi-tenant. Provide Tenant Id to make it org specific
ADAL_TENANT_ID = 'common'

ADAL_APP_ID = 'APP_ID'

ADAL_APP_SECRET = 'APP_SECRET'
