import requests
import random
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BASE_URL="https://petstore.swagger.io/v2"

"""随机数
def unique_id():
    return random.randint(100000, 999999)"""

def unique_id():
    return int(time.time() * 1000) % 1000000   # 返回 0~999999 之间的唯一值

def unique_username():
    """返回唯一的用户名（基于时间戳）"""
    return f"user_{int(time.time()*1000)}"

def get_pet_with_retry(pet_id, expected_name=None, max_retries=10, delay=0.8):
    """尝试多次查询宠物，直到成功或超时"""
    for i in range(max_retries):
        resp = requests.get(f"{BASE_URL}/pet/{pet_id}",verify=False)
        if resp.status_code == 200:
            if expected_name is None or resp.json().get("name") == expected_name:
                return resp
        time.sleep(delay)
    return resp  # 返回最后一次响应"""

# 建立全局 Session 对象，所有测试共享
session = requests.Session()
session.verify = False