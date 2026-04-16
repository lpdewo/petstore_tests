import time
from conftest import BASE_URL, unique_id, get_pet_with_retry, session

class TestOrderCRUD:
    def _create_temp_pet(self):
        pet_id=unique_id()
        pet_data={
            "id":pet_id,
            "name":"temp_pet_for_order",
            "status":"available"
        }
        post_resp=session.post(f"{BASE_URL}/pet",json=pet_data,verify=False)
        assert post_resp.status_code==200,f"创建临时宠物失败：{post_resp.status_code}-{post_resp.text}"
        return pet_id
    
    #创建订单,订单状态可以是 "placed", "approved", "delivered"
    def test_create_order(self):
        order_id=unique_id()
        pet_id=self._create_temp_pet()
        order_data={
            "id":order_id,
            "petId":pet_id,
            "quantity":0,#数量
            "status":"placed"
        }
        post_resp=session.post(f"{BASE_URL}/store/order",json=order_data,verify=False)
        assert post_resp.status_code==200,f"订单创建失败：{post_resp.status_code}-{post_resp.text}"
        #验证一下，返回订单id是否一致
        assert post_resp.json()["id"]==order_id
        print("创建订单测试通过！")

    #查询订单
    def test_get_order(self):
        order_id=unique_id()
        pet_id=self._create_temp_pet()
        order_data={
            "id":order_id,
            "petId":pet_id,
            "quantity":0,
            "status":"placed"
        }
        post_resp=session.post(f"{BASE_URL}/store/order",json=order_data,verify=False)
        assert post_resp.status_code==200,f"订单未找到:{post_resp.status_code}-{post_resp.text}"
        
        get_resp=None
        for attempt in range(5):
            get_resp=session.get(f"{BASE_URL}/store/order/{order_id}",verify=False)
            if get_resp.status_code==200:
                break
            time.sleep(0.5)
        
        # get_resp=session.get(f"{BASE_URL}/store/order/{order_id}",verify=False)
        assert get_resp.status_code==200,f"查询订单失败:{get_resp.status_code}-{get_resp.text}"

        assert get_resp.json()["id"]==order_id
        print("查询订单测试通过！")

    #删除订单
    def test_delete_order(self):
        order_id=unique_id()
        pet_id=self._create_temp_pet()
        order_data={
            "id":order_id,
            "petId":pet_id,
            "quantity":0,
            "status":"placed"
        }
        post_resp=session.post(f"{BASE_URL}/store/order",json=order_data,verify=False)
        assert post_resp.status_code==200,f"创建订单失败:：{post_resp.status_code}-{post_resp.text}"

        del_resp=False
        for attempt in range(8):
            del_resp=session.delete(f"{BASE_URL}/store/order/{order_id}",verify=False)
            if del_resp.status_code==200:
                break
            time.sleep(0.5)
        assert del_resp.status_code==200,f"删除订单测试失败:{del_resp.status_code}-{del_resp.text}"

        get_resp=session.get(f"{BASE_URL}/store/order/{order_id}", verify=False)

        assert get_resp.status_code == 404, f"删除后仍能查到订单: {get_resp.status_code} - {get_resp.text}"
        print("删除订单测试通过！")
        
    #无改

    #负向
    def test_get_nonexistent_order(self):
        fake_id=9999999999
        resp=session.get(f"{BASE_URL}/store/order/{fake_id}",verify=False)
        assert resp.status_code==404
        print("负向测试：不存在的订单返回404")

    