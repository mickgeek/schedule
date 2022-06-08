# -*- coding: utf-8 -*-

PRODUCTION = 'production'
DEVELOPMENT = 'development'
mode = DEVELOPMENT

production_database_uri = 'file:/usr/local/sqlite/data/production_schedule.db'
development_database_uri = 'file:/usr/local/sqlite/data/development_schedule.db'
jwt_expiration_time = 60*60*24*30
client_endpoint = 'http://0.0.0.0:3000'
