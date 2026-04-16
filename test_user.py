import time
from conftest import BASE_URL,unique_id,session,unique_username

class TestUserCRUD:

    def _generate_user_data(self,username=None):#我传的话有名字，不传就是none随机生成一个
        if username is None:
            username=unique_username()
        return{
            "id":unique_id(),
            "username":username,
            "firstName": "string",
            "lastName": "string",
            "email": "string",
            "password": "string",
            "phone": "string",
            "userStatus": 0
        }



    #增加新用户
    def test_create_user(self):
        user_data=self._generate_user_data()
        username=user_data["username"]
        post_resp=session.post(f"{BASE_URL}/user",json=user_data,verify=False)
        assert post_resp.status_code==200,f"创建新用户失败:{post_resp.status_code}-{post_resp.text}"

        get_resp=session.get(f"{BASE_URL}/user/{username}",verify=False)
        assert get_resp.status_code==200,f"没有查询到用户:{get_resp.status_code}-{get_resp}"
        print("创建用户测试通过！")

    #删除用户
    def test_delete_user(self):
        user_data=self._generate_user_data()
        username=user_data["username"]
        post_resp=session.post(f"{BASE_URL}/user",json=user_data,verify=False)
        assert post_resp.status_code==200,f"创建用户失败：,{post_resp.status_code}-{post_resp.text}"

        del_success=False
        for attempt in range(8):
            del_resp=session.delete(f"{BASE_URL}/user/{username}",verify=False)
            if del_resp.status_code==200:
                del_success=True
                break
            time.sleep(0.8)
        assert del_success,f"删除用户失败，最后的状态码：{del_resp.status_code}"

        get_resp=session.get(f"{BASE_URL}/user/{username}",verify=False)
        assert get_resp.status_code==404,f"删除后仍能差到用户：,{get_resp.status_code}-{get_resp.text}"
        print("删除用户测试通过！")


    #修改用户信息
    def test_Update_user(self):
        user_data=self._generate_user_data()
        username=user_data["username"]#相当于身份证号
        post_resp=session.post(f"{BASE_URL}/user",json=user_data,verify=False)
        assert post_resp.status_code==200,f"创建用户失败：，{post_resp.status_code}-{post_resp.text}"

        user_data["firstName"]="updatename"#要改的名字
        update_success=False
        for attempt in range(8):
            update_resp=session.put(f"{BASE_URL}/user/{username}",json=user_data,verify=False)
            if update_resp.status_code==200:
                update_success=True
                break
            time.sleep(0.8)
        assert update_success,f"修改用户失败，最后的状态码：{update_resp.status_code}"

        get_resp=session.get(f"{BASE_URL}/user/{username}",verify=False)
        assert get_resp.status_code==200,f"修改用户信息失败：{get_resp.status_code}-{get_resp.text}"
        assert get_resp.json()["firstName"]=="updatename"
        print("修改用户信息测试成功！")

    #查询用户
    def test_Read_user(self):
        user_data=self._generate_user_data()
        username=user_data["username"]
        post_resp=session.post(f"{BASE_URL}/user",json=user_data,verify=False)
        assert post_resp.status_code==200,f"创建用户失败：，{post_resp.status_code}-{post_resp.text}"

        get_resp=session.get(f"{BASE_URL}/user/{username}",verify=False)
        assert get_resp.status_code==200,f"查询用户信息失败：{get_resp.status_code}-{get_resp.text}"
        print("查询用户测试成功！")
       
    #负向
    def test_get_nonexistent_user(self):
        fake_id="user_that_does_not_exist_12345"
        resp=session.get(f"{BASE_URL}/user/{fake_id}",verify=False)
        assert resp.status_code==404
        print("负向测试：不存在的用户返回404")

   


