'''Factories for the different user types.'''

from factory import Factory, SubFactory, Sequence

from django.contrib.auth.models import User
from inventory.user.models import Experimenter, Reader, Lendee

class UserFactory(Factory):
    FACTORY_FOR = User

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = 'abc'
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

class ExperimenterFactory(Factory):
    FACTORY_FOR = Experimenter

    user = SubFactory(UserFactory)

class ReaderFactory(Factory):
    FACTORY_FOR = Reader

    user = SubFactory(UserFactory)
    
class LendeeFactory(Factory):
    FACTORY_FOR = Lendee

    user = SubFactory(UserFactory)