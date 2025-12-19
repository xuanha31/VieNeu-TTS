"""
Script để test API VieNeu-TTS
"""
import requests
import json
import time
import os

# Cấu hình
API_URL = "http://localhost:8000"  # Thay bằng Ngrok URL nếu dùng Colab

def test_health_check():
    """Test endpoint root"""
    print("\n" + "="*50)
    print("TEST 1: Health Check")
    print("="*50)
    
    response = requests.get(f"{API_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_status():
    """Test endpoint status"""
    print("\n" + "="*50)
    print("TEST 2: Get Status")
    print("="*50)
    
    response = requests.get(f"{API_URL}/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.status_code == 200

def test_list_voices():
    """Test endpoint list voices"""
    print("\n" + "="*50)
    print("TEST 3: List Voices")
    print("="*50)
    
    response = requests.get(f"{API_URL}/voices")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        voices = response.json()
        print(f"Available voices: {len(voices['voices'])}")
        for name in voices['voices'].keys():
            print(f"  - {name}")
    
    return response.status_code == 200

def test_load_model():
    """Test endpoint load model"""
    print("\n" + "="*50)
    print("TEST 4: Load Model")
    print("="*50)
    
    # Cấu hình model
    config = {
        "backbone": "VieNeu-TTS (GPU)",  # Hoặc "VieNeu-TTS-q4-gguf" cho CPU
        "codec": "NeuCodec (Standard)",
        "device": "Auto",
        "enable_triton": True,
        "max_batch_size": 8
    }
    
    print(f"Loading model with config:")
    print(json.dumps(config, indent=2, ensure_ascii=False))
    
    start_time = time.time()
    response = requests.post(f"{API_URL}/load_model", json=config)
    load_time = time.time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Load Time: {load_time:.2f}s")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_synthesize():
    """Test endpoint synthesize"""
    print("\n" + "="*50)
    print("TEST 5: Synthesize Speech")
    print("="*50)
    
    # Request
    tts_request = {
        "text": "Xin chào, đây là hệ thống chuyển đổi văn bản thành giọng nói tiếng Việt. Hệ thống hỗ trợ nhiều giọng khác nhau từ miền Bắc đến miền Nam.",
        "voice": "Vĩnh (nam miền Nam)",
        "use_batch": True
    }
    
    print(f"Request:")
    print(f"  Text: {tts_request['text'][:50]}...")
    print(f"  Voice: {tts_request['voice']}")
    print(f"  Use Batch: {tts_request['use_batch']}")
    
    start_time = time.time()
    response = requests.post(f"{API_URL}/synthesize", json=tts_request)
    synthesis_time = time.time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Synthesis Time: {synthesis_time:.2f}s")
    
    if response.status_code == 200:
        # Save audio
        output_file = "test_output.wav"
        with open(output_file, "wb") as f:
            f.write(response.content)
        
        file_size = os.path.getsize(output_file)
        print(f"✅ Audio saved to: {output_file}")
        print(f"File size: {file_size / 1024:.2f} KB")
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_synthesize_base64():
    """Test endpoint synthesize base64"""
    print("\n" + "="*50)
    print("TEST 6: Synthesize Speech (Base64)")
    print("="*50)
    
    tts_request = {
        "text": "Đây là test trả về audio dưới dạng base64.",
        "voice": "Ngọc (nữ miền Bắc)",
        "use_batch": True
    }
    
    print(f"Request:")
    print(f"  Text: {tts_request['text']}")
    print(f"  Voice: {tts_request['voice']}")
    
    start_time = time.time()
    response = requests.post(f"{API_URL}/synthesize_base64", json=tts_request)
    synthesis_time = time.time() - start_time
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Synthesis Time: {synthesis_time:.2f}s")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success!")
        print(f"Duration: {result['duration']:.2f}s")
        print(f"Sample Rate: {result['sample_rate']}Hz")
        print(f"Base64 length: {len(result['audio_base64'])} chars")
        
        # Optionally decode and save
        import base64
        audio_bytes = base64.b64decode(result['audio_base64'])
        output_file = "test_output_base64.wav"
        with open(output_file, "wb") as f:
            f.write(audio_bytes)
        print(f"Audio saved to: {output_file}")
        
        return True
    else:
        print(f"❌ Error: {response.text}")
        return False

def test_multiple_voices():
    """Test synthesize với nhiều giọng khác nhau"""
    print("\n" + "="*50)
    print("TEST 7: Multiple Voices")
    print("="*50)
    
    voices_to_test = [
        "Vĩnh (nam miền Nam)",
        "Bình (nam miền Bắc)",
        "Ngọc (nữ miền Bắc)",
        "Dung (nữ miền Nam)"
    ]
    
    text = "Đây là test với nhiều giọng khác nhau."
    
    results = []
    for voice in voices_to_test:
        print(f"\nTesting voice: {voice}")
        
        tts_request = {
            "text": text,
            "voice": voice,
            "use_batch": True
        }
        
        start_time = time.time()
        response = requests.post(f"{API_URL}/synthesize", json=tts_request)
        synthesis_time = time.time() - start_time
        
        if response.status_code == 200:
            output_file = f"test_{voice.replace(' ', '_')}.wav"
            with open(output_file, "wb") as f:
                f.write(response.content)
            
            print(f"  ✅ Success! Time: {synthesis_time:.2f}s, File: {output_file}")
            results.append(True)
        else:
            print(f"  ❌ Failed: {response.text}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print(f"\n📊 Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
    
    return all(results)

def run_all_tests():
    """Chạy tất cả tests"""
    print("\n" + "="*70)
    print("🧪 VieNeu-TTS API Test Suite")
    print("="*70)
    print(f"API URL: {API_URL}")
    
    tests = [
        ("Health Check", test_health_check),
        ("Get Status", test_status),
        ("List Voices", test_list_voices),
        ("Load Model", test_load_model),
        ("Synthesize Speech", test_synthesize),
        ("Synthesize Base64", test_synthesize_base64),
        ("Multiple Voices", test_multiple_voices),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = "✅ PASS" if success else "❌ FAIL"
        except Exception as e:
            print(f"\n❌ Exception in {test_name}: {str(e)}")
            results[test_name] = f"❌ ERROR: {str(e)}"
        
        # Delay giữa các tests
        time.sleep(1)
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results.items():
        print(f"{test_name:.<50} {result}")
    
    passed = sum(1 for r in results.values() if "PASS" in r)
    total = len(results)
    
    print("\n" + "="*70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("="*70)

if __name__ == "__main__":
    import sys
    
    # Cho phép override API URL từ command line
    if len(sys.argv) > 1:
        API_URL = sys.argv[1]
        print(f"Using API URL: {API_URL}")
    
    run_all_tests()
