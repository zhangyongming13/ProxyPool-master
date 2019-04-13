# Redis数据库的地址和端口
HOST = '192.168.1.247'
PORT = 6379

FLASK_HOST = '192.168.1.247'
FLASK_PORT = '5000'

# 如果Redis有密码，则添加这句密码，否则设置为None或''
PASSWORD = ''

# 获得代理测试时间界限
get_proxy_timeout = 9

# 代理池数量界限
POOL_LOWER_THRESHOLD = 20
POOL_UPPER_THRESHOLD = 175

# 检查周期
VALID_CHECK_CYCLE = 80
POOL_LEN_CHECK_CYCLE = 20

# 测试API，用百度来测试
TEST_API='http://www.baidu.com'

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
}

url_xici = 'https://www.xicidaili.com/nn/{}'
url_ip3366 = 'http://www.ip3366.net/free/?stype=1&page={}'
