import os
from app import app, scheduler
from app.jobs import alerts_job

scheduler.add_job(id='alerts job', func=alerts_job, trigger='interval', days=1)
scheduler.start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)