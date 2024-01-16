from django.core.mail import send_mail
from django.utils.html import format_html
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags



def send_confirmation_email(email , code):
    activation_url = f'http://127.0.0.1:8000/api/account/activate/?u={code}'
    context = {'activation_url': activation_url}
    subject = 'Здраствуйте потвердите свое присудствие '
    html_message = render_to_string('activate.html',context)
    plain_message = strip_tags(html_message)
    
    
    send_mail(
        subject,
        plain_message,
        'mp3_club@gmail.com',
        [email],
        html_message=html_message,
        fail_silently=False
    )
def send_confirmation_password(email,code):
    
    send_mail(
            'Подтвердите ваше изменение',
            f'Ваш код подтверждение: {code}',
            'mp3_club@gmail.com',
            [email],
            fail_silently=False,
        )