from abc import ABCMeta, abstractmethod

from src.auth.domain.token import Token


class CredentialRepositoryInterface(metaclass=ABCMeta):
    """Interface for managing credential objects in a repository.
    This abstract base class defines the contract for credential repository implementations.
    It provides methods for creating and managing credential objects in a storage system.
    """

    @abstractmethod
    async def create_credential(self, credential: Token) -> Token:
        pass
