from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseCommandVerificateUserService(ABC):
    @abstractmethod
    def verificate_password(self):
        raise NotImplementedError()


@dataclass
class BaseCommandAuthenticateUserService(ABC):
    @abstractmethod
    def login(self):
        raise NotImplementedError()


@dataclass
class BaseCommandAddPacketToUserBySessionKeyService(ABC):
    @abstractmethod
    def add_packet_to_user_by_session_key(self):
        raise NotImplementedError()
