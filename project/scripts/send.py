from accounts.models import User
from .seed_db import get_user_data

user_data = get_user_data(email='Kyrylo.Ktl@gmail.com')
user, created = User.objects.get_or_create(**user_data)
if created:
    user.set_password(',YpLnu7@BP=K5s+T')
    user.save()

user.email_user(subject='Testing', message='testing')

