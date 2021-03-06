# 光学图像识别(OCR) 后端服务

该服务用于为上应小风筝提供验证码和文本识别功能。Web 服务框架使用了 flask 框架，验证码识别使用了国内的 ddddocr 库。Python 语言中可以很方便地调用相关功能的库。

## 安装

### 使用 pipenv

本项目使用 pipenv 进行虚拟环境隔离与依赖管理，请确保系统中存在`pipenv`命令，若不存在，使用以下命令安装
```bash
pip3 install pipenv
```

可执行以下命令创建虚拟环境并安装所需依赖
```bash
cd ./ocr-server
pipenv install
```

使用命令`pipenv shell`可进入该虚拟环境
使用`python main.py`可运行该项目

### 使用 pip

你也可以直接使用以下命令安装依赖：
```bash
cd ./ocr-server
pip3 install -i requirements.txt
```
注意 windows 系统下使用 `pip` 代替 `pip3`，服务器默认监听 `0.0.0.0:5000`。


## 使用

### 安装

Uwsgi 方式运行：

```bash
uwsgi -c ./uwsgi.ini
```

### 调用

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

## 常见问题

### 
### Python.h 找不到
fatal error: Python.h: No such file or directory
linux环境中, 安装过程中可能会报错#include <Python.h>找不到
使用以下命令安装Python开发依赖
```bash
sudo apt install python3-dev
```