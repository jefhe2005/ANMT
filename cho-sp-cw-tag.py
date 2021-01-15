import random
import datetime
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
import sys
import multiprocessing


def dc_load(dc, word_pair_list):
    with open(dc, 'r', encoding='utf-8') as dc_file:
        for line in dc_file:
            tokens = line.split()
            # only load the lines with 2 and different tokens
            if len(tokens) == 2 and tokens[0] != tokens[1]:
                word_pair_list[tokens[0]] = tokens[1]
    # print(word_pair_list)
    return


# read file and append a list of all lines
def file_to_list(src_file, total_list):
    with open(src_file, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            total_list.append(line)
    return


# check and return
# cho_tokens = [-1, -1, '', -1, ''] , line number, position, src token, position, correct tgt token
def check_src_tgt_token(src_total_list, tgt_total_list, dc_list, stoplist, line_number):
    # get the corresponding line pair at the source and target, and take tokens to a list
    src_line = src_total_list[line_number]
    tgt_line = tgt_total_list[line_number]
    src_tokens = src_line.split()
    tgt_tokens = tgt_line.split()
    # for zh-en, use english text (tgt) to choose the cw
    tagged = nltk.pos_tag(tgt_line)
    cho_tokens = [-1, -1, '', -1, '']
    for i in range(len(src_tokens)):
        # use src_tokens[i] to look up the dictionary
        # TODO need to be unique both at the src/tgt sentences; change to low case before processing
        if src_tokens[i] in stoplist:
            continue
        if src_tokens.count(src_tokens[i]) != 1:
            continue
        if src_tokens[i].lower() in dc_list:
            # print('in dict:', dc_list.get(src_tokens[i].lower()))
            values = dc_list.get(src_tokens[i].lower())
            if values in tgt_tokens:
                posi = tgt_tokens.index(values)
                if tagged[posi][1].find('N') == 0 or tagged[posi][1].find('V') == 0 or tagged[posi][1].find('J') == 0:
                    cho_tokens[0] = line_number
                    cho_tokens[1] = i
                    cho_tokens[2] = src_tokens[i]
                    cho_tokens[3] = tgt_tokens.index(values)
                    cho_tokens[4] = values
                    # print('match a token pair! tgt token = ', values)
                    return cho_tokens
    return cho_tokens


# Calculate the total number of lines in a text file
def cal_lines(source_txt):
    number_lines = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            if number_lines % 1000000 == 0:
                print(datetime.datetime.now(), 'cal line numbers ', number_lines)
            number_lines += 1
    source_file.close()
    return number_lines


# NOT used in Choose
# change the line numbers in the 'token_list" to be random
def random_line(total_lines, total_process_lines, token_list):
    lott = [x for x in range(total_lines)]
    print('lott size = ', len(lott))
    random.shuffle(lott)
    for i in range(total_process_lines):
        token_list[i][0] = lott[i]
        if i % 1000000 == 0:
            print('random line no: ', i, ' = ', lott[i])
    return

# NOT used in Choose
# Get random tokens in specific lines in a text file
def random_token(source_txt, token_list, total_process_lines):
    line_number = token_list[0][0]
    # token = token_list[0][1]
    i = 0
    j = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            if i % 1000000 == 0:
                print('random tokens = ', i)
            if j < total_process_lines:
                if i == line_number:
                    # tokens = line.split()
                    token_number = 0
                    tokens = word_tokenize(line)
                    for token in tokens:
                        if len(token) < 2 or len(token) > 10:
                            if len(tokens) > 1:
                                del token
                    # print(tokens)
                    length = len(tokens)
                    if length > 1:
                        token_number = random.randint(0, length - 1)
                    if length == 1:
                        token_number = 0
                    """ try to avoid too short tokens, but probably not necessary
                    number_try = 0
                    while len(token) < 3:
                        token_number = random.randint(0, length - 1)
                        print('too short token, try to find another')
                        number_try +=1
                        if number_try > 4:
                            break
                    """
                    if token_number >= len(tokens):
                        print('token number = ', token_number, ' length = ', len(tokens))
                    if len(tokens) == 0:
                        print('empty lines in random')
                        token_list[j] = [line_number, ' ']
                    else:
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


def cho_process_src(tag, read_file, write_file, src_token_list, tgt_token_list, ran_token_list, total_process_lines):
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
                    if tag == 'cho':
                        # insert choose tag with token to the specific line
                        if random.randint(0, 2) == 0:
                            token = src_token + ' ' + '<TO>' + ' ' + ran_token + ' ' + '<OR>' + ' ' + tgt_token
                        else:
                            token = src_token + ' ' + '<TO>' + ' ' + tgt_token + ' ' + '<OR>' + ' ' + ran_token
                    if tag == 'sp':
                        token = src_token + ' ' + '<TO>' + ' ' + tgt_token
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


def main(para):
    # parameters: ratio, filenames
    # percentage of lines for processing
    print(datetime.datetime.now(), '---start main...')
    ratio = int(para[3]) / 100

    # path for dictionary
    dc = './' + para[5] + '.txt'

    # prepare the stoplist
    stoplist = stopwords.words('english')

    # path for source text (before processing)
    source_txt_rd = './' + para[1]
    # path for source text(after processing)
    source_txt_wr = source_txt_rd + str(int(ratio * 100)) + para[4] + '-CW-' + para[5]

    # path for target text(before processing)
    target_txt_rd = './' + para[2]
    # path for target text(after processing)
    target_txt_wr = target_txt_rd + str(int(ratio * 100)) + para[4] + '-CW-' + para[5]

    # compare the number of lines in source and target, if not same, quit
    total_lines = cal_lines(source_txt_rd)
    tgt_lines = cal_lines(target_txt_rd)
    if len(target_txt_rd) > 3 and total_lines != tgt_lines:
        print('source and target text have different numbers of lines')
        print('src: ', total_lines, ' tgt: ', tgt_lines)
        return
    print('total lines in file = ')
    print(total_lines)
    # calculate the TotalProcessLines
    total_process_lines = int(ratio * total_lines)
    print('total processing lines = ')
    print(total_process_lines)
    dc_list = {'': ''}
    # load the dictionary to 'word_pair_list'
    dc_load(dc, dc_list)

    # initial toke_list(xxx, ccc, www)
    src_token_list = [[-1, -1, '']]  # line number, token position, token
    tgt_token_list = [[-1, -1, '']]  # line number, token position, token
    ran_token_list = [[-1, '']]  # line number, token
    for i in range(total_lines - 1):
        if i % 5000000 == 0:
            print('appending src ad tgt:', i)
        src_token_list.append([-1, -1, ''])
        tgt_token_list.append([-1, -1, ''])
    for i in range(total_process_lines - 1):
        if i % 1000000 == 0:
            print('appending randoms:', i)
        ran_token_list.append([-1, ''])
    # print(len(src_token_list))

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
        if i % 1000000 == 0:
            print(datetime.datetime.now(), 'choose tokens, line:', i, 'length= ', len(src_total_list[i]))
        if len(src_total_list[i]) > 4096:
            print('skip long sentence > 4096 char; line :', i)
            continue
        # print('line number:', i)
        cho_tokens = check_src_tgt_token(src_total_list, tgt_total_list, dc_list, stoplist, i)
        src_token_list[i][0] = cho_tokens[0]
        src_token_list[i][1] = cho_tokens[1]
        src_token_list[i][2] = cho_tokens[2]
        tgt_token_list[i][0] = cho_tokens[0]
        tgt_token_list[i][1] = cho_tokens[3]
        tgt_token_list[i][2] = cho_tokens[4]
    # delete the no-match record in the token list
    # be faster using sort and cut
    print(datetime.datetime.now(), 'sorting src list and cut the useless')
    src_token_list.sort(key=lambda x: x[1], reverse=True)
    cut_pos = 0
    for i in range(total_lines):
        if src_token_list[i][1] == -1:
            cut_pos = i
            break
    print('cut pos = ', cut_pos)
    del src_token_list[cut_pos:]
    print('remain src list', len(src_token_list))

    print(datetime.datetime.now(), 'sorting tgt list and cut the useless')
    tgt_token_list.sort(key=lambda x: x[1], reverse=True)
    cut_pos = 0
    for i in range(total_lines):
        if tgt_token_list[i][1] == -1:
            cut_pos = i
            break
    print('cut pos = ', cut_pos)
    del tgt_token_list[cut_pos:]
    print('remain tgt list', len(tgt_token_list))

    # for i in reversed(range(total_lines)):
      #  if i % 500000 == 0:
       #     print(datetime.datetime.now(), 'delete no-match records, line:', i)
        # if src_token_list[i][1] == -1 or tgt_token_list[i][1] == -1:
            # src_noun_list.pop(i)
          #  del src_token_list[i]
           # del tgt_token_list[i]

    # shuffle the list and get the first "n" of the token list
    list_length = len(src_token_list)
    if list_length > total_process_lines:
        print('list larger than ratio')
        print(list_length)
        random.shuffle(src_token_list)
        # todo : can be faster, sort and cut
        #create a dictionary for tgt: key= line number, value = index;
        # assume no duplicate line numbers in the list (only one tag allowed for one line)
        tgt_dc = {-1: -1}
        for j in range(len(tgt_token_list)):
            tgt_dc[tgt_token_list[j][0]] = j

        for i in range(list_length - total_process_lines):
            line_number = src_token_list[list_length - 1 - i][0]
            if i % 1000000 == 0:
                print('trim the list, now: ', i)
            if line_number in tgt_dc:
                # print('in dict:', dc_list.get(src_tokens[i].lower()))
                tgt_index = tgt_dc.get(line_number)
                tgt_token_list[tgt_index][0] = -1  # change that line number to '-1'
            # src_token_list.pop(list_length - 1 - i)
            # del src_token_list[list_length - 1 - i]
            # for j in range(len(tgt_token_list)):
              #  if tgt_token_list[j][0] == line_number:
               #     del tgt_token_list[j]
                #    break
        del src_token_list[total_process_lines:]
        # trim the tgt list
        tgt_token_list.sort(key=lambda x: x[0], reverse=True)
        cut_pos = 0
        for i in range(len(tgt_token_list)):
            if tgt_token_list[i][0] == -1:
                cut_pos = i
                break
        print('cut pos = ', cut_pos)
        del tgt_token_list[cut_pos:]

    print('length of src:', len(src_token_list), ' length of tgt: ', len(tgt_token_list))
    if len(src_token_list) != len(tgt_token_list):
        print('src token != tgt token')
        return
    # sort the remaining token list using line number
    print(datetime.datetime.now(), 'sorting src list')
    src_token_list.sort(key=lambda x: x[0])
    print(datetime.datetime.now(), 'sorting tgt list')
    tgt_token_list.sort(key=lambda x: x[0])

    # generate the ran_token_list (www-wrong)
    # generate the token list for random tgt token yyy; copy, change the line numbers, replace; no merging
    # first, generate the random line numbers
    random_line(total_lines, total_process_lines, ran_token_list)
    # second, sort the token list
    ran_token_list.sort(key=lambda x: x[0])
    # finally, replace the source token in the list with random tgt tokens from the text file
    random_token(target_txt_rd, ran_token_list, total_process_lines)
    print('line number with random target tokens(www)')
    # print(ran_token_list)

    # change the line number of random token list to be same as the src/tgt token list

    for i in range(len(src_token_list)):
        ran_token_list[i][0] = src_token_list[i][0]
    print('before inserting : line number with real random tokens www')
    # print(ran_token_list)
    print('length: src= ', len(src_token_list), ' tgt = ', len(tgt_token_list), ' random = ', len(ran_token_list))
    # process ( insert tags) the source and target text file
    # process the source text
    print('processing ')
    cho_process_src(para[4], source_txt_rd, source_txt_wr, src_token_list, tgt_token_list, ran_token_list, len(src_token_list))
    # process the target text if the file path is not empty
    if len(target_txt_rd) > 3:
        cho_process_tgt(target_txt_rd, target_txt_wr, tgt_token_list, len(src_token_list))
    print('finish processing!')
    return


if __name__ == '__main__':
    print('argv number ', len(sys.argv))
    # 1st argv: src file(read)
    # 2nd argv: tgt file(read)
    # 3rd argv: ratio in percentage
    # 4th argv: cho or sp (or cp)
    # 5th argv: en-zh or en-de or zh-en
    # output files = input file + ratio * 10 + 4th argv
    main(sys.argv)
