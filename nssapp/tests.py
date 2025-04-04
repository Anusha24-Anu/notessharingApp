from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import CustomUser, UserReg, Notes
from django.utils import timezone

class UserModelTests(TestCase):

    def test_create_user_reg(self):
        """Test creating a UserReg instance."""
        user = CustomUser.objects.create_user(
            username="testuser", password="password123", user_type="nsuser"
        )
        user_reg = UserReg.objects.create(
            admin=user, mobilenumber="12345678901"
        )

        self.assertEqual(user_reg.admin, user)
        self.assertEqual(user_reg.mobilenumber, "12345678901")
        self.assertIsNotNone(user_reg.regdate_at)
    
    def test_create_notes(self):
        """Test creating a Notes instance linked to a UserReg."""
        user = CustomUser.objects.create_user(
            username="testuser", password="password123", user_type="nsuser"
        )
        user_reg = UserReg.objects.create(
            admin=user, mobilenumber="12345678901"
        )
        
        # Create a note
        note = Notes.objects.create(
            nsuser=user_reg,
            notestitle="Test Note",
            subject="Subject 1",
            notesdesc="This is a test note description.",
            file1=None,  # You can test file uploads later
        )
        
        self.assertEqual(note.nsuser, user_reg)
        self.assertEqual(note.notestitle, "Test Note")
        self.assertEqual(note.subject, "Subject 1")
        self.assertEqual(note.notesdesc, "This is a test note description.")
        self.assertIsNotNone(note.created_at)
        self.assertIsNotNone(note.updated_at)
