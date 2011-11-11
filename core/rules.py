# Define how rules are handled

class LoginScanRule:
    """
    Basic Framework for a LoginScan Rule
    Subclasses MUST implement handle(self,data)
    """
    def __init__(self,config):
        self.config = config

    def handle(self,data,ex=None):
        """
        Handles the response from urllib2.urlopen and/or any HTTPError (ex)
        Should return a tuple of score,message where score is [0,1] and message is an optional message.
        """
        return (0,None)

def loadRule(name):
    """ 
    Loads a class from its name.
    TODO: Validate that the class extends LoginScanRule
    """
    # Have to strip off the class name and just get the module
    mod = '.'.join(name.split('.')[:-1])
    mod = __import__(mod)
    for piece in name.split('.')[1:]:
        mod = getattr(mod,piece)
    return mod

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
