#!/usr/bin/env python3
"""
Test Django configuration and imports
"""
import os
import sys

# Add the project directory to Python path
sys.path.insert(0, '/usr/src/app')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consultation_analyser.settings.production')

try:
    import django
    print(f"Django version: {django.get_version()}")
    
    django.setup()
    print("✅ Django setup successful")
    
    from django.conf import settings
    print(f"✅ Settings loaded: {settings.DJANGO_SETTINGS_MODULE}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
    
    from consultation_analyser.wsgi import application
    print("✅ WSGI application imported successfully")
    
    from django.core.management import execute_from_command_line
    print("✅ Django management commands available")
    
    print("\n🎉 All Django components loaded successfully!")
    
except Exception as e:
    print(f"❌ Django error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1) 