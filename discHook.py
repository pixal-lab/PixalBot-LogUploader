from dhooks import Webhook, Embed
from datetime import datetime, timedelta
from collections import defaultdict

def lunes():
  hoy = datetime.today()
  lunes = hoy - timedelta(days=hoy.weekday())
  return lunes.strftime('%d/%m/%y')





  # Convertir la diferencia de tiempo en formato hhmmss
  return datetime.utcfromtimestamp(diferencia_segundos).strftime('%Hh %Mm %Ss'), diferencia