import time
from conftest import BASE_URL,unique_id,unique_username,session

class TestScenarios:
    def test_full_business_flow(self):
        user_data={
            "id": unique_id(),
            "username": unique_username(),
            "firstName": "test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "123456",
            "phone": "1234567890",
            "userStatus": 0
        }
        session.post(f"{BASE_URL}/user",json=user_data,verify=False)

        pet_id=unique_id()
        pet_data={
            "id":pet_id,
            "name":"test_dog",
            "status":"available"
        }
        session.post(f"{BASE_URL}/pet",json=pet_data,verify=False)

        order_id=unique_id()
        order_data={
            "id":order_id,
            "petId":pet_id,
            "quantity":1,#数量
            "status":"placed"
        }
        session.post(f"{BASE_URL}/store/order",json=order_data,verify=False)

        time.sleep(0.5)

        get_resp=session.get(f"{BASE_URL}/store/order/{order_id}",verify=False)
        assert get_resp.status_code==200
        assert get_resp.json()["id"]==order_id

        del_resp=session.delete(f"{BASE_URL}/store/order/{order_id}",verify=False)
        assert del_resp.status_code==200

        session.delete(f"{BASE_URL}/pet/{pet_id}",verify=False)

        print("完整业务流程测试通过")
    
