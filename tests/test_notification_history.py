import pytest
import falcon
import json
import unittest
import history
import datetime
import pymongo
from unittest.mock import Mock, MagicMock, patch
from history import app
from history.api import models
from history.api.models import NotificationHistory, HistoryUtil
from falcon import testing

class TestNotificationHistory:

    @patch.object(HistoryUtil,'get_collection')
    @patch('history.api.models.NotificationHistory.get_query')
    @patch('history.api.models.NotificationHistory.get_notifications')
    def test_notification_on_get(self,mock_hutil,mock_getquery,mock_get_notifications):
        req = MagicMock()
        req.context.return_value = {}
        resp = falcon.Response()
        mock_hutil.return_value = {}
        mock_getquery.return_value = {}
        mock_get_notifications.return_value= {}
        NotificationHistory.on_get(req,resp)
        assert resp.status == falcon.HTTP_200
    
    def test_parse_request(self):
        request = MagicMock()
        request.params.keys.return_value = ['lastN']
        req_content = {"lastN":10}
        request.params.__getitem__.side_effect = lambda key: req_content[key]
        assert NotificationHistory.parse_request(request,'test')
    
    def test_parse_request_invalid_lastN(self):
        with pytest.raises(falcon.HTTPInvalidParam):
            request = MagicMock()
            request.params.keys.return_value = ['lastN']
            req_content = {"lastN":"test"}
            request.params.__getitem__.side_effect = lambda key: req_content[key]
            NotificationHistory.parse_request(request,"test")

    def test_parse_request_invalid_hLimit(self):
        with pytest.raises(falcon.HTTPInvalidParam):
            request = MagicMock()
            request.params.keys.return_value = ['hLimit']
            req_content = {"hLimit":"test"}
            request.params.__getitem__.side_effect = lambda key: req_content[key]
            NotificationHistory.parse_request(request,"test")
    
    @patch('pymongo.collection.Collection.find')
    def test_get_notifications(self, mock_find):
        mock_find.return_value = {"meta":[
            {"ts":1567704621},
            {"ts":1567701021},
            {"ts":1567099821}]
        }
        query = {"query":"","filter":"","limit_val":0,"sort":0}
        assert NotificationHistory.get_notifications(mock_find,query) == []            
