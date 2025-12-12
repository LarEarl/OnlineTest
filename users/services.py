from typing import Optional
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def authenticate_identifier_password(identifier: str, password: str) -> Optional[User]:
    """
    Аутентифицирует пользователя по username или email.
    Возвращает пользователя при успехе, иначе None.
    """
    if not identifier or not password:
        return None
    user = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()
    if user and user.check_password(password):
        return user
    return None
