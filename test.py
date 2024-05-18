from utils.repairer import auto_correct

if __name__ == '__main__':
    inputData = {
        'height': 50,
        'weight': 150
    }
    rs = auto_correct('gender', None, inputData)
    print('Result is ', rs)