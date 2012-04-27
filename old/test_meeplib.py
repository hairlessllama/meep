import unittest
import meeplib

# note:
#
# functions start within test_ are discovered and run
#       between setUp and tearDown;
# setUp and tearDown are run *once* for *each* test_ function.

class TestMeepLib(unittest.TestCase):
    def setUp(self):
        u = meeplib.User('a Llama', 'box')
        m = meeplib.Message( 'not', u)
        l = meeplib.Thread('What a great title!')
        l.add_post(m)

    def test_for_message_existence(self):
        x = meeplib.get_all_threads()
        e=x[0].get_all_posts()
        assert len(e) == 1
        assert x[0].title == 'What a great title!'
        assert e[0].post == 'not'

    def test_message_ownership(self):
        x = meeplib.get_all_users()
        assert len(x) == 1
        u = x[0]

        x = meeplib.get_all_messages()
        assert len(x) == 1
        m = x[0]

        assert m.author == u

    def test_get_next_user(self):
        x = meeplib._get_next_user_id()
        assert x == 1 

    def tearDown(self):
        m = meeplib.get_all_threads()
        z = m[0].get_all_posts('id')
        m[0].delete_post(z[0])

        u = meeplib.get_all_users()[0]
        meeplib.delete_user(u)

        assert len(meeplib._messages) == 0
        assert len(meeplib._users) == 0
        assert len(meeplib._user_ids) == 0

if __name__ == '__main__':
    unittest.main()

