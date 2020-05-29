import unittest
import uuid
import pprint
import json
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core.unittest.runner import RichTestRunner

from spaceone.inventory.connector.gcp_compute_connector import GcpComputeConnector
from spaceone.tester import TestCase, print_json

def random_string():
    return uuid.uuid4().hex


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


class TestGCPComputeConnector(unittest.TestCase):
    config = config.load_config('./config.yml')
    # pprint(config)

    @classmethod
    def setUpClass(cls):
        super(TestGCPComputeConnector, cls).setUpClass()
        # Do your initialize
        cls.credentials = credentials

    @classmethod
    def tearDownClass(cls):
        super(TestGCPComputeConnector, cls).tearDownClass()

    def setUp(self):
        options = {}


    def tearDown(self):
        pass

    def test_init(self):
        pass

    def test_verify(self):

         options = {}
         gcpconnector = GcpComputeConnector(Transaction(), None)
         gcpconnector._setConnect(credentials)

         result = gcpconnector.verify(options, credentials)
         self.assertEqual(result,"ACTIVE")

    def test_gcp_connector_collectinfo(self):
        query = ""

        gcpconnector = GcpComputeConnector(Transaction(), None)
        gcpconnector._setConnect(credentials)

        result = gcpconnector._listInstances(None, None, None, None, query, None)

        for res in result:
           print(res)






if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
