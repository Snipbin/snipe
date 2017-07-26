REM Azure webjob to sync search

set DJANGO_SETTINGS_MODULE=snipe.settings.production
D:\home\python361x64\python.exe -m pip install -r requirements/production.txt

D:\home\python361x64\python.exe manage.py sync_search
D:\home\python361x64\python.exe manage.py delete_expired_snippets
