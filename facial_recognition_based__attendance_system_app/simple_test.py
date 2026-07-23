# simple_test.py
import os
import sys
import django

print("1. Testing basic Python imports...")
try:
    import sqlite3
    print("✓ SQLite imported")
except Exception as e:
    print(f"✗ SQLite error: {e}")

print("\n2. Setting Django settings...")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FRAS.settings')  # Change FRAS to your project name

print("\n3. Trying Django setup...")
try:
    django.setup()
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    import traceback
    traceback.print_exc()

print("\n4. Testing database...")
try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database error: {e}")

print("\n5. Testing URL loading...")
try:
    from django.urls import get_resolver
    resolver = get_resolver()
    print(f"✓ URL resolver loaded. Found {len(resolver.url_patterns)} patterns")
except Exception as e:
    print(f"✗ URL loading error: {e}")