import sys
sys.path=[x for x in sys.path if not "python2.7" in x]

import os
import random
import numpy as np
import ujson as json
import matplotlib.pyplot as plt 
from torch.utils.data import Dataset
from PIL import Image
from torchvision import transforms
import torch
# import sys
# if '/opt/ros/kinetic/lib/python2.7/dist-packages' in sys.path:
#     sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

class LaneDataset(Dataset):
    I_H = 512
    I_W = 1024
    def __init__(self, data_path):
        if not os.path.exists(data_path):
            pths = ['/home/ubuntu/aiml/lane_model/']
            if not os.path.exists("data"):
                os.mkdir("data")
            with open("data/train.txt","w") as train, open("data/val.txt","w") as val, open("data/test.txt","w") as test:
                for pth in pths: # data/.txt에 모델 과정별로 입력될 사진자료 디렉토리 주소 입력
                    for i in range(1,51): # 1~50 까지 만들어진 폴더를 정해진 규칙에 따라 txt파일에 써줌
                        if i % 10 == 1:
                            val.write(pth+str(i)+"\n")
                        elif i % 10 == 2:
                            test.write(pth+str(i)+"\n")
                        else:
                            train.write(pth+str(i)+"\n")

        with open(data_path) as txt:
            lines = txt.readlines()  # .txt파일 내용 읽어오기

        self.img_list_1 = [] # .txt 경로를 따라가서 이미지 파일리스트를 저장할 리스트 변수 생성.
        self.img_list = []
        for line in lines:
            self.img_list_1 += [line.strip()+f for f in os.listdir(line.strip()) if ".jpg" in f or '.png' in f]
 ###########################    사진수량        ###########################################
        for i in range(50) :
            index = random.randrange(0, len(self.img_list_1)-1)
            self.img_list += [self.img_list_1[index]] # 대괄호로 안감싸주면  ㅂ,ㅈ,ㄷㄱ,ㅅ,ㅂ, 이렇게 저장됨
#       self.train_list=[]
#       for i in range(3000) :훈련 데이터 n 개 선택
#           self.train_list += self.img_list[random.randrange(0, len(simg_list))] 랜덤으로
#        

#           len(listimg)       
        # print([f for f in self.img_list if not os.path.exists(f.replace('.jpg','.json').replace('.png','.json'))])
        self.len = len(self.img_list)
        self.data_path = data_path

    def __getitem__(self, index): # 입력된 index에 해당하는 이미지를 출력
        while True:
            img_path = self.img_list[index]
            try:
                img = Image.open(img_path)
                break
            except:
                with open("error_files.txt",'a') as errlog:
                    errlog.write(img_path+'\n')
                    index = index + 1
            
        w, h = img.size
        label_path = img_path.replace("image","json").replace('.jpg','.json').replace('.png','.json')
        with open(label_path) as json_file:
            json_data = json.load(json_file)
        img_tensor = transforms.functional.to_tensor(transforms.functional.resized_crop(img, h-w//2, 0, w//2, w, (self.I_H,self.I_W)))
        target_map = self.make_gt_map(json_data, w, h)

        return img_tensor, torch.LongTensor(target_map), img_path

    def __len__(self):
        return self.len

    def make_gt_map(self, json_data, original_w, original_h):
        target_map = np.zeros((self.I_H, self.I_W),dtype=np.int32)
        annotation = json_data["annotations"]
        y_offset = original_h - original_w // 2
        for item in annotation:
            obj_class = item["class"]
            if obj_class == "traffic_lane":
                pos = item["data"]
                poly_points = np.array([([pt["x"]*self.I_W/original_w, (pt["y"] - y_offset)*self.I_H/(original_h-y_offset)]) for pt in pos]).astype(np.int32)
                cv2.polylines(target_map, [poly_points], False, 1,10)
            if obj_class == "stop_line":
                pos = item["data"]
                poly_points = np.array([([pt["x"]*self.I_W/original_w, (pt["y"] - y_offset)*self.I_H/(original_h-y_offset)]) for pt in pos]).astype(np.int32)
                cv2.polylines(target_map, [poly_points], False, 2,10)
            if obj_class == "crosswalk":
                pos = item["data"]
                poly_points = np.array([([pt["x"]*self.I_W/original_w, (pt["y"] - y_offset)*self.I_H/(original_h-y_offset)]) for pt in pos]).astype(np.int32)
                if len(poly_points) == 0:
                    continue
                cv2.fillPoly(target_map, [poly_points], 3)
        return target_map
        


if __name__ == "__main__":
    ld = LaneDataset(data_path='data/val.txt')
    # ss = torch.zeros(4)
    # cnt = 0
    #
    for i,(img, target,path) in enumerate(ld):
        print(i)
        plt.imshow(img.permute((1,2,0)))
        plt.savefig("a.png")
        plt.imshow(target,vmax =3)
        plt.savefig("b.png")
        input()