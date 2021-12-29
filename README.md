# 光学图像识别(OCR) 后端服务

该服务用于为上应小风筝提供验证码和文本识别功能。Web 服务框架使用了 flask 框架，验证码识别使用了国内的 ddddocr 库。Python 语言中可以很方便地调用相关功能的库。

## pipenv 包管理器

本项目使用 pipenv 进行虚拟环境隔离与依赖管理，请确保系统中存在`pipenv`命令，若不存在，使用以下命令安装
```bash
pip3 install pipenv
```

第一次使用时，先为本项目创建虚拟 Python 隔离环境,
```bash
cd ./ocr-server
pipenv install
```



## 安装

你可以使用以下命令安装依赖：
```bash
cd ./ocr-server
pip3 install -i requirements.txt
```
注意 windows 系统下使用 `pip` 代替 `pip3`，服务器默认监听 `0.0.0.0:5000`。


## 使用

我们提供了两个 API，负责验证码识别和文本识别。两个接口均需在 HTTP request 中的 body 需要传入直接 base64 处理后的图片，具体请求格式可以参考 [test_recognition.http](./test_recognition.http) 文件和测试脚本 [test_recognition.py](./test_recognition.py)。

返回格式包括三个字段：`code`，`data`，`msg`。注意， `code` 为 `0` 表示操作成功，此时 `msg` 字段将被忽略。否则，`data` 字段会被忽略，`msg` 字段会返回一些错误信息提示。

**POST /ocr/captcha**

请求识别验证码

```json
{
    "code": 0,
    "data": "64f6dc"
}
```

**POST /ocr/text**

请求识别中文文本

```json
{
    "code": 0,
    "data": [
        "text1",
        "text2"
    ]
}
```