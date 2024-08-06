import unittest

from model import session, List_Hosts
from client_interaction.network_scanning import make_scanning


class TestCase(unittest.TestCase):
    def test_add_new_server(self):
        pre_hosts = session.query(List_Hosts).all()
        pre_list = len(pre_hosts)
        make_scanning()
        post_hosts = session.query(List_Hosts).all()
        post_list = len(post_hosts)
        self.assertTrue(pre_list < post_list)
