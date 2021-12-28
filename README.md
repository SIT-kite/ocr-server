# 验证码识别服务

Web服务器采用Flask

验证码识别使用ddddocr

使用以下命令安装依赖
```bash
pip install flask
pip install ddddocr
```
服务器默认监听localhost:5000

api路由为 /recognition

使用POST请求传输纯文本的base64后的图片，具体请求格式参考test_recognition.http文件

返回格式为json
```json
{
    "code":0,
    "msg":"成功",
    "data":{
        "captcha":"64f6dc"
    }
}
```