from persistent import Persistent

class IcepapDriverTemplate(Persistent):
    def __init__(self, name, description, cfg):
        self.name = name
        self.description = description
        self.cfg = cfg
