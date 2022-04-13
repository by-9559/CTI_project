from OCR import *
import base64
import os, shutil
import re
import pandas as pd
import numpy as np
import cv2

if os.path.exists(str(r'%s'%(os.path.join(os.path.expanduser("~"), 'Desktop') + "\\screenshot\\"))):
    shutil.rmtree(str(r'%s'%(os.path.join(os.path.expanduser("~"), 'Desktop') + "\\screenshot\\")))

PATHDIR = os.path.join(os.path.expanduser("~"), 'Desktop') + "\\screenshot\\"

TABLIST =   {
        "净含量":"D6",
        "地址":"D8",
        "生产者":"D9",
        "联系方式":"D10",
        "生产日期":"D11",
        "贮存条件":"D13",
        "食品生产许可证编号":"D15",
        "产品标准代号":"D17",
        "辐照食品":"D19",
        "转基因食品":"D21",
        "质量（品质）等级":"D26"
              }

class img_ocr:
    def __init__(self,img_path):
        (
            self.path,
            self.name
        )= os.path.splitext(img_path)
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            res = bytes.decode(base64_data)
        self.img_result = general_ocr_v3(res) 
        if 'details' in self.img_result:
            os.makedirs(PATHDIR+self.path.split('/')[-1])
            self.details = self.img_result['details']
            self.description = self.img_result['description']
            self.img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8),1)
            self.exp =  False
        else:self.exp =  True

    def re2(self, re_list:list):
        result = []
        a = str(self.details).replace("'","").replace(" ","")
        [[result.append(re.findall('\w.*',i)[0][0:-1]) for i in re.findall(r"%s(.*?),"%t,a) if len(re.findall('\w+',i)) > 0] for t in re_list]
        return result

    def productList(self):
        b = {}
        ls = pd.read_excel("标签描述字典.xlsx").to_dict('records')
        for i in ls:
            if not (i['标签描述'] is np.nan):
                b[i["标签名称"]] = self.re2(i['标签描述'].split(","))
                print(i['标签描述'])

        b["食品生产许可证编号"] =  re.findall(r"SC\d{14}",self.description)
        b["产品标准代号"] =  re.findall(r"[A-Z]{1}B[/T]{0,2}\s{0,1}\d{5}",self.description)

        return b

    
    def __xy(self,b,a):
        for _ in a:
            # print(b,_[1])
            if b in _[1]:
                # print(_)
                return _[0]
        return False
    
    def main(self):
        if self.exp:
            print("服务异常可能是图片超过4M")
            return 
        product = self.productList()
        for i in product:
            if product[i]:
                print(i,product[i][0])
                xy = self.__xy(product[i][0],self.details)
                if xy == False:
                    continue
                img = self.img[int(xy[0][1]-xy[1][1]/2):int(xy[0][1]+xy[1][1]/2),int(xy[0][0]-xy[1][0]/2):int(xy[0][0]+xy[1][0]/2)]
                cv2.imencode('.jpg',img)[1].tofile(os.path.join(PATHDIR+self.path.split('/')[-1],i+self.name))
                print("标签截取成功")


if __name__ == '__main__':

    dir = 'Input/'
    for img_path in os.listdir(dir):
        print(img_path)
        if img_path.split(".")[-1] in ['jpg','png']:
            img_ocr(dir+img_path).main()