import requests
import pytest
import os

"""Test that valid .txt files are accepted"""
def test_valid_txt_file_upload():
    
    
    # Path to test file
    test_file = os.path.join(os.path.dirname(__file__), 'positive.txt')
    
    # Login first
    session = requests.Session()
    session.verify = False
    
    login_data = {
        'username': 'username',
        'password': 'password!'
    }
    
    # Login
    session.post('https://localhost:443/login.php', data=login_data, timeout=5)
    
    # Prepare file upload to vault
    vault_id = 1  # Assuming vault 1 exists
    with open(test_file, 'rb') as f:
        files = {'file': f}
        data = {
            'addUsername': 'testuser',
            'addWebsite': 'testsite.com',
            'addPassword': 'testpass123',
            'addNotes': 'Test notes',
            'vaultId': vault_id
        }
        
        response = session.post(
            f'https://localhost:443/vaults/vault_details.php?vault_id={vault_id}',
            files=files,
            data=data,
            timeout=5
        )
    
    # Should redirect back to vault_details page (success)
    assert 'vault_details.php' in response.url or response.status_code == 200
    assert 'Error' not in response.text

"""Test that invalid .pdf files are rejected"""
def test_invalid_pdf_file_upload():    
    # Path to test file
    test_file = os.path.join(os.path.dirname(__file__), 'negative.pdf')
    
    # Login first
    session = requests.Session()
    session.verify = False
    
    login_data = {
        'username': 'username',
        'password': 'password!'
    }
    
    # Login
    session.post('https://localhost:443/login.php', data=login_data, timeout=5)
    
    # Prepare file upload to vault
    vault_id = 1
    with open(test_file, 'rb') as f:
        files = {'file': f}
        data = {
            'addUsername': 'testuser2',
            'addWebsite': 'testsite2.com',
            'addPassword': 'testpass456',
            'addNotes': 'Test notes',
            'vaultId': vault_id
        }
        
        response = session.post(
            f'https://localhost:443/vaults/vault_details.php?vault_id={vault_id}',
            files=files,
            data=data,
            timeout=5
        )
    
    # Should show error message about file type
    assert 'Error' in response.text or 'Only .txt files allowed' in response.text
    
"""Test that files larger than 100KB are rejected"""
def test_file_too_large():
    # Path to test file (negative.pdf is 131KB, exceeds 100KB limit)
    test_file = os.path.join(os.path.dirname(__file__), 'negative.pdf')
    
    # Login first
    session = requests.Session()
    session.verify = False
    
    login_data = {
        'username': 'username',
        'password': 'password!'
    }
    
    # Login
    session.post('https://localhost:443/login.php', data=login_data, timeout=5)
    
    # Prepare file upload to vault
    vault_id = 1
    with open(test_file, 'rb') as f:
        files = {'file': f}
        data = {
            'addUsername': 'testuser3',
            'addWebsite': 'testsite3.com',
            'addPassword': 'testpass789',
            'addNotes': 'Test notes',
            'vaultId': vault_id
        }
        
        response = session.post(
            f'https://localhost:443/vaults/vault_details.php?vault_id={vault_id}',
            files=files,
            data=data,
            timeout=5
        )
    
    # Should show error message about file size
    assert 'Error' in response.text or 'File too large' in response.text
