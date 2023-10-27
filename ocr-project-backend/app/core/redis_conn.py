import redis
from app.core.settings import settings

def create_redis():
  return redis.ConnectionPool(
    host=settings.RD_HOST, 
    port=settings.RD_PORT, 
    db=0, 
    decode_responses=True
  )

pool = create_redis()