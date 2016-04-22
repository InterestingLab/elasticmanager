from .exceptions import *

def timenow():
    """use django.utils.timezone.now() for timezone aware
    """
    from django.utils import timezone
    return timezone.now()
