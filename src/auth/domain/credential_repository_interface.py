from abc import ABCMeta, abstractmethod

from src.auth.domain.token import Credential


class CredentialRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    async def create_credential(self, credential: Credential) -> Credential:
        pass