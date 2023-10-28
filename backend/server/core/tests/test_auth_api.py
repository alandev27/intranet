import json
import traceback
from ..lib.fs import format_file
from faker import Faker
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import *
fake = Faker()

tot = 0

def fake_image_file() -> SimpleUploadedFile:
        global tot
        image_data = b'fake image data'
        image_file = SimpleUploadedFile(f'fake_image_{tot}.jpg', image_data, content_type='image/jpeg')
        tot+=1
        return image_file

class TestAuthApi(TestCase):
    def setUp(self) -> None:
        self.username = fake.user_name()
        self.password = fake.password()

        self.user = User.objects.create_user(
            username=self.username,
            email=fake.email(),
            password=self.password,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            avatar=format_file(fake_image_file(), 'assets/avatars/'),
        )
    
        self.user.save()

        self.parent = Parent.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )

        self.parent.save()

    def test_post_auth_login_success(self):
        body = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post('/api/auth/login',
                            data=body,
                            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
    def test_post_auth_login_fail(self):
        body = {
            'username': self.username,
            'password': fake.password()
        }

        response = self.client.post('/api/auth/login',
                            data=body,
                            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
    def test_post_auth_logout_success(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post('/api/auth/logout')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
    def test_post_auth_logout_fail(self):
        response = self.client.post('/api/auth/logout')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)

    def test_post_create_user_success(self):
        self.client.login(username=self.username, password=self.password)

        self.user.role = UserRole.ADMIN
        self.user.is_superuser = True

        self.user.save()
        body = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'avatar': fake_image_file(),
            'role': UserRole.PARENT
        }

        response = self.client.post('/api/auth/user/create',
                            body,
                        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_post_create_student_success(self):
        self.client.login(username=self.username, password=self.password)

        self.user.role = UserRole.ADMIN
        self.user.is_superuser = True

        self.user.save()

        body = {
            'username': fake.user_name(),
            'password': fake.password(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'avatar': fake_image_file(),
            'current_grade': fake.random_int(min=1, max=12),
            'guardian': self.parent.id
        }

        response = self.client.post('/api/auth/student/create',
                            body,
                        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
    
    def test_put_edit_student(self):
        self.client.login(username=self.username, password=self.password)

        self.user.role = UserRole.ADMIN
        self.user.is_superuser = True

        self.user.save()

        body = {
            'id': self.user.id,
            'username': fake.user_name(),
            'password': fake.password(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'avatar': fake_image_file(),
            'current_grade': fake.random_int(min=1, max=12),
            'guardian': self.parent.id
        }

        response = self.client.post('/api/auth/student/update',
                            body,
                        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)      
    
    def test_put_edit_user(self):
        self.client.login(username=self.username, password=self.password)

        self.user.role = UserRole.ADMIN
        self.user.is_superuser = True

        self.user.save()

        body = {
            'id': self.user.id,
            'username': fake.user_name(),
            'password': fake.password(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'avatar': fake_image_file(),
            'role': UserRole.PARENT
        }

        response = self.client.post('/api/auth/user/update',
                            body,
                        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)

    def test_put_replace_avatar(self):
        self.client.login(username=self.username, password=self.password)

        self.user.role = UserRole.ADMIN
        self.user.is_superuser = True

        self.user.save()

        body = {
            'user_id': self.user.id,
            'avatar': fake_image_file(),
            'role': UserRole.ADMIN
        }

        response = self.client.post('/api/auth/user/replace_avatar',
                            body,
                        )
        
        print(response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
