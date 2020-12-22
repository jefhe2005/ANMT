import random
import datetime
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords


def dc_load(dc, word_pair_list):
    with open(dc, 'r', encoding='utf-8') as dc_file:
        for line in dc_file:
            tokens = line.split()
            # only load the lines with 2 and different tokens
            if len(tokens) == 2 and tokens[0] != tokens[1]:
                word_pair_list.append([tokens[0], tokens[1]])
    return


def stopwords_load(stoplib, word_list):
    with open(stoplib, 'r', encoding='utf-8') as dc_file:
        for line in dc_file:
            tokens = line.split()
            # only load the lines with 2 and different tokens
            if len(tokens) == 1:
                word_list.append(tokens[0])
    return


# read file and append a list of all lines
def file_to_list(src_file, total_list):
    with open(src_file, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            total_list.append(line)
    return


# check and return
# cho_tokens = [-1, -1, '', -1, ''] , line number, position, src token, position, correct tgt token
def check_src_tgt_token(src_total_list, tgt_total_list, dc_list, line_number, stoplist):
    # get the corresponding line pair at the source and target, and take tokens to a list
    src_line = src_total_list[line_number]
    tgt_line = tgt_total_list[line_number]
    src_tokens = src_line.split()
    tagged = nltk.pos_tag(src_tokens)
    tgt_tokens = tgt_line.split()
    cho_tokens = [-1, -1, '', -1, '']
    for i in range(len(src_tokens)):
        # use src_tokens[i] to look up the dictionary
        # TODO need to be unique both at the src/tgt sentences; change to low case before processing
        if src_tokens.count(src_tokens[i]) != 1:
            continue
        if src_tokens[i] in stoplist:  # skip stopwords
            continue
        # skip not content words
        if tagged[i][1].find('N') != 0 and tagged[i][1].find('V') != 0 and tagged[i][1].find('J') != 0:
            continue
        for word_pair in dc_list:
            if src_tokens[i].lower() == word_pair[0].lower():  # src token found in dictionary; check the tgt
                try:
                    cho_tokens[3] = tgt_tokens.index(word_pair[1])
                except:
                    cho_tokens[3] = -1
            if cho_tokens[3] >= 0:  # success in tgt sentence
                cho_tokens[0] = line_number
                cho_tokens[1] = i
                cho_tokens[2] = src_tokens[i]
                cho_tokens[4] = tgt_tokens[cho_tokens[3]]
                return cho_tokens
    return cho_tokens


# Calculate the total number of lines in a text file
def cal_lines(source_txt):
    number_lines = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            number_lines += 1
    source_file.close()
    return number_lines


# NOT used in Choose
# change the line numbers in the 'token_list" to be random
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
def random_token(source_txt, token_list, total_process_lines, stoplist_tgt):
    line_number = token_list[0][0]
    # token = token_list[0][1]
    i = 0
    j = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # tokens = line.split()
                    tokens = word_tokenize(line)
                    tagged = nltk.pos_tag(tokens)
                    # print(tokens)
                    length = len(tokens)
                    n = random.randint(0, length - 1)
                    number_try = 0
                    len_c = len(tokens[n]) < 2 or len(tokens[n]) > 10
                    CW = tagged[n][1].find('N') == 0 or tagged[n][1].find('V') == 0 or tagged[n][1].find('J') == 0
                    while tokens[n] in stoplist_tgt or (not CW) or len_c:
                        # skip stopwords, not content words, too short/long
                        n = random.randint(0, length - 1)
                        len_c = len(tokens[n]) < 2 or len(tokens[n]) > 10
                        CW = tagged[n][1].find('N') == 0 or tagged[n][1].find('V') == 0 or tagged[n][1].find('J') == 0
                        print('token not good, try to find another')
                        number_try += 1
                        if number_try > 6:
                            break
                    token_list[j] = [line_number, tokens[n]]
                    j += 1
                    if j < total_process_lines:
                        line_number = token_list[j][0]
                    # print(line_number)
                    # print(token_list)
            i += 1
    source_file.close()
    return


# Insert a tag with its token into a line of text
def insert_cho_tag(line, tag, token, position):
    if tag == 'CHOOSE':
        open_copy = '<choose>'
        close_copy = '</choose>'
        list_token = line.split()
        list_token.append('\n')
        # replace the token at 'position' to 'token' and return
        list_token.pop(position)
        list_token.insert(position, open_copy + ' ' + token + ' ' + close_copy)
        return ' '.join(list_token)
    """
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
    """


def cho_process_src(read_file, write_file, src_token_list, tgt_token_list, ran_token_list, total_process_lines):
    line_number = src_token_list[0][0]
    src_token = src_token_list[0][2]
    tgt_token = tgt_token_list[0][2]
    ran_token = ran_token_list[0][1]
    i = 0
    j = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # insert choose tag with token to the specific line
                    if random.randint(0, 2) == 0:
                        token = src_token + ' ' + '<TO>' + ' ' + ran_token + ' ' + '<OR>' + ' ' + tgt_token
                    else:
                        token = src_token + ' ' + '<TO>' + ' ' + tgt_token + ' ' + '<OR>' + ' ' + ran_token
                    line = insert_cho_tag(line, 'CHOOSE', token, src_token_list[j][1])
                    j += 1
                    if j < total_process_lines:
                        line_number = src_token_list[j][0]
                        src_token = src_token_list[j][2]
                        tgt_token = tgt_token_list[j][2]
                        ran_token = ran_token_list[j][1]
            target_file.write(line)
            # target_file.write('\n')
            i += 1
    source_file.close()
    target_file.close()
    return


def cho_process_tgt(read_file, write_file, token_list, total_process_lines):
    line_number = token_list[0][0]
    token = token_list[0][2]
    i = 0
    j = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # insert copy tag with token to the specific line
                    line = insert_cho_tag(line, 'CHOOSE', token, token_list[j][1])
                    j += 1
                    if j < total_process_lines:
                        line_number = token_list[j][0]
                        token = token_list[j][2]
            target_file.write(line)
            # target_file.write('\n')
            i += 1
    source_file.close()
    target_file.close()
    return


def main():
    # parameters: ratio, filenames
    # percentage of lines for processing
    ratio = 0.8

    # path for dictionary
    dc = './en-zh.txt'

    # prepare the stoplist
    stoplist = stopwords.words('english')
    stoplib = './cn_stopwords.txt'
    stoplist_zh = ['']
    stopwords_load(stoplib, stoplist_zh)
    del stoplist_zh[0]
    print(stoplist_zh)
    # path for source text (before processing)
    source_txt_rd = './test.en-og'
    # path for source text(after processing)
    source_txt_wr = './test.en80cho-cw'

    # path for target text(before processing)
    target_txt_rd = './test-jieba.zh'
    # path for target text(after processing)
    target_txt_wr = './test.zh80cho-cw'

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
    dc_list = [['', '']]
    # load the dictionary to 'word_pair_list'
    dc_load(dc, dc_list)

    # initial toke_list(xxx, ccc, www)
    src_token_list = [[-1, -1, '']]  # line number, token position, token
    tgt_token_list = [[-1, -1, '']]  # line number, token position, token
    ran_token_list = [[-1, '']]  # line number, token
    for i in range(total_lines - 1):
        src_token_list.append([-1, -1, ''])
        tgt_token_list.append([-1, -1, ''])
    for i in range(total_process_lines - 1):
        ran_token_list.append([-1, ''])
    # print(len(src_token_list))

    # generate the ran_token_list (www-wrong)
    # generate the token list for random tgt token yyy; copy, change the line numbers, replace; no merging
    # first, generate the random line numbers
    random_line(total_lines, total_process_lines, ran_token_list)
    # second, sort the token list
    ran_token_list.sort(key=lambda x: x[0])
    # finally, replace the source token in the list with random tgt tokens from the text file
    random_token(target_txt_rd, ran_token_list, total_process_lines, stoplist_zh)
    print('line number with random target tokens(www)')
    print(ran_token_list)

    # generate the src token(xxx) and its corresponding tgt token(ccc -correct) with the help of dictionary

    # read src and tgt files to line lists
    src_total_list = ['']
    tgt_total_list = ['']
    file_to_list(source_txt_rd, src_total_list)
    file_to_list(target_txt_rd, tgt_total_list)
    src_total_list.pop(0)
    tgt_total_list.pop(0)
    if len(src_total_list) != len(tgt_total_list):
        print('read files error: source != target lines')
        return
    if len(src_total_list) != total_lines:
        print('read files error: source != total lines')
        return
    # i = 0  # counter for correct tokens generated
    # cho_tokens = [-1, -1, '', -1, '']  # line number, position, src token, position, correct tgt token
    # remain_process_lines = total_process_lines
    for i in range(total_lines):
        if i % 3000 == 0:
            print(datetime.datetime.now(), 'check pos, line:', i, 'length= ', len(src_total_list[i]))
        if len(src_total_list[i]) > 4096:
            print('skip long sentence > 4096 char; line :', i)
            continue
        # print('line number:', i)
        cho_tokens = check_src_tgt_token(src_total_list, tgt_total_list, dc_list, i, stoplist)
        src_token_list[i][0] = cho_tokens[0]
        src_token_list[i][1] = cho_tokens[1]
        src_token_list[i][2] = cho_tokens[2]
        tgt_token_list[i][0] = cho_tokens[0]
        tgt_token_list[i][1] = cho_tokens[3]
        tgt_token_list[i][2] = cho_tokens[4]
    # delete the no-match record in the token list
    for i in reversed(range(total_lines)):
        if i % 20000 == 0:
            print(datetime.datetime.now(), 'delete no-match records, line:', i)
        if src_token_list[i][1] == -1 or tgt_token_list[i][1] == -1:
            # src_noun_list.pop(i)
            del src_token_list[i]
            del tgt_token_list[i]

    # shuffle the list and get the first "n" of the token list
    list_length = len(src_token_list)
    if list_length > total_process_lines:
        print('noun list larger than ratio')
        print(list_length)
        random.shuffle(src_token_list)
        for i in range(list_length - total_process_lines):
            line_number = src_token_list[list_length - 1 - i][0]
            src_token_list.pop(list_length - 1 - i)
            for j in range(len(tgt_token_list)):
                if tgt_token_list[j][0] == line_number:
                    del tgt_token_list[j]
                    break
    # sort the remaining token list using line number
    print(datetime.datetime.now(), 'sorting src list')
    src_token_list.sort(key=lambda x: x[0])
    print(datetime.datetime.now(), 'sorting src list')
    tgt_token_list.sort(key=lambda x: x[0])
    
    # change the line number of random token list to be same as the src/tgt token list

    for i in range(len(src_token_list)):
        ran_token_list[i][0] = src_token_list[i][0]
    print('before inserting : line number with real random tokens www')
    print(ran_token_list)

    # process ( insert tags) the source and target text file
    # process the source text
    cho_process_src(source_txt_rd, source_txt_wr, src_token_list, tgt_token_list, ran_token_list, len(src_token_list))
    # process the target text if the file path is not empty
    if len(target_txt_rd) > 3:
        cho_process_tgt(target_txt_rd, target_txt_wr, tgt_token_list, len(src_token_list))
    print('finish processing!')
    return


if __name__ == '__main__':
    main()
