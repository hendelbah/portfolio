"""
This module should be used for running this application
"""
from clinic_app import app
from clinic_app.service.populate import populate, clear_tables

if __name__ == '__main__':
    clear_tables()
    populate()
    app.run()
