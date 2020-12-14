
# sourceTxt = './UNv1.0.testset.zh.hyp_model_step_90000'
# targetTxt = './UNv1.0.testset.zh.hyp_model_step_90000'
for i in range(10):
    sourceTxt = './UNv1.0.testset.zh.hyp_model_step_' + str(55000 + i * 5000)
    targetTxt = './UNv1.0.testset.zh-r.hyp_model_step_' + str(55000 + i * 5000)
    tag_removed = 0
    with open(sourceTxt, 'r', encoding='utf-8') as sourceFile, open(targetTxt, 'w', encoding='utf-8') as targetFile:
        print(' open file', sourceTxt)
        for line in sourceFile:
            tokens = line.split()
            for j in reversed(range(len(tokens))):
                if tokens[j].startswith('<') and tokens[j].endswith('>'):
                    del tokens[j]
                    tag_removed += 1
                    # print('one tag removed!')
            output = ' '.join(tokens)
            targetFile.write(output)
            targetFile.write('\n')
    sourceFile.close()
    targetFile.close()
    print('finish--remove tags:', sourceTxt)
    print('tag removed:', tag_removed)
