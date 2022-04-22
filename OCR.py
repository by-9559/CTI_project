import requests
import json
import base64


HEADER = {
    'Content-Type': 'application/json',
    'X-HW-ID': 'com.huawei.gts.experience4ca',
    'X-HW-APPKEY': '3LYg4LYTPfCgYGA1DePUrAnkryRrTLQqpNLhKNU0DVl35xR4uCsxSDv8GX9JajV1'
}


def general_ocr_v3(img_path):
    with open(img_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    "https://apigw.huawei.com/api/v2/ocr/general-text"
    url = 'https://apigw-02.huawei.com/api/ocr-dev/api/v1/ocr/general-text'
    body = {
        "image_base64": bytes.decode(base64_data),
        "mode": "noah-doc"
    }

    resp = requests.post(url,
                         headers=HEADER,
                         data=json.dumps(body),
                         verify=False)
    result = json.loads(resp.text)
    resp.close()
    return result

if __name__ == '__main__':
    req = general_ocr_v3("EC5293DB-386E-4cf8-BF1D-C84C62316220.png")
    print(req)