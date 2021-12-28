import json
import ddddocr
from typing import *
from flask import Flask, request


# Initialize DdddOcr library (load model)
ocr = ddddocr.DdddOcr()

# Create flask app object
app = Flask('kite-ocr-server')


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
        return ResponseBody(
            code=0,
            data=data
        )

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


#####################################
# OCR service handlers.
#####################################

@app.route('/ocr/captcha', methods=['POST'])
def captcha_recognition() -> str:
    """
    Do captcha recognition by DdddOcr library.
    :return: A json in plain text of a ResponseBody object, wtih data field is the result in str.
    If the captcha is not recognized, return code 1 instead.
    """

    captcha_in_base64 = request.get_data(as_text=True)
    response: ResponseBody

    try:
        # Use DdddOcr to recognize
        response = ocr.classification(img_base64=captcha_in_base64)
    except Exception as e:
        response = ResponseBody(
            code=1,
            msg=str(e),
        )
        response = response.to_json()
    
    return response


# Entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
