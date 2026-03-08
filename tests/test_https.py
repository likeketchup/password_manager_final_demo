import requests
import pytest
import os


def test_https_connection():
    """Test that the application is running on HTTPS (port 443)"""
    url = "https://localhost:443"
    
    # Construct path to the certificate (from repo root)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    cert_path = os.path.join(repo_root, 'certs', 'localhost.crt')
    
    # Use certificate verification if file exists, otherwise allow unverified
    verify_cert = cert_path if os.path.exists(cert_path) else False
    
    # Make request with self-signed certificate verification
    response = requests.get(url, verify=verify_cert, timeout=5)
    
    # Verify the connection was successful
    assert response.status_code < 500, "Server should be responding"
    
    # Verify HTTPS is being used
    assert response.url.startswith("https://"), "Connection must use HTTPS protocol"
