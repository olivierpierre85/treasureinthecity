from django.test import TestCase
from django.core.mail import send_mail
from django.test import Client
#import .views

# Test email sending is still working
# don't forget to lauche server : python -m smtpd -n -c DebuggingServer localhost:1025

class showcaseTest(TestCase):
    def test_send_mail_request(self):
        c = Client()
        response = c.post('/en/email', {'name': 'John Doe', 'email': 'j@doe.test', 'phone': '00000', 'message': 'I want stuff test'})
        print(response)
        self.assertIs(response.status_code, 200)