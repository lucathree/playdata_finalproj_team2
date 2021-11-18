import logging
from torch.utils import tensorboard
from pytorch_lightning.loggers import TensorBoardLogger
import arg_parse
import datetime
import platform
import psutil
# import cpuinfo
from module import NIA_SEGNet_module
import pytorch_lightning as pl
import torch
import random
import time
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import shutil
###############################################################################################################
from torch.utils.tensorboard import SummaryWriter
import numpy as np

#텐서보드 로거 객체 생성
hyp_val=arg_parse.hyp
logger  = TensorBoardLogger('tb_logs', name='NIA_SEGNet_module'+hyp_val, default_hp_metric=False)

#tensor board
writer = SummaryWriter('/home/ubuntu/aiml/lane_model/src_test/lightning_logs')
# for n_iter in range(500)
#     writer.add_scalar('Loss/train', np.random.random(), n_iter)
#     writer.add_scalar('Loss/test', np.random.random(), n_iter)
#     writer.add_scalar('Accuracy/train', np.random.random(), n_iter)
#     writer.add_scalar('Accuracy/test', np.random.random(), n_iter)

writer.close()
###############################################################################################################
param = arg_parse.args








###############################################################################################################


torch.manual_seed(777)
random.seed(777)

model = NIA_SEGNet_module()

model.batch_size =param.batch_size

# print(model.fcn)
# print(flush=True)

trainer = pl.Trainer(gpus=[0],prepare_data_per_node=True, distributed_backend="ddp", callbacks=[EarlyStopping(monitor='val_loss', patience=2)],  max_epochs=param.epochs, logger=logger)

# lr_finder = trainer.tuner.lr_find(model) # Run learning rate finder
# fig = lr_finder.plot(suggest=True) # Plot
# fig.show()
# model.hparams.lr = lr_finder.suggestion()
trainer.fit(model)

