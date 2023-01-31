
def generate_response(message,**kwargs):
  res={
    "message":message
  }
  for k,v in kwargs.items():
    res[k]=v
  
  return res