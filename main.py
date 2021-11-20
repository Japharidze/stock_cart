import os
from app import app, scheduler
from app.stock_api import generate_alerts

scheduler.add_job(id='araperi', func=generate_alerts, trigger='interval', days=1)
scheduler.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)