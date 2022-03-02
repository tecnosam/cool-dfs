from . import net_interface
from .config import port

net_interface.run('0.0.0.0', port=port, debug=False)
