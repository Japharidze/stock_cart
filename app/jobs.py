from .stock_api import generate_alerts

def alerts_job():
    generate_alerts(clip_today=True)