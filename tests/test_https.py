import requests
import pytest
import os


def test_https_connection():
    """Test that the application is running on HTTPS (port 443)"""
    url = "https://localhost:443"
    
    # Use the self-signed certificate from the repo
    cert_path = os.path.join(os.path.dirname(__file__), '..', 'certs', 'localhost.crt')
    
    # Make request with self-signed certificate verification
    response = requests.get(url, verify=cert_path, timeout=5)
    
    # Verify the connection was successful
    assert response.status_code < 500, "Server should be responding"
    
    # Verify HTTPS is being used
    assert response.url.startswith("https://"), "Connection must use HTTPS protocol"
