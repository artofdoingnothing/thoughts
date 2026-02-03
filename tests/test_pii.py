import unittest
import sys
import os

# Add workers directory to path to import tasks
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workers.utils import remove_pii

class TestPIIRemoval(unittest.TestCase):
    def test_remove_email(self):
        text = "Contact me at test@example.com for more info."
        expected = "Contact me at [EMAIL_REDACTED] for more info."
        self.assertEqual(remove_pii(text), expected)

    def test_remove_phone(self):
        text = "Call me at 123-456-7890."
        expected = "Call me at [PHONE_REDACTED]."
        self.assertEqual(remove_pii(text), expected)

    def test_remove_multiple(self):
        text = "Email: foo@bar.com, Phone: (555) 123-4567"
        expected = "Email: [EMAIL_REDACTED], Phone: [PHONE_REDACTED]"
        self.assertEqual(remove_pii(text), expected)

    def test_no_pii(self):
        text = "Just some normal text."
        self.assertEqual(remove_pii(text), text)

if __name__ == '__main__':
    unittest.main()
