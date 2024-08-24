import random
import vonage
from django.utils import timezone
from django.conf import settings

client = vonage.Client(key=settings.VONAGE_API_KEY,
                       secret=settings.VONAGE_API_SECRET)
sms = vonage.Sms(client)


def send_verification_code(user):
    verification_code = str(random.randint(100000, 999999))
    user.verification_code = verification_code
    user.save()

    response_data = sms.send_message({
        'from': 'HuilaXplorer',
        'to': "57" + user.phone_number,
        'text': f'Your verification code is: {verification_code}'
    })

    return response_data


def send_reset_pass_code(user):
    code = str(random.randint(100000, 999999))
    expiration_code = timezone.now() + timezone.timedelta(minutes=1)

    user.code_reset_password = code
    user. expiration_code_reset_password = expiration_code
    user.save()

    reponse_data = sms.send_message({
        'from': 'HuilaXplorer',
        'to': "57" + user.phone_number,
        'text': f'Your reset password code is: {code}'
    })

    return reponse_data
