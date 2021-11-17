from module import NIA_SEGNet_module
import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

# module.py 에서 NIA_SEGNet_module() 클래스를 모델로 불러옴
model = NIA_SEGNet_module()

# 모듈에서 self.batch_size로 사용되는 변수를 4로 설정 
model.batch_size = 4

# print(model.fcn)
# print(flush=True)

# 파이토치 코드를 간단하게 만들어주는 파이토치 라이트닝의 트레이너 객체 생성
# gpus : 사용할 gpu 설정, [0] 번째 gpu 사용

trainer = pl.Trainer(gpus=[0],prepare_data_per_node=True, distributed_backend="ddp", callbacks=[EarlyStopping(monitor='val_loss',patience=2)])
trainer.fit(model)
