import base64

import requests


def test_captcha_recognition():
    """
    测试验证码识别服务
    :return:
    """
    with open('test_captcha.jpeg', 'rb') as f:
        base64_result = base64.b64encode(f.read()).decode()
        response = requests.post(
            url='http://localhost:5000/captcha/recognition',
            data=base64_result)
        assert response.json()['result'] == '64f6dc'
