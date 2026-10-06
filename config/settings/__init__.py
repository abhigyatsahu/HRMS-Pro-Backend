import os

# Dynamically load settings depending on environment variable, defaulting to development.
env = os.environ.get("DJANGO_ENV", "development").lower()

if env == "production":
    from config.settings.production import *
elif env == "testing":
    from config.settings.testing import *
else:
    from config.settings.development import *
