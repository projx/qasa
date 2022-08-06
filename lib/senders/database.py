from lib.base import *


########################################################################################################################
## Config Model - Uses pythantic to provide a typed-dict and validation
##

class QDatabase(QSenderModel):
    """
    Config attribs expected for Forwarders, note some attribs are inherited from QSenderModel
    """
    host: str
    port: int
    protocol: int