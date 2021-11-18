import argparse

# if __name__ == '__main__':

def print_parse():
    # 1. create parser
    parser = argparse.ArgumentParser(description='This is argparse example python program.')

    # 2. add arguments to parser

    parser.add_argument(
        '--epochs', '-e',
        type=int,
        default=3,
        help='Number of epoch to train.')

    parser.add_argument(
        '--batch_size', '-b',
        type=int,
        default=1,
        help='Size of batch')

    parser.add_argument(
        '--learning_rate', '-lr',
        type=float,
        default=0.001,
        help='Learning rateD'
    )

    # 3. parse arguments
    args = parser.parse_args()

    # 4. use arguments
    print(args)
    
    print('epochs :',args.epochs)
    print('batch_size :',args.batch_size)
    print('learning_rate : ', args.learning_rate)

    return 'parse return'

def batch_size():
    return args.batch_size