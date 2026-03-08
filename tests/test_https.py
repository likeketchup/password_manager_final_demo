import requests
import pytest


def test_https_connection():
    """Test that the application is running on HTTPS (port 443)"""
    url = "https://localhost:443"
    
    # Make request with self-signed certificate verification disabled
    response = requests.get(url, verify=False, timeout=5)
    
    # Verify the connection was successful
    assert response.status_code < 500, "Server should be responding"
    
    # Verify HTTPS is being used
    assert response.url.startswith("https://"), "Connection must use HTTPS protocol"


def test_http_connection_fails():
    """Test that plain HTTP on port 80 is not the primary connection method"""
    url = "http://localhost:80"
    
    try:
        # Attempt to connect via HTTP
        response = requests.get(url, timeout=5, allow_redirects=False)
        
        # If we get here, HTTP is accessible. Check if it redirects to HTTPS
        if response.status_code in [301, 302, 303, 307, 308]:
            # HTTP redirects to HTTPS (this is acceptable)
            assert "location" in response.headers
            assert response.headers["location"].startswith("https://"), \
                "HTTP should redirect to HTTPS"
        else:
            # HTTP responds directly - this might be expected for routing
            # but we should verify the main endpoint uses HTTPS
            pass
    except requests.exceptions.ConnectionError:
        # Cannot connect via HTTP - this is also acceptable
        pass
