from injector import Injector
from api.factories.repository_factory import RepositoryModule
from api.factories.service_factory import ServiceModule

injector = Injector([
    RepositoryModule(),
    ServiceModule(),
])
