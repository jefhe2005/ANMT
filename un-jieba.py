import jieba
import jieba.analyse

sourceTxt = './test.zh'

targetTxt = './test-jieba.zh'


with open(sourceTxt, 'r', encoding = 'utf-8') as sourceFile, open(targetTxt, 'a+', encoding = 'utf-8') as targetFile:
    for line in sourceFile:
        seg = jieba.cut(line.strip(), cut_all = False)
        output = ' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
    print('finish jieba--test')
    
sourceTxt = './valid.zh'

targetTxt = './valid-jieba.zh'


with open(sourceTxt, 'r', encoding = 'utf-8') as sourceFile, open(targetTxt, 'a+', encoding = 'utf-8') as targetFile:
    for line in sourceFile:
        seg = jieba.cut(line.strip(), cut_all = False)
        output = ' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
    print('finish jieba--valid')