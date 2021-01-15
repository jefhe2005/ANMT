import random


# Calculate the total number of lines in a text file
def cal_lines(source_txt):
    number_lines = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            number_lines += 1
    source_file.close()
    return number_lines


def random_line(total_lines, total_process_lines, token_list):
    for i in range(total_process_lines):
        line_number = random.randint(0, total_lines - 1)
        # deduplicate if line number is already in the list
        dup = True
        while dup:
            for j in range(total_process_lines):
                if token_list[j][0] == line_number:
                    dup = True
                    line_number = random.randint(0, total_lines - 1)
                    print('duplicate random line_number is found, try another random line')
                    break
                dup = False
        token_list[i][0] = line_number
    return


# Get random tokens in specific lines in a text file
def random_token(source_txt, token_list, total_process_lines):
    line_number = token_list[0][0]
    # token = token_list[0][1]
    i = 0
    j = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    tokens = line.split()
                    # print(tokens)
                    length = len(tokens)
                    token_number = random.randint(0, length - 1)
                    """ try to avoid too short tokens, but probably not necessary
                    number_try = 0
                    while len(token) < 3:
                        token_number = random.randint(0, length - 1)
                        print('too short token, try to find another')
                        number_try +=1
                        if number_try > 4:
                            break
                    """
                    token_list[j] = [line_number, tokens[token_number]]
                    j += 1
                    if j < total_process_lines:
                        line_number = token_list[j][0]
                    # print(line_number)
                    # print(token_list)
            i += 1
    source_file.close()
    return


# Insert a tag with its token into a line of text
def insert_tag(line, tag, token):
    if tag == 'COPY':
        open_copy = '<copy>'
        close_copy = '</copy>'
        list_token = line.split()
        list_token.append('\n')
        length = len(list_token)
        insert_pos = random.randint(0, length - 1)
        list_token.insert(insert_pos, open_copy + ' ' + token + ' ' + close_copy)
        return ' '.join(list_token)
    if tag == 'SP':
        open_copy = '<specify>'
        close_copy = '</specify>'
        list_token = line.split()
        list_token.append('\n')
        length = len(list_token)
        insert_pos = random.randint(0, length - 1)
        list_token.insert(insert_pos, open_copy + ' ' + token + ' ' + close_copy)
        return ' '.join(list_token)


def sp_process_src(read_file, write_file, token_list, tgt_token_list, total_process_lines):
    line_number = token_list[0][0]
    src_token = token_list[0][1]
    tgt_token = tgt_token_list[0][1]
    i = 0
    j = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # insert copy tag with token to the specific line
                    token = src_token + ' ' + '<TO>' + ' ' + tgt_token
                    line = insert_tag(line, 'SP', token)
                    j += 1
                    if j < total_process_lines:
                        line_number = token_list[j][0]
                        src_token = token_list[j][1]
                        tgt_token = tgt_token_list[j][1]
            target_file.write(line)
            # target_file.write('\n')
            i += 1
    source_file.close()
    target_file.close()
    return


def sp_process_tgt(read_file, write_file, token_list, total_process_lines):
    line_number = token_list[0][0]
    token = token_list[0][1]
    i = 0
    j = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # insert copy tag with token to the specific line
                    line = insert_tag(line, 'SP', token)
                    j += 1
                    if j < total_process_lines:
                        line_number = token_list[j][0]
                        token = token_list[j][1]
            target_file.write(line)
            # target_file.write('\n')
            i += 1
    source_file.close()
    target_file.close()
    return


def main():
    # parameters: ratio, filenames
    # percentage of lines for processing
    ratio = 0.01

    # path for source text (before processing)
    source_txt_rd = './UNv1.0.testset.en'
    # path for source text(after processing)
    source_txt_wr = './UNv1.0.testset.ensp'

    # path for target text(before processing)
    target_txt_rd = './UNv1.0.testset.zh'
    # path for target text(after processing)
    target_txt_wr = './UNv1.0.testset.zhsp'

    # compare the number of lines in source and target, if not same, quit
    total_lines = cal_lines(source_txt_rd)
    if len(target_txt_rd) > 3 and total_lines != cal_lines(target_txt_rd):
        print('source and target text have different numbers of lines')
        return
    print('total lines in file = ')
    print(total_lines)
    # calculate the TotalProcessLines
    total_process_lines = int(ratio * total_lines)
    print('total processing lines = ')
    print(total_process_lines)

    # initial toke_list(only source token xxx)
    src_token_list = [[-1, '']]
    tgt_token_list = [[-1, '']]
    for i in range(total_process_lines - 1):
        src_token_list.append([-1, ''])
        tgt_token_list.append([-1, ''])
    # print(len(src_token_list))
    
    # generate the token list but with placehold
    random_line(total_lines, total_process_lines, src_token_list)

    # sort the token list
    src_token_list.sort(key=lambda x: x[0])
    print('line number after sorting')
    print(src_token_list)

    # replace the placehold token in the list with random tokens from the text file
    random_token(source_txt_rd, src_token_list, total_process_lines)
    print('line number with real source tokens')
    print(src_token_list)

    # generate the token list for random tgt token yyy; copy, change the line numbers, replace; no merging
    # tgt_tokens = src_token_list
    random_line(total_lines, total_process_lines, tgt_token_list)
    # sort the token list
    tgt_token_list.sort(key=lambda x: x[0])
    # replace the source token in the list with random tgt tokens from the text file
    random_token(target_txt_rd, tgt_token_list, total_process_lines)
    print('line number with real target tokens')
    print(tgt_token_list)

    # change the line number in the source token list to be random
    random_line(total_lines, total_process_lines, src_token_list)
    # sort again with the new line number
    src_token_list.sort(key=lambda x: x[0])
    print('before inserting : line number with real source tokens')
    print(src_token_list)
    
    # change the line number of tgt token list to be same as the source token list
    for i in range(total_process_lines):
        tgt_token_list[i][0] = src_token_list[i][0]
    print('before inserting : line number with real tgt tokens')
    print(tgt_token_list)
    # process ( insert tags) the source and target text file
    # process the source text
    sp_process_src(source_txt_rd, source_txt_wr, src_token_list, tgt_token_list, total_process_lines)
    # process the target text if the file path is not empty
    if len(target_txt_rd) > 3:
        sp_process_tgt(target_txt_rd, target_txt_wr, tgt_token_list, total_process_lines)
    print('finish processing!')
    return


if __name__ == '__main__':
    main()
