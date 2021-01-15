import sys

# 1st argv: original file 1, used to check the lines with or without tags
# 2nd argv: original file 2, will operate according to the check in file 1


def cotherfile(file_r, file_w, line_set):
    with open(file_r, 'r', encoding='utf-8') as sourceFile2, open(file_w, 'w', encoding='utf-8') as targetFile2:
        print(' open file', file_r)
        line_index = 0
        for line in sourceFile2:
            if line_index in line_set:
                targetFile2.write(line)
                # targetFile2.write('\n')
            line_index += 1
    sourceFile2.close()
    targetFile2.close()
    return


def main(para):
    sourceTxt1 = './' + para[1]
    targetTxt1 = './' + para[1] + '-alltags'

    line_set = {-1:''}
    with open(sourceTxt1, 'r', encoding='utf-8') as sourceFile1, open(targetTxt1, 'w', encoding='utf-8') as targetFile1:
        print(' open file', sourceTxt1)
        line_index = 0
        for line in sourceFile1:
            tokens = line.split()
            for j in reversed(range(len(tokens))):
                if tokens[j].startswith('<') and tokens[j].endswith('>'):
                    line_set[line_index] = ''
                    targetFile1.write(line)
                    # targetFile1.write('\n')
                    break
            line_index += 1
    sourceFile1.close()
    targetFile1.close()
    for file_name in para[2:]:
        file_r = './' + file_name
        file_w = './' + file_name + '-alltags'
        cotherfile(file_r, file_w, line_set)
    return

if __name__ == '__main__':
    print('argv number ', len(sys.argv))
    # 1st argv: original file 1, used to check the lines with or without tags
    # 2nd and more argv: original file 2 and more, will operate according to the check in file 1

    main(sys.argv)
