# Proxy Pool

## Pre-requriement

Make sure you have install python3.6+ and pip before this.

Execute
```
pip install wheel setuptools.
pip install aiohttp asyncio
pip install flask redis pyquery
sudo apt-get install unzip
wget https://github.com/RunningIkkyu/ProxyPool/archive/master.zip && unzip master.zip && rm master.zip
```

## Run

You can get a random proxy here (Personal light server, please be gentle.):

```
http://45.77.9.33:5555/get
```

Before running this program, make sure your redis server has already been 
running. If you're using Linux, run this to start redis server:

```
redis-server
```

Once you have your redis-server runing, start the *run.py* script:
```
python run.py
```

Then you'll get information on your screen.


