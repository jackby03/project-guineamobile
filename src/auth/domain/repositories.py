from abc import ABCMeta, abstractmethod

from src.auth.domain.token import Credential


class CredentialRepositoryInterface(metaclass=ABCMeta):
    """Interface for managing credential objects in a repository.
    This abstract base class defines the contract for credential repository implementations.
    It provides methods for creating and managing credential objects in a storage system.
    Methods:
        create_credential(credential: Credential) -> Credential:
            Creates a new credential record in the repository.
            Args:
                credential (Credential): The credential object to be created.
            Returns:
                Credential: The created credential object with any system-generated fields populated.
            Raises:
                RepositoryError: If there is an error creating the credential in storage.
    """

    @abstractmethod
    async def create_credential(self, credential: Credential) -> Credential:
        pass
