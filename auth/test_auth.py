import unittest
from unittest.mock import patch
import authentication

class TestAuthentication(unittest.TestCase):

    @patch('builtins.input', side_effect=['Juan Dela Cruz', 'juandelacruz@email.com'])
    @patch.object(authentication.Authentication, 'get_password', return_value='password123')
    @patch.object(authentication.Authentication, 'save_data')
    @patch.object(authentication.Authentication, 'load_data', return_value=[])
    def test_register_user_success(self, mock_load_data, mock_save_data, mock_get_password, mock_input):
        auth = authentication.Authentication()
        auth.register_user()

        mock_save_data.assert_called_once()
        saved_users = mock_save_data.call_args[0][1]
        self.assertEqual(len(saved_users), 1)
        self.assertEqual(saved_users[0]['email'], 'juandelacruz@email.com')
        self.assertEqual(saved_users[0]['name'], 'Juan Dela Cruz')
        self.assertEqual(saved_users[0]['password'], 'password123')

    @patch('builtins.input', side_effect=['juandelacruz@email.com'])
    @patch.object(authentication.Authentication, 'get_password', return_value='password123')
    @patch.object(authentication.Authentication, 'load_data', return_value=[
        {'user_id': 1, 'name': 'Juan Dela Cruz', 'email': 'juandelacruz@email.com', 'password': 'password123'}
    ])
    def test_login_success(self, mock_load_data, mock_get_password, mock_input):
        auth = authentication.Authentication()
        result = auth.login()
        self.assertTrue(result)
        self.assertIsNotNone(auth.current_user)
        self.assertEqual(auth.current_user['name'], 'Juan Dela Cruz')

    @patch('builtins.input', side_effect=['unknown@email.com'])
    @patch.object(authentication.Authentication, 'get_password', return_value='wrongpass')
    @patch.object(authentication.Authentication, 'load_data', return_value=[
        {'user_id': 1, 'name': 'Juan Dela Cruz', 'email': 'juandelacruz@email.com', 'password': 'password123'}
    ])
    def test_login_failure(self, mock_load_data, mock_get_password, mock_input):
        auth = authentication.Authentication()
        result = auth.login()
        self.assertFalse(result)
        self.assertIsNone(auth.current_user)

if __name__ == '__main__':
    unittest.main(verbosity=2)
