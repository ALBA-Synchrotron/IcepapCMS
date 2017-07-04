class Singleton(object):
    def __new__(cls, *p, **k):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.init(*p)
        return cls._the_instance
     
    def init(self, *p):
        pass
    
