import requests
import cv2
from json import *
from pprint import *
from api_key import key, secret


#attributes
def detect(filepath, attributes = "gender,age,beauty"):
    http_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
    data = {"api_key": key, "api_secret": secret, "return_landmark": "1", "return_attributes": attributes}
    files = {"image_file": open(filepath, "rb")}
    response = requests.post(http_url, data=data, files=files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    pprint(req_dict)

    return req_dict


#需要传入两张图片
def compare(filepath1, filepath2):
    http_url= 'https://api-cn.faceplusplus.com/facepp/v3/compare'
    data = {"api_key": key, "api_secret": secret}
    files = {"image_file1": open(filepath1, "rb"), "image_file2": open(filepath2, "rb")}
    response = requests.post(http_url, data = data, files= files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    pprint(req_dict)

    return req_dict

#在已有的FaceSet中找出与目标人脸最相似的一张或多张
def search(filepath, outer_id):
    http_url= 'https://api-cn.faceplusplus.com/facepp/v3/search'
    data = {"api_key": key, "api_secret": secret, "outer_id":outer_id}
    files = {"image_file": open(filepath, "rb")}
    response = requests.post(http_url, data = data, files= files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    pprint(req_dict)

    return req_dict


#融合人脸
def merge(template_filepath, merge_filepath, merge_rate=20):
    http_url = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    data = {"api_key": key, "api_secret": secret, "merge_rate": merge_rate}
    files = {"template_file": open(template_filepath, "rb"), "merge_file": open(merge_filepath, "rb")}

    response = requests.post(http_url, data=data, files=files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    pprint(req_dict)

    return req_dict
#识别场景
def detect_scence(filepath):
    http_url = 'https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject'
    data = {"api_key": key, "api_secret": secret}
    files = {"image_file": open(filepath, "rb")}

    response = requests.post(http_url, data=data, files=files)

    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    pprint(req_dict)

    return req_dict

