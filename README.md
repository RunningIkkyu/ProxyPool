# Proxy Pool
[![](https://img.shields.io/badge/python-3.6+-brightgreen.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/redis-4.0.0+-brightgreen.svg)](https://redis.io/download)


# Pre-requriements

Make sure you have install python3.6+ and pip:

```
sudo apt-get update && sudo apt-get upgrade
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install redis
```

install unzip
```
sudo apt-get install unzip
```

install requirements:

```
pip install wheel setuptools
pip install aiohttp asyncio
pip install flask redis pyquery
```

also, you can install requirements by this ( only python packages).

```
pip install -r requirements
```

# Installation

Execute

```
wget https://github.com/RunningIkkyu/ProxyPool/archive/master.zip && unzip master.zip && rm master.zip
```

## Run

Before running this program, make sure your redis server has already been 
running. If you're using Linux, run this to start redis server:

```
redis-server
```

Once you have your redis-server runing, start the *run.py* script:
```
python run.py
```

Then you'll get a random proxy by using the API(xxx.xxx.xxx.xxx) is your ip address:


```
http://xxx.xxx.xxx.xxx:555/get
```

# Structure


There are three modules in this project: 


**tester**: Tester proxies in redis by given test url.


**getter**: Getter proxies from wesite or your personal way.(You can rewrite your method in PrivateProxy.py).


**api**: Privide API which let you get random proxy from proxy pool.




# Configuration

You can customize your setting in settings.py.

#### Redis server

**REDIS_HOST**

**REDIS_PORT**

**REIDS_PASSWORD**

#### Proxy Score

**INITIAL_SCORE**

**MAX_SCORE**

**MIN_SCORE**

#### API setting

**API_HOST**

**API_PORT**
