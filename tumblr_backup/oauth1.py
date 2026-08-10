"""OAuth 1.0a credentials for Tumblr API endpoints that require user auth (e.g. drafts)."""

from typing import final

from pydantic import BaseModel, ConfigDict, Field
from requests_oauthlib import OAuth1

__all__ = [
    'OAuthCredentials',
]


@final
class OAuthCredentials(BaseModel):
    model_config = ConfigDict(frozen=True)

    consumer_key: str = Field(alias='oauth_consumer_key')
    consumer_secret: str = Field(alias='oauth_consumer_secret')
    token: str = Field(alias='oauth_token')
    token_secret: str = Field(alias='oauth_token_secret')

    def to_auth(self) -> OAuth1:
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.token,
            resource_owner_secret=self.token_secret,
        )
