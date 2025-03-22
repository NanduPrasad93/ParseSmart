import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ParseSmart.settings")
django.setup()

print("Django setup is successful!")
