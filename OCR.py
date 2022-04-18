import requests
import json


HEADER = {
    'Content-Type': 'application/json',
    'X-HW-ID': 'com.huawei.gts.experience4ca',
    'X-HW-APPKEY': '3LYg4LYTPfCgYGA1DePUrAnkryRrTLQqpNLhKNU0DVl35xR4uCsxSDv8GX9JajV1'
}


def general_ocr_v3(image_base64):
    "https://apigw.huawei.com/api/v2/ocr/general-text"
    url = 'https://apigw-02.huawei.com/api/ocr-dev/api/v1/ocr/general-text'
    body = {
        "image_base64": image_base64,
        "mode": "noah-doc"
    }

    resp = requests.post(url,
                         headers=HEADER,
                         data=json.dumps(body),
                         verify=False)
    result = json.loads(resp.text)
    resp.close()
    return result