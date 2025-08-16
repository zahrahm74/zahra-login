"""
Test Script for Flask API
Simple test script to verify API endpoints are working correctly.
"""

import requests
import json
import time

# API Base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_register():
    """Test user registration"""
    print("\nTesting user registration...")
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123",
        "first_name": "نام",
        "last_name": "نام خانوادگی"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\nTesting user login...")
    data = {
        "username": "testuser",
        "password": "SecurePass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_profile(token):
    """Test getting user profile"""
    print("\nTesting get profile...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/auth/profile",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_profile(token):
    """Test updating user profile"""
    print("\nTesting update profile...")
    data = {
        "first_name": "نام جدید",
        "last_name": "نام خانوادگی جدید"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/users/1",  # Assuming user ID is 1
            json=data,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting API Tests...")
    print("=" * 50)
    
    # Test health check
    if not test_health_check():
        print("Health check failed. Make sure the server is running.")
        return
    
    # Test registration
    token = test_register()
    if not token:
        print("Registration failed or user already exists.")
        # Try login instead
        token = test_login()
        if not token:
            print("Login also failed. Check server logs.")
            return
    
    # Test profile endpoints
    if token:
        test_profile(token)
        test_update_profile(token)
    
    print("\n" + "=" * 50)
    print("Tests completed!")

if __name__ == "__main__":
    main()