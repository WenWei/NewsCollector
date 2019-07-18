
class IParser:
    #def show(self): raise NotImplementedError

    def is_match(self, raw_path): raise NotImplementedError

    def parse(self, content): raise NotImplementedError
