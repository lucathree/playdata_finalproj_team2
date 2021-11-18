import os
import torch
from torch import nn
import torch.nn.functional as F
from torchvision import transforms
from torch.utils.data import DataLoader
import pytorch_lightning as pl
from datasets import LaneDataset
import matplotlib.pyplot as plt
from torchvision.models.segmentation import fcn_resnet50
import numpy as np
from focal_loss import FocalLoss
import datetime
import sys
import arg_parse
import torchvision
# from src_test import arg_parse as arg


class NIA_SEGNet_module(pl.LightningModule):
    def __init__(self):
        super(NIA_SEGNet_module, self).__init__()
        # self.save_hyperparameters()
        self.fcn = fcn_resnet50(pretrained=True)
        in_channels = 2048
        inter_channels = in_channels // 4
        channels = 4
        dropout = 0.1
        self.fcn.classifier = nn.Sequential(
            nn.Conv2d(in_channels, inter_channels, 3, padding=1, bias=False),
            nn.BatchNorm2d(inter_channels),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv2d(inter_channels, channels, 1)
        )
        self.f1 = 0
        self.f1cnt = 0
        
    def forward(self, x):
        out = self.fcn(x)
        return out


    # def training_epoch_end(self,outputs):
    #     #  the function is called after every epoch is completed
    #     # calculating average loss 
    #     avg_loss = torch.stack([x['loss'] for x in outputs]).mean()
    #     # calculating correect and total predictions
    #     # total=sum([x["total"] for  x in outputs])
    #     # correct=sum([x["correct"] for  x in outputs])
    #     # logging using tensorboard logger
    #     self.logger.experiment.add_scalar("Loss/Train",
    #                                         avg_loss,
    #                                         self.current_epoch)

    #     # self.logger.experiment.add_scalar("Accuracy/Train",
    #     #                                     correct/total,
    #     #                                     self.current_epoch)
    #     epoch_dictionary={
    #         # required
    #         'loss': avg_loss}

    #     return epoch_dictionary


    def custom_histogram_adder(self):

        # iterating through all parameters
        for name,params in self.named_parameters():

            self.logger.experiment.add_histogram(name,params,self.current_epoch)

    # def training_epoch_end(self,batch,outputs):

    #     #  the function is called after every epoch is completed
    #     # calculating average loss

    #     avg_loss = torch.stack([x['loss'] for x in outputs]).mean()
    #     avg_loss2 = self.get_loss(batch)
    #     # logging histograms
    #     self.custom_histogram_adder()

    #     epoch_dictionary={

    #     # required

    #         'loss': avg_loss}



    #     return epoch_dictionary

    def training_step(self, batch, batch_idx):
        # ######################################
        # REQUIRED- run at every batch of training data
        # extracting input and output from the batch
        # x, y, _ = batch
        # # forward pass on a batch
        # pred=self.forward(x)
        # # identifying number of correct predections in a given batch
        # correct=torch.argmax(dim=1).eq(y).sum().item()
        # # identifying total number of labels in a given batch
        # total=len(y)
        # # calculating the loss
        # train_loss = F.cross_entropy(pred, y)
        # # logs- a dictionary
        # logs={"train_loss": train_loss}
        # batch_dictionary={
        #     #REQUIRED: It ie required for us to return "loss"
        #     "loss": train_loss,
        #     #optional for batch logging purposes
        #     "log": logs,
        #     # info to be used at epoch end
        #     "correct": correct,
        #     "total": total
        # }
        ######################################
        
        loss = self.get_loss(batch)
        self.log('train_loss', loss)
        return loss

        
    def get_loss(self,batch):
        x, y, _ = batch
        out = (self(x)['out'])
        ltype = "default"
        if ltype == "sqrt-frq":
            frequency_weight = torch.Tensor([0.03055164, 0.15936654, 0.60941457, 0.20066725]).to(self.device)
            loss = F.cross_entropy(out, y, weight=frequency_weight)
        elif ltype == "focal":
            fl = FocalLoss()
            loss = fl(out, y)
        else:
            loss = F.cross_entropy(out, y)
        return loss
        
    def test_step(self, batch, batch_idx):
        x, y, img_path = batch
        out = torch.sigmoid(self(x)['out'])
        confusion_mat = torch.zeros((4,4), device=self.device,dtype=torch.long)
        f1_sum = 0
        f1_cnt = 0
        # print(batch_idx)
        acc = torch.tensor(0.0,device=self.device)
        # imshow = False
        imshow = True
        if imshow:
            for i, output in enumerate(out):
                final_out = torch.argmax(output,0)
                img = x[i].cpu().permute((1,2,0)).numpy()
                # img = img[:,:,::-1]
                plt.imsave("input.png", img)
                plt.imsave("output.png", (final_out.cpu()).int(),vmin=0,vmax=3)
                plt.imsave("target.png", (y[i].cpu()).int(),vmin=0,vmax=3)
                input()
        else:
            for i, output in enumerate(out):
                final_out = torch.argmax(output,0)

                acc += torch.sum((final_out==y[i]))/(512*1024.0)

                for xx in torch.arange(4, device=self.device):
                    for yy in torch.arange(4, device=self.device):
                        confusion_mat[xx,yy] += torch.sum((final_out==xx)*(y[i]==yy))

                aa,bb,cnt = 0,0,0
                for ii in range(4):
                    if torch.sum(confusion_mat[ii,:]) !=0 and torch.sum(confusion_mat[:,ii]) != 0:
                        aa += confusion_mat[ii,ii]/torch.sum(confusion_mat[ii,:]).float()
                        bb += confusion_mat[ii,ii]/torch.sum(confusion_mat[:,ii]).float()
                        cnt += 1
                aa /= cnt
                bb /= cnt
                # self.f1 += (2*aa*bb/(aa+bb))
                # self.f1cnt += 1
                f1 = (2*aa*bb/(aa+bb)).item()
                f1_sum += f1
                f1_cnt += 1
                print(img_path, "F1 measure :", f1)

                file_output = False
                # file_output = True
                if file_output:
                    if not os.path.exists("./output/"):
                        os.mkdir("./output/")
                    img = x[i].cpu().permute((1,2,0)).numpy()
                    folder_path = "./output/"+str(batch_idx*self.batch_size + i)
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)
                    plt.imsave(folder_path+"/input.png", img)
                    plt.imsave(folder_path+"/output.png", final_out.cpu()*255/3)
                    plt.imsave(folder_path+"/target.png", y[i].cpu())
            acc /= len(out)
            return confusion_mat, f1_sum, f1_cnt

    def test_epoch_end(self,outputs):
        sum_confusion_mat = 0
        total_f1 = 0
        total_f1_cnt = 0
        for confusion_mat, f1_sum, f1_cnt in outputs:
            sum_confusion_mat += confusion_mat
            total_f1 += f1_sum
            total_f1_cnt += f1_cnt

        if total_f1_cnt > 0:
            print("total_f1_cnt",total_f1_cnt)
            print("average F1 measure", total_f1/total_f1_cnt)
            print("total confusion matrix:\n", sum_confusion_mat.cpu().numpy())

        print("total_f1_cnt",total_f1_cnt)
        print("average F1 measure", total_f1/total_f1_cnt)
        print("total confusion matrix:\n", sum_confusion_mat.cpu().numpy())

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=arg_parse.args.learning_rate)
        return optimizer

    def validation_step(self, batch, batch_idx):
        loss =  self.get_loss(batch)
        self.log_dict({'val_loss': loss})
        ########################################################################
        # x, y, _ = batch
        # y_hat = self(x)
        # correct=y_hat.argmax(dim=1).eq(y).sum().item()
        # total=len(y)
        # return {'val_loss': F.cross_entropy(y_hat, y),"correct": correct,"total": total}, loss
        ###################################################################################
        return loss

    def validation_epoch_end(self, outputs):
        sum_loss = 0
        for loss in outputs:
            sum_loss += loss



    def val_dataloader(self):
        dataset = LaneDataset(data_path='/home/ubuntu/aiml/lane_model/data/val.txt')
        train_loader = DataLoader(dataset, batch_size = self.batch_size, num_workers=28)
        return train_loader

    def test_dataloader(self):
        dataset = LaneDataset(data_path='/home/ubuntu/aiml/lane_model/data/sample.txt')
        train_loader = DataLoader(dataset, batch_size = self.batch_size, num_workers=12)
        return train_loader

    def train_dataloader(self):
        dataset = LaneDataset(data_path='/home/ubuntu/aiml/lane_model/data/train.txt')
        train_loader = DataLoader(dataset, batch_size = self.batch_size, num_workers=12,shuffle=True)
        #    DataLoader(dataset, batch_size=1, shuffle=False, sampler=None,
        #    batch_sampler=None, num_workers=0, collate_fn=None,
        #    pin_memory=False, drop_last=False, timeout=0,
        #    worker_init_fn=None)
        return train_loader
