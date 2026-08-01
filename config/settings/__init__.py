import os

# Dynamically load settings depending on environment variable, defaulting to development.
env = os.environ.get("DJANGO_ENV", "development").lower()

if env == "production":
    from .production import *
elif env == "testing":
    from .testing import *
else:
    from .development import *
