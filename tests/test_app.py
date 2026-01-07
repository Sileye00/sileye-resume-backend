import json
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import lambda_handler

def test_lambda_handler_new_visitor():
    """Test lambda handler with no existing count"""
    
    # Mock DynamoDB response for new visitor
    with patch('app.table') as mock_table:
        mock_table.get_item.return_value = {}
        mock_table.put_item.return_value = None
        
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['count'] == 1
        assert 'Access-Control-Allow-Origin' in response['headers']

def test_lambda_handler_existing_visitor():
    """Test lambda handler with existing count"""
    
    # Mock DynamoDB response for existing visitor
    with patch('app.table') as mock_table:
        mock_table.get_item.return_value = {'Item': {'count': 5}}
        mock_table.put_item.return_value = None
        
        event = {}
        context = {}
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['count'] == 6