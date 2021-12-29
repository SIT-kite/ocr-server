import base64
import json
import numpy as np
import ddddocr
from PIL import Image
from io import BytesIO
import flask
from typing import *
from paddleocr import PaddleOCR


# Initialize DdddOcr library (load model)
ocr_captcha = ddddocr.DdddOcr()

# Initialize PaddleOCR library (download and load model)
ocr_text = PaddleOCR(use_angle_cls=True, lang="ch")

# Create flask app object
app = flask.Flask('kite-ocr-server')


class ResponseBody(NamedTuple):
    """
    Class ResponseBody is the class that set and formatten ocr recognizing result.
    Each result consists of three fields: code, msg and data.
    """
    code: int   # 0 if ok. TODO: Add a status code table.
    msg: str    # Error message if code doesn't mean success.
    data: Optional[Dict[str, object]]  # A dict from keys to objects if recognized successfully.

    @staticmethod
    def success(data: Dict[str, object]):
        """
        Create a success response.
        """
        return ResponseBody(code=0, msg=None, data=data)

    @staticmethod
    def failure(code: int, msg: str):
        """
        Create a failure response.
        """
        return ResponseBody(code=code, msg=msg, data=None)

    def to_json(self):
        """
        Convert the response object to plain text in json.
        """
        if self.code == 0:
            # If code is zero, which means the opertaion success, msg field will be ignored.
            return json.dumps({'code': self.code, 'data': self.data})
        else:
            # Else, return with no data, so ignore the data field.
            return json.dumps({'code': self.code, 'msg': self.msg})


def preprocess_captcha(captcha: Image, threshold: int = 130) -> Image:
    """
    Convert captcha image to binary image with a given threshold.
    The default threshold is 130.
    """
    orignal_image = captcha

    # Convert to grey level image 
    image_in_grey  =  orignal_image.convert("L")

    # Setup a converting table with constant threshold
    threshold = 128 if threshold >= 255 or threshold < 0 else threshold
    mapping_table  =  [0] * threshold + [1] * (256 - threshold)

    # Convert to binary image by the table 
    binary_image = image_in_grey.point(mapping_table, '1')
    return binary_image



#####################################
# OCR service handlers.
#####################################

@app.route('/ocr/captcha', methods=['POST'])
def recognize_captcha():
    """
    Do captcha recognition by DdddOcr library.
    :return: A json in plain text of a ResponseBody object, wtih data field is the result in str.
    If the captcha is not recognized, return code 1 instead.
    """

    captcha_in_base64 = flask.request.get_data(as_text=True)
    response: ResponseBody

    try:
        # Use DdddOcr to recognize
        result = ocr_captcha.classification(img_base64=captcha_in_base64)
        response = ResponseBody.success(result)
    except Exception as e:
        response = ResponseBody.failure(1, str(e))

    return response.to_json(), 200, {"Content-Type":"application/json"}


@app.route('/ocr/text', methods=['POST'])
def recognize_text():
    """
    Do text recognition by PaddleOCR library.
    :return: A json in plain text of a ResponseBody object, wtih data field is the result in str.
    If the text is not recognized, return code 1 instead.
    """
    # TODO: Optimize these lines.
    image_in_base64: str = flask.request.get_data(as_text=True)
    image_bytes: bytes = base64.b64decode(image_in_base64)
    image_bytes: BytesIO = BytesIO(image_bytes)
    image: Image = Image.open(image_bytes)

    result = ocr_text.ocr(np.array(image), cls=True, det=False)
    # for line in result:
    #     print(line)

    return ResponseBody.success(result).to_json(), 200, {"Content-Type":"application/json"}


# Entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
