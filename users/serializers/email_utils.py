from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse

def send_password_reset_email(user, request):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    reset_url = request.build_absolute_uri(
        reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
    )
    
    message = f"Click the link to reset your password: {reset_url}"
    
    send_mail(
        subject="Password Reset",
        message=message,
        from_email="no-reply@example.com",
        recipient_list=[user.email],
        fail_silently=False,
    )
