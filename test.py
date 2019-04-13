import redis, random


def main():
    db = redis.Redis(host='192.168.1.247', port=6379)
    ming = db.rpop("proxies")
    print(db.type("proxies"))
    proxy = ['HTTPS://163.204.241.5:9999']
    # b = bytes(proxy, encoding='utf-8')
    try:
       if db.sismember("proxies", proxy):
           print('该代理已经存在：', proxy)
       else:
           db.rpush("proxies", proxy)
    except Exception as e:
        print(e)
    # len = db.llen("proxies")
    # zhang = random.randint(0, len)
    # yong = db.lrange("proxies", zhang, zhang)[0].decode('utf-8')
    # print(yong)
    # try:
    #     db.randomkey()
    #     ming = db.rpop("proxies").decode('utf-8')
    #     print(ming)
    #     pass
    # except:
    #     pass


if __name__ == '__main__':
    main()
