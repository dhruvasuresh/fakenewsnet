#!/usr/bin/env python3
"""
Test script to verify model integration is working properly
"""

import requests
import json
import time

def test_backend_health():
    """Test if backend is running and healthy"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            print(f"Models loaded: {response.json()}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_analyze_endpoint():
    """Test the main analyze endpoint with sample tweets"""
    
    # Test cases with expected results
    test_cases = [
        {
            "text": "BREAKING: Massive wildfire spreading rapidly in California! SHARE THIS NOW! #wildfire #california",
            "expected_type": "fake",
            "description": "Fake news with sensationalist language"
        },
        {
            "text": "Firefighters are responding to a wildfire in the northern region. Evacuation orders issued for residents in affected areas.",
            "expected_type": "real",
            "description": "Real disaster report with factual language"
        },
        {
            "text": "Heavy rainfall causing flooding in downtown area. Water levels rising rapidly. Emergency services on scene.",
            "expected_type": "real", 
            "description": "Real flood report"
        },
        {
            "text": "ALIENS CAUSING WEATHER CHANGES! Government hiding the truth! WAKE UP SHEEPLE! #conspiracy #truth",
            "expected_type": "fake",
            "description": "Conspiracy theory fake news"
        }
    ]
    
    print("\n🧪 Testing analyze endpoint...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Input: {test_case['text'][:50]}...")
        
        try:
            response = requests.post(
                'http://localhost:5000/api/analyze',
                json={'text': test_case['text']},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('multimodal_analysis', {}).get('prediction', 'unknown')
                confidence = result.get('multimodal_analysis', {}).get('confidence', 0)
                
                print(f"✅ Response received")
                print(f"   Prediction: {prediction}")
                print(f"   Confidence: {confidence:.2f}")
                print(f"   Expected: {test_case['expected_type']}")
                
                # Check if prediction matches expected type
                if test_case['expected_type'] in prediction:
                    print(f"   ✅ Prediction matches expected type")
                else:
                    print(f"   ⚠️  Prediction doesn't match expected type")
                    
            else:
                print(f"❌ Request failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        
        time.sleep(1)  # Small delay between requests

def test_model_loading():
    """Test if models are properly loaded"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=10)
        if response.status_code == 200:
            models_status = response.json().get('models_loaded', {})
            
            print("\n🔍 Model Loading Status:")
            for model, status in models_status.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {model}: {'Loaded' if status else 'Not loaded'}")
            
            all_loaded = all(models_status.values())
            if all_loaded:
                print("✅ All models are loaded successfully")
            else:
                print("❌ Some models failed to load")
                
            return all_loaded
        else:
            print("❌ Could not check model status")
            return False
    except Exception as e:
        print(f"❌ Error checking model status: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Integration Test")
    print("=" * 50)
    
    # Test 1: Backend health
    if not test_backend_health():
        print("\n❌ Backend is not running. Please start the backend first:")
        print("   cd backend")
        print("   python app.py")
        return
    
    # Test 2: Model loading
    if not test_model_loading():
        print("\n❌ Models are not properly loaded")
        return
    
    # Test 3: Analyze endpoint
    test_analyze_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Integration test completed!")
    print("\nTo start the frontend:")
    print("   cd frontend")
    print("   npm start")

if __name__ == "__main__":
    main()
