from flask import Flask, request
import ddddocr
import json

ocr = ddddocr.DdddOcr()

app = Flask(__name__)


@app.route('/recognition', methods=['POST'])
def recognition() -> str:
    try:
        return json.dumps({
            'code': 0,
            'result': ocr.classification(img_base64=request.get_data(as_text=True))
        })
    except Exception as e:
        return json.dumps({
            'code': 1,
            'result': str(e)
        })


if __name__ == '__main__':
    app.run(host='127.0.0.1',
            port=5000,
            debug=True)
