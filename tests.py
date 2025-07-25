#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path so we can import functions
sys.path.insert(0, '.')

from functions.get_file_content import get_file_content

def test_cli_expected_cases():
    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    test_cli_expected_cases()

def test_lorem_file():
    """Test get_file_content with lorem.txt"""
    
    print("Testing get_file_content('calculator', 'lorem.txt')")
    print("=" * 50)
    
    # Check if calculator directory exists
    if not os.path.exists("calculator"):
        print("❌ Error: 'calculator' directory not found")
        return
    
    # Check if lorem.txt exists in calculator directory
    lorem_path = os.path.join("calculator", "lorem.txt")
    if not os.path.exists(lorem_path):
        print("❌ Error: 'lorem.txt' not found in calculator directory")
        return
    
    # Get file size for reference
    file_size = os.path.getsize(lorem_path)
    print(f"📁 File size: {file_size} bytes")
    
    # Test the function
    result = get_file_content("calculator", "lorem.txt")
    
    # Display results
    print(f"📄 Returned content length: {len(result)} characters")
    print()
    
    # Check if truncation occurred
    if "[...File \"lorem.txt\" truncated at 10000 characters]" in result:
        print("✂️  TRUNCATION OCCURRED")
        content_part = result.split('\n[...File "lorem.txt" truncated at 10000 characters]')[0]
        print(f"   Content before truncation: {len(content_part)} characters")
    else:
        print("📋 NO TRUNCATION (file is under 10,000 characters)")
    
    print()
    print("📖 First 200 characters:")
    print("-" * 40)
    print(repr(result[:200]))
    print()
    print("📖 Last 200 characters:")
    print("-" * 40)
    print(repr(result[-200:]))

def test_truncation_simulation():
    """Create a large file to test truncation"""
    
    print("\n" + "=" * 60)
    print("TESTING TRUNCATION WITH LARGE FILE")
    print("=" * 60)
    
    # Create calculator directory if it doesn't exist
    if not os.path.exists("calculator"):
        os.makedirs("calculator")
    
    # Create a large test file
    large_content = "This is a test line for truncation. " * 500  # Should be > 10,000 chars
    large_file_path = os.path.join("calculator", "large_test.txt")
    
    with open(large_file_path, 'w', encoding='utf-8') as f:
        f.write(large_content)
    
    print(f"📁 Created test file with {len(large_content)} characters")
    
    try:
        # Test the function with large file
        result = get_file_content("calculator", "large_test.txt")
        print(f"📄 Returned content length: {len(result)} characters")
        
        # Check truncation
        if "[...File \"large_test.txt\" truncated at 10000 characters]" in result:
            print("✂️  TRUNCATION SUCCESSFUL")
            content_part = result.split('\n[...File "large_test.txt" truncated at 10000 characters]')[0]
            print(f"   Content before truncation: {len(content_part)} characters")
            
            if len(content_part) == 10000:
                print("✅ Content truncated at exactly 10,000 characters")
            else:
                print(f"❌ Expected 10,000 characters, got {len(content_part)}")
        else:
            print("❌ TRUNCATION FAILED")
        
        print()
        print("📖 Last 100 characters of result:")
        print("-" * 40)
        print(repr(result[-100:]))
        
    finally:
        # Clean up test file
        if os.path.exists(large_file_path):
            os.remove(large_file_path)
            print(f"\n🗑️  Cleaned up test file: large_test.txt")

def test_error_cases():
    """Test error conditions"""
    
    print("\n" + "=" * 60)
    print("TESTING ERROR CASES")
    print("=" * 60)
    
    # Test 1: File outside working directory
    print("Test 1: File outside working directory")
    result1 = get_file_content("calculator", "../config.py")
    print(f"Result: {result1}")
    print()
    
    # Test 2: Non-existent file
    print("Test 2: Non-existent file")
    result2 = get_file_content("calculator", "nonexistent.txt")
    print(f"Result: {result2}")
    print()
    
    # Test 3: Directory instead of file
    if os.path.exists("calculator"):
        print("Test 3: Directory instead of file")
        result3 = get_file_content("calculator", ".")
        print(f"Result: {result3}")

if __name__ == "__main__":
    # Test with your actual lorem.txt
    test_lorem_file()
    
    # Test truncation with a large file
    test_truncation_simulation()
    
    # Test error cases
    test_error_cases()
