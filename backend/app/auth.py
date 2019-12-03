
from rest_framework.authentication import TokenAuthentication

from .utils import Logger

class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate(self, key):
        Logger.info("Login requested")
        super().authenticate(key)
