import base64
import requests


def test_captcha_recognition():
    """ 测试验证码识别服务 """
    with open('test_captcha.jpeg', 'rb') as f:
        base64_result = base64.b64encode(f.read()).decode()

    response = requests.post(url='http://localhost:5000/ocr/captcha', data=base64_result)
    response.raise_for_status()

    assert response.json()['data'] == '64f6dc'


def test_text_recognition():
    """ 测试文字识别服务 """
    with open('book_list_screenshot.png', 'rb') as f:
        base64_result = base64.b64encode(f.read()).decode()

    response = requests.post(url='http://localhost:5000/ocr/text', data=base64_result)
    response.raise_for_status()

    print(response.json())


if __name__ == '__main__':
    test_captcha_recognition()
    test_text_recognition()