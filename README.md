# Snipe

Privately hosted Gistbin

## Setup (Before Installation)
- Follow all steps mentioned in `INSTALLATION.md`
- Move `snipe/settings/conf.sample.py` to `snipe/settings/conf.py`
- Use Python 3.5
- Install and configure virtualenvwrapper https://virtualenvwrapper.readthedocs.org/en/latest/

## Setting up local machine for development
- In local machine use `pip install -r requirements/local.txt`
- Edit `snipe/settings/conf.py` to your local settings

## Setting up Production server
- In local machine use `pip install -r requirements/production.txt`
- Edit `snipe/settings/conf.py` to add your production level settings
- Set environment variable `DJANGO_SETTINGS_MODULE` to `snipe.settings.production`
- Continue with Django deployment normally
