import requests
import pytest
import os


def test_sql_injection_protection():
    """Test that SQL injection attacks are blocked on login page"""
    # Use the self-signed certificate from the repo
    cert_path = os.path.join(os.path.dirname(__file__), '..', 'certs', 'localhost.crt')
    
    session = requests.Session()
    session.verify = cert_path
    
    # SQL injection payload
    sql_injection_payload = "' OR 1=1 --"
    
    login_url = "https://localhost:443/login.php"
    
    # Attempt SQL injection attack
    data = {
        'username': sql_injection_payload,
        'password': 'anything'
    }
    
    response = session.post(login_url, data=data, timeout=5)
    
    # Verify the attack is blocked by checking:
    # 1. We don't get redirected to index.php (successful login)
    # 2. We either get an error message or stay on login page
    assert "index.php" not in response.url, \
        "SQL injection attack should not grant access to index.php"
    
    # 3. Verify error message is displayed
    assert "Invalid username or password" in response.text, \
        "Should show authentication error message"
