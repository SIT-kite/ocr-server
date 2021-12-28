from flask import Flask, request
import ddddocr
import json
from typing import *
ocr = ddddocr.DdddOcr()

app = Flask(__name__)


class ResponseBody(NamedTuple):
    code: int
    msg: str
    data: Optional[Dict[str, object]]

    @staticmethod
    def success(data: Dict[str, object]):
        return ResponseBody(
            code=0,
            msg='成功',
            data=data
        )

    def to_json(self):
        return json.dumps({
            'code': self.code,
            'msg': self.msg,
            'data': self.data,
        })


@app.route('/captcha/recognition', methods=['POST'])
def captcha_recognition() -> str:
    """
    验证码识别
    :return: 识别结果
    """
    try:
        result = ocr.classification(img_base64=request.get_data(as_text=True))
        return ResponseBody.success({'captcha': result}).to_json()
    except Exception as e:
        return ResponseBody(
            code=1,
            msg=str(e),
            data=None,
        ).to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=True)
