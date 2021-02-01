import inspect
from .gui.messagedialogs import MessageDialogs


def loggingInfo(f):
    def wrapper(obj, *args, **kwargs):
        try:
            f_name = f.__name__
            obj.log.info('Entering %s%s ', f_name, args)
            f_params = len((inspect.signature(f)).parameters)
            if f_params == 1:
                if len(args) > 0:
                    obj.log.info('Calling %s without params', f_name)
                result = f(obj)
            elif f_params >= 1:
                result = f(obj, *args, **kwargs)
            obj.log.info('Living %s ', f_name)
            return result
        except Exception as e:
            obj.log.error('Exception on %s: %s', f.__name__, e)
            raise e
    return wrapper


def catchError(msg=''):
    def wrapper(f):
        def _wrapper(obj, *args, **kwargs):
            try:
                return f(obj, *args, **kwargs)
            except Exception as e:
                if msg != '':
                    m = '{}. Icepap Error:\n{}'.format(msg, e)
                else:
                    m = 'Icepap Error:\n{}'.format(e)
                obj.log.error(m)
                MessageDialogs.showErrorMessage(None, 'Runtime Error', m)
        return _wrapper
    return wrapper