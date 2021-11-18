import argparse

parser = argparse.ArgumentParser(description='This is argparse example python program.')

parser.add_argument('-f')
# 2. add arguments to parser

parser.add_argument(
    '--epochs', '-e',
    type=int,
    default=1,
    help='Number of epoch to train.')

parser.add_argument(
    '--batch_size', '-b',
    type=int,
    default=1,
    help='Size of batch')

parser.add_argument(
    '--learning_rate', '-lr',
    type=float,
    default=0.1,
    help='Learning rate'
)

# 3. parse arguments
args = parser.parse_args()

# 4. use arguments
print(args)

print('epochs :',args.epochs)
print('batch_size :',args.batch_size)
print('learning_rate : ', args.learning_rate)

e = args.epochs
b = args.batch_size
lr = args.learning_rate

hyp = "e-" + str(e)+ '_' + "b-" + str(b) +'_'+ "lr-" + str(lr)

print (hyp)