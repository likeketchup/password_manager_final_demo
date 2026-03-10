import requests
import pytest


def test_https_connection():
    """Test that the application is running on HTTPS (port 443)"""
    url = "https://localhost:443"
    
    response = requests.get(url, verify=False, timeout=5)
    
    # Verify the connection was successful
    assert response.status_code < 500, "Server should be responding"
    
    # Verify HTTPS is being used
    assert response.url.startswith("https://"), "Connection must use HTTPS protocol"
