import unittest
import uuid
import pprint
from spaceone.core import config
from spaceone.core.transaction import Transaction
from spaceone.core.unittest.runner import RichTestRunner

from spaceone.inventory.manager.collector_manager import CollectorManager


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


class TestCollector(unittest.TestCase):
    config = config.load_config('./config.yml')

    # pprint(config)

    @classmethod
    def setUpClass(cls):
        super(TestCollector, cls).setUpClass()
        # Do your initialize

    @classmethod
    def tearDownClass(cls):
        super(TestCollector, cls).tearDownClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_verify(self):
        """ Test Verify
        """
        options = {
        }
        mgr = CollectorManager(Transaction())
        result = mgr.verify(options, credentials)

        self.assertEqual(result, 'ACTIVE')

    def test_collect(self):
        options = {}
        filter = {}
        mgr = CollectorManager(Transaction())
        res = mgr.list_resources(options, credentials, filter)
        for re in res:
            print(re)



if __name__ == "__main__":
    unittest.main(testRunner=RichTestRunner)
