import  os
import base64
from ocrtools import get_ocr_result

class Ocr_model():
    def __init__(self,name,img_paths,result_root_path,img_type):
        self.name=name
        self.img_paths=img_paths
        self.result_root_path=result_root_path
        self.img_type=img_type

    def ocr_files(self):
        for img_path in self.img_paths:
            img_file_name=os.path.basename(img_path).split('.')[0]
            #print('==========='+img_file_name+'===========')
            f=open(img_path,'rb')
            img_code=base64.b64encode(f.read()).decode('utf-8')
            f.close()
            #print(img_code)
            ocr_result= self.ocr_by_netease(img_code, self.img_type)
            #print(ocr_result)
            return ocr_result


    def ocr_by_netease(self,img_code,img_type):
        result=get_ocr_result(img_code,img_type)
        return result


