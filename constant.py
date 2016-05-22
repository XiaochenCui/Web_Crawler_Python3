
class Const(object):
    class ConstError(TypeError): pass

    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError('Can\'t change const.{}'.format(name))
        if not name.isupper():
            raise self.ConstCaseError('Const name {} is not all uppercase'.format(name))
        self.__dict__[name] = value


# import sys
# sys.modules[__name__] = Const()

