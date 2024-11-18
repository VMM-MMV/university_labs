import unittest
from caesar_naive import *

class TestEncryptFunction(unittest.TestCase):

    def test_encrypt_basic_message(self):
        message = "HELLO"
        key = 1
        result = encrypt_message(message, key)
        self.assertEqual(result, "IFMMP", f"Expected 'IFMMP' but got {result}")

    def test_encrypt_message_with_spaces(self):
        message = "HELLO WORLD"
        key = 1
        result = encrypt_message(message, key)
        self.assertEqual(result, "IFMMPXPSME", f"Expected 'IFMMPXPSME' but got {result}")

    def test_encrypt_lowercase_message(self):
        message = "hello"
        key = 1
        result = encrypt_message(message, key)
        self.assertEqual(result, "IFMMP", f"Expected 'IFMMP' but got {result}")

    def test_encrypt_wrap_around_Z(self):
        message = "XYZ"
        key = 2
        result = encrypt_message(message, key)
        self.assertEqual(result, "ZAB", f"Expected 'ZAB' but got {result}")

    def test_encrypt_large_key(self):
        message = "HELLO"
        key = 26  # Full alphabet rotation
        result = encrypt_message(message, key)
        self.assertEqual(result, "HELLO", f"Expected 'HELLO' but got {result}")

    def test_encrypt_empty_string(self):
        message = ""
        key = 5
        result = encrypt_message(message, key)
        self.assertEqual(result, "", f"Expected an empty string but got {result}")

    def test_decrypt_message(self):
        self.assertEqual(decrypt_message("JGNNQ", 2), "HELLO")
        self.assertEqual(decrypt_message("jgnnq", 2), "HELLO")  # case insensitive
        self.assertEqual(decrypt_message("WHVWPHVVDJH", 3), "TESTMESSAGE")
        self.assertEqual(decrypt_message("BCD", 1), "ABC")

    def test_encrypt_decrypt_consistency(self):
        original_message = "HELLO"
        key = 2
        encrypted = encrypt_message(original_message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted, original_message)

        original_message = "TEST MESSAGE"
        key = 3
        encrypted = encrypt_message(original_message, key)
        decrypted = decrypt_message(encrypted, key)
        self.assertEqual(decrypted.replace(" ", ""), original_message.replace(" ", ""))

if __name__ == "__main__":
    unittest.main()
