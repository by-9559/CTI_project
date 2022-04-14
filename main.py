import base64
import os, shutil
import re
import pandas as pd
import numpy as np
import cv2
import loging
from OCR import *
import PIL.Image as tu
from openpyxl.drawing.image import Image
import traceback


log = loging.log()

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


class Img_ocr:
    def __init__(self,img_path):
        (
            self.path,
            self.file_name
        )= os.path.split(img_path)
        with open(img_path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            res = bytes.decode(base64_data)
        self.img_result = general_ocr_v3(res) 
        if 'details' in self.img_result:
            self.img_dir = PATHDIR+self.file_name.split('.')[0]
            os.makedirs(self.img_dir)
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
            if b in _[1]:
                return _[0]
        return False
    
    def main(self):
        if self.exp:
            log.warning("图片可能超过4M 跳过执行")
            return 
        product = self.productList()
        for i in product:
            if product[i]:
                log.info(i+" 结果: "+product[i][0])
                xy = self.__xy(product[i][0],self.details)
                if xy == False:
                    continue
                img = self.img[int(xy[0][1]-xy[1][1]/2):int(xy[0][1]+xy[1][1]/2),int(xy[0][0]-xy[1][0]/2):int(xy[0][0]+xy[1][0]/2)]
                cv2.imencode('.jpg',img)[1].tofile(os.path.join(self.img_dir,i+".jpg"))
                log.info(f"{i}   标签截取成功")


if __name__ == '__main__':

    dir = 'Input/'
    for img_path in os.listdir(dir):
        # print(img_path)
        if img_path.split(".")[-1] in ['jpg','png']:
            log.info(f"任务: {img_path} 开始")
            Img_ocr(dir+img_path).main()
   