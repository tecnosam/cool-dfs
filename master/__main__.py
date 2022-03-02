from master import app
from .config import port


app.run(host='0.0.0.0', port=port,debug=False)