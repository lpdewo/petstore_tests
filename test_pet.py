import time
import pytest
from conftest import BASE_URL, unique_id, get_pet_with_retry, session

class TestPetCRUD:
# 增
    def test_get_pet_by_id(self):
        pet_id = unique_id()   # 改用动态 ID
        pet_data={
            "id":pet_id,
            "name":"test_dog",
            "status":"available"
        }
        post_resp=session.post(f"{BASE_URL}/pet",json=pet_data,verify=False)
        # print(f"POST 状态码: {post_resp.status_code}")
        # print(f"POST 响应内容: {post_resp.text}")
        assert post_resp.status_code == 200, f"创建失败: {post_resp.text}"

        # 等待一会儿time.sleep(0.5)

        # resp=requests.get(f"{BASE_URL}/pet/{pet_id}")
        resp = get_pet_with_retry(pet_id, expected_name="test_dog")
        # print(f"GET 状态码: {resp.status_code}")
        # print(f"GET 响应内容: {resp.text}")
        assert resp.status_code==200, f"查询失败: {resp.text}"
        assert resp.json()["name"]=="test_dog"
        print("增加宠物测试通过！！")


    # 删除宠物接口
    def test_delete_pet(self):
        pet_id = unique_id()   # 改用动态 ID
        pet_data={
            "id":pet_id,
            "name":"to_be_deleted",
            "status":"available"
        }
        # requests.post(f"{BASE_URL}/pet",json=pet_data)
        # 创建
        post_resp = session.post(f"{BASE_URL}/pet", json=pet_data,verify=False)
        assert post_resp.status_code == 200, f"创建失败: {post_resp.text}"

        # 等待宠物可查询，并断言成功（这是关键！）
        resp = get_pet_with_retry(pet_id)          # 返回响应对象
        assert resp.status_code == 200, f"创建后无法查询到宠物: {resp.text}"

        time.sleep(0.5)

        # del_resp=session.delete(f"{BASE_URL}/pet/{pet_id}",verify=False)
        # assert del_resp.status_code==200, f"删除失败: {del_resp.text}"# 删除成功通常返回200

        #删除，重试最多5次
        del_success=False
        for attempt in range(5):
            del_resp=session.delete(f"{BASE_URL}/pet/{pet_id}",verify=False)
            if del_resp.status_code==200:
                del_success=True
                break
            time.sleep(0.5)
        assert del_success,f"删除失败，最后状态码：{del_resp.status_code}"

        #再次查找，应该找不到才对
        get_resp=session.get(f"{BASE_URL}/pet/{pet_id}",verify=False)
        assert get_resp.status_code==404
        print("删除宠物测试通过！！") 

    # 改
    def test_update_pet(self):
        pet_id = unique_id()   # 改用动态 ID
        pet_data={
            "id":pet_id,
            "name":"old_name",
            "status":"available"
        }
    # requests.post(f"{BASE_URL}/pet",json=pet_data)
    # 创建
        post_resp = session.post(f"{BASE_URL}/pet", json=pet_data,verify=False)
        assert post_resp.status_code == 200, f"创建失败: {post_resp.text}"
        
        # 等待存在
        get_pet_with_retry(pet_id)

        pet_data["name"]="new_name"
        up_resp=session.put(f"{BASE_URL}/pet",json=pet_data,verify=False)
        assert up_resp.status_code==200, f"更新失败: {up_resp.text}"

        resp = get_pet_with_retry(pet_id, expected_name="new_name")
        assert resp.status_code == 200, f"查询失败: {resp.text}"
        # get_resp=requests.get(f"{BASE_URL}/pet/{pet_id}")# 查询单个宠物
        assert resp.json()["name"]=="new_name"
        print("更新宠物测试成功！")

    # 查
    def test_get_pet(self):
        pet_id=unique_id()
        pet_data={
            "id":pet_id,
            "name":"query_only",
            "status":"available"
        }
        post_resp=session.post(f"{BASE_URL}/pet",json=pet_data,verify=False)
        assert post_resp.status_code==200

        resp=get_pet_with_retry(pet_id,expected_name="query_only")
        assert resp.status_code==200
        assert resp.json()["name"]=="query_only"
        print("独立查询宠物测试通过！")

    #负向
    def test_get_nonexistent_pet(self):
        fake_id=99999999999
        resp=session.get(f"{BASE_URL}/pet/{fake_id}",verify=False)
        assert resp.status_code==404
        print("负向测试：不存在的宠物返回 404")

    def test_update_nonexistent_pet(self):
        fake_id=99999999999
        pet_data={
            "name":"query_only",
            "status":"available"
        }
        
        resp=session.put(f"{BASE_URL}/pet{fake_id}",json=pet_data,verify=False)
        assert resp.status_code==404
        print("负向测试：更新不存在的宠物返回404")

    #参数化测试
    @pytest.mark.parametrize("status",["available","pending","sold"])
    def test_find_pets_by_status(self,status):
        resp=session.get(f"{BASE_URL}/pet/findByStatus",params={"status":status},verify=False)
        assert resp.status_code==200
        pets=resp.json()
        if len(pets)>0:
            for pet in pets:
                assert pet["status"]==status
        print(f"按状态{status}查询成功")



    


