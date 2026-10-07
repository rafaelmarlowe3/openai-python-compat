import httpx,os,time
base=os.getenv('OPENAI_BASE_URL','https://argolink.io/v1');h={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'User-Agent':'openai-python-compat/1.0'}
with httpx.Client(timeout=90) as c:
 job=c.post(base+'/videos/generations',headers=h,json={'model':'seedance-2.5','prompt':'A paper boat','duration':5,'resolution':'720p','aspect_ratio':'16:9'}).json()['request_id']
 while True:
  item=c.get(base+'/videos/'+job,headers=h).json()
  if item['status']!='pending':break
  time.sleep(10)
 print(item)
