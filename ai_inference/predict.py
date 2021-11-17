import os
import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from torchvision import transforms
from module import NIA_SEGNet_module
from PIL import Image
import pytorch_lightning as pl
import matplotlib.pyplot as plt

class ImgListDataset(Dataset):
    I_H = 512
    I_W = 1024
    def __init__(self, img_data_path_list):
        self.img_list = img_data_path_list.copy()
        print(self.img_list)
        self.len = len(self.img_list)

    def __getitem__(self, index):
        print('index: ', index)
        while index < self.len:
            try:
                img_path = self.img_list[index]
                print(img_path)
                img = Image.open(img_path)
                print(img)
                break
            except:
                with open("error_files.txt",'a') as errlog:
                    errlog.write(img_path+'\n')
                    index = index + 1
            
        w, h = img.size
        img_tensor = transforms.functional.to_tensor(transforms.functional.resized_crop(img, h-w//2, 0, w//2, w, (self.I_H,self.I_W)))
        target_map = np.zeros((self.I_H, self.I_W),dtype=np.int32)

        return img_tensor, torch.LongTensor(target_map), img_path

    def __len__(self):
        return self.len
    
    
class TrafficLaneInference(NIA_SEGNet_module):

    def __init__(self):
        super().__init__()
    
    def test_step(self, batch, batch_idx):
        x, y, img_path = batch
        print(img_path)
        out = torch.sigmoid(self(x)['out'])
        for i, output in enumerate(out):
            final_out = torch.argmax(output,0)
            img = x[i].cpu().permute((1,2,0)).numpy()
            plt.imsave(img_path[i].replace('upload', 'response'), (final_out.cpu()).int(),vmin=0,vmax=3)
            #plt.imsave(f"input-{i+1}.png", img)
            #plt.imsave(f"output-{i+1}.png", (final_out.cpu()).int(),vmin=0,vmax=3)
            #plt.imsave(f"target-{i+1}.png", (y[i].cpu()).int(),vmin=0,vmax=3)

    def test_epoch_end(self,outputs):
        print('end')