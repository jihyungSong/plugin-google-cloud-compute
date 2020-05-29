import os
import uuid
import unittest
from spaceone.core.unittest.runner import RichTestRunner
from spaceone.core import config
from spaceone.core import pygrpc
from spaceone.core import utils
from spaceone.core.error import *
from spaceone.tester import TestCase, print_json
from google.protobuf import empty_pb2
from google.protobuf.json_format import MessageToDict

from spaceone.api.inventory.plugin.collector_pb2 import ResourceInfo

import pprint


credentials = {
    "type": "service_account",
    "project_id": "GOOGLE_PROJECT",
    "private_key_id": "PRIVATE_KEY_ID",
    "private_key": "PRIVATE_KEY",
    "CLIENT_EMAIL": "EMAIL",
    "client_id": "CLIENT_ID",
    "auth_uri": "AUTH_URI",
    "token_uri" "TOKEN_URI",
    "auth_provider_x509_cert_url" "",
    "client_x509_cert_url": "",
    "region": "",
    "region_id": "",
    "zone_id": "",
    "identity.project_id" : ""
}


def random_string():
    return uuid.uuid4().hex


class TestCollector(TestCase):

    def _test_verify(self):
        options = {
            "domain": "mz.co.kr"
        }
        v_info = self.inventory.Collector.verify({'options': options, 'credentials': credentials})
        print_json(v_info)

    def test_collect(self):

        options = {}
        filter = {}

        resource_stream = self.inventory.Collector.collect(
            {'options': options, 'credentials': credentials, 'filter': filter})
        print(resource_stream)
        for res in resource_stream:
            print_json(res)


if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
