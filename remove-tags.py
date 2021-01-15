import sys

# remove tags before bleu
# 1st argv: original file, such as test.zh
# 2nd argv: number of checkpoints from 55k, (4 for 55~70k, 10 for 55~100k)


def main(para):
    if para[2] == 'infer':
        j = int(para[3])
    if para[2] == 'og':
        j = 1
    for i in range(j):
        if para[2] == 'infer':
            sourceTxt = './' + para[1] + '.hyp_model_step_' + str(55000 + i * 5000)
            targetTxt = './' + para[1] + '-r.hyp_model_step_' + str(55000 + i * 5000)
        if para[2] == 'og':
            sourceTxt = './' + para[1]
            targetTxt = './' + para[1] + '-rm'
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
        print('remove tags from file : ', sourceTxt)
        print('write to file : ', targetTxt)
        print('total tags removed:', tag_removed)
    return


if __name__ == '__main__':
    print('argv number ', len(sys.argv))
    # 1st argv: original file, such as test.zh， test.de，news-test.en(for zh-en)
    # 2nd argv: 'infer', to add "hyper" to the file name, 'og': direct use the file name
    # 3nd argv: number of checkpoints from 55k, (4 for 55~70k, 10 for 55~100k)
    main(sys.argv)
