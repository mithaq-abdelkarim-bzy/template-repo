import logging
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, cast

import jwt
import requests

logger = logging.getLogger(__name__)


@dataclass
class HxRenewCredentials(ABC):
    @abstractmethod
    def generate_bearer_token(self) -> str:
        """Function that returns a valid signed bearer token string for working with the hx Renew API

        Raises:
            NotImplementedError

        Returns:
            str: Valid bearer token strings
        """
        raise NotImplementedError()


@dataclass
class HxRenewSingleApiCallAuth(HxRenewCredentials, ABC):
    @property
    @abstractmethod
    def url(self) -> str:
        raise NotImplementedError()

    def generate_bearer_token(self) -> str:
        response = requests.post(self.url, data=self._to_dict())
        response.raise_for_status()
        try:
            bearer_token = response.json()["access_token"]
            logger.info("Bearer Token created")
            return cast(str, bearer_token)
        except KeyError:
            raise Exception(response.content)

    def _to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AzureADCredentials(HxRenewSingleApiCallAuth):
    azure_ad_tenant: str
    client_id: str
    client_secret: str
    scope: str
    grant_type: str = "client_credentials"

    @property
    def url(self) -> str:
        return f"https://login.microsoftonline.com/{self.azure_ad_tenant}/oauth2/v2.0/token"


class HxRenewAuth:
    def __init__(self, credential: HxRenewCredentials):
        self.cred = credential
        self._bearer_token: Optional[str] = None

    @property
    def bearer_token(self) -> str:
        if self.expired:
            self._bearer_token = self.cred.generate_bearer_token()
        return cast(str, self._bearer_token)

    @property
    def expired(self) -> bool:
        if not self._bearer_token:
            return True
        try:
            headers = jwt.get_unverified_header(self._bearer_token)
            token = jwt.decode(
                self._bearer_token,
                verify=False,
                algorithms=[headers["alg"]],
                options={"verify_signature": False},
            )
            current_epoch = time.time()
            expiry_time = token.get("exp")
            # Give ourselves a 5 minute buffer. To generate a new token
            if not expiry_time or (current_epoch > (expiry_time - 60 * 5)):
                return True
        except jwt.ExpiredSignatureError:
            return True
        return False
