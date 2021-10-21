import os
from app import app

if __name__ == '__main__':
    port = int(os.environ('PORT', 5000))
    app.run(host='0.0.0.0', port=port)