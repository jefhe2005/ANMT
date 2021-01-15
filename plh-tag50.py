import random
import nltk
from nltk.corpus import stopwords
import datetime

# read file and append a list of all lines
def file_to_list(src_file, total_list):
    with open(src_file, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            total_list.append(line)
    return


# check and return
# pos_tokens = [-1, -1, '',  ''] , line number, match or not, position, token, pos attribute
# pos sequence: NN, VERB, ADJ
def check_pos_token(src_line, stoplist):
    src_tokens = src_line.split()
    tagged = nltk.pos_tag(src_tokens)
    pos_tokens = [[-1, False, '', ''], [-1, False, '', ''], [-1, False, '', '']]

    for i in range(len(src_tokens)):
        # not process stopwords and non-unique words in the same sentence
        if src_tokens[i] in stoplist:
            continue
        if src_tokens.count(src_tokens[i]) != 1:
            continue
        # if tagged[i][1].startswith('N') == True and pos_tokens[0][0] < 0:
        if tagged[i][1].find('N') == 0 and pos_tokens[0][0] < 0:
            pos_tokens[0][0] = True
            pos_tokens[0][1] = i
            pos_tokens[0][2] = src_tokens[i]
            pos_tokens[0][3] = tagged[i][1]
        if tagged[i][1].find('V') == 0 and pos_tokens[1][0] < 0:
            pos_tokens[1][0] = True
            pos_tokens[1][1] = i
            pos_tokens[1][2] = src_tokens[i]
            pos_tokens[1][3] = tagged[i][1]
        if tagged[i][1].find('J') == 0 and pos_tokens[2][0] < 0:
            pos_tokens[2][0] = True
            pos_tokens[2][1] = i
            pos_tokens[2][2] = src_tokens[i]
            pos_tokens[2][3] = tagged[i][1]
    return pos_tokens


# Calculate the total number of lines in a text file
def cal_lines(source_txt):
    number_lines = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            number_lines += 1
    source_file.close()
    return number_lines


# Insert a tag with its token into a line of text
def insert_cw_tag(line, tag, flag_noun, token_noun, posi_noun, flag_verb, token_verb, posi_verb, flag_adj,
                   token_adj, posi_adj):
    if tag == 'CW':
        open_copy = '<nulltag>'
        close_copy = '</nulltag>'
        list_token = line.split()
        list_token.append('\n')
        # replace the token at 'position' to 'token' and return
        # sort and replace from the latter position to the beginning position
        insert_list = [[-1, '']]
        if flag_noun > 0:
            insert_list.append([posi_noun, token_noun])
        if flag_verb > 0:
            insert_list.append([posi_verb, token_verb])
        if flag_adj > 0:
            insert_list.append([posi_adj, token_adj])
        insert_list.pop(0)
        print('insert list')
        print(insert_list)
        insert_list.sort(key=lambda x: x[0], reverse=True)
        if len(insert_list) > 0:
            for i in range(len(insert_list)):
                list_token.pop(insert_list[i][0])
                list_token.insert(insert_list[i][0], open_copy + ' ' + insert_list[i][1] + ' ' + close_copy)
        return ' '.join(list_token)


def pos_process_src(read_file, write_file, src_noun_list, src_verb_list, src_adj_list):
    line_number_noun = src_noun_list[0][0]
    src_token_noun = src_noun_list[0][3]
    # src_pos_noun = src_noun_list[0][4]
    total_process_lines_noun = len(src_verb_list)
    line_number_verb = src_verb_list[0][0]
    src_token_verb = src_verb_list[0][3]
    # src_pos_verb = src_verb_list[0][4]
    total_process_lines_verb = len(src_verb_list)
    line_number_adj = src_adj_list[0][0]
    src_token_adj = src_adj_list[0][3]
    # src_pos_adj = src_adj_list[0][4]
    total_process_lines_adj = len(src_adj_list)
    j_noun = 0
    j_verb = 0
    j_adj = 0
    flag_noun = -1
    flag_verb = -1
    flag_adj = -1
    line_number = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if line_number % 3000 == 0:
                print(datetime.datetime.now(), 'reading and writing, line  ', line_number)
            if j_noun < total_process_lines_noun and line_number == line_number_noun:
                # insert pos tag with token to the specific line
                flag_noun = 1

            if j_verb < total_process_lines_verb and line_number == line_number_verb:
                # insert pos tag with token to the specific line
                flag_verb = 1

            if j_adj < total_process_lines_adj and line_number == line_number_adj:
                # insert pos tag with token to the specific line
                flag_adj = 1

            # insert pos tag with token to the specific line
            if flag_noun > 0 or flag_verb > 0 or flag_adj > 0:
                    line = insert_cw_tag(line, 'CW', flag_noun, src_token_noun, src_noun_list[j_noun][2],
                                         flag_verb, src_token_verb, src_verb_list[j_verb][2], flag_adj, src_token_adj,
                                         src_adj_list[j_adj][2])
            target_file.write(line)

            if flag_noun > 0:
                if j_noun < (total_process_lines_noun - 1):
                    j_noun += 1
                    line_number_noun = src_noun_list[j_noun][0]
                    src_token_noun = src_noun_list[j_noun][3]
            if flag_verb > 0:
                j_verb += 1
                if j_verb < (total_process_lines_verb - 1):
                    line_number_verb = src_verb_list[j_verb][0]
                    src_token_verb = src_verb_list[j_verb][3]
            if flag_adj > 0:
                j_adj += 1
                if j_adj < (total_process_lines_adj - 1):
                    line_number_adj = src_adj_list[j_adj][0]
                    src_token_adj = src_adj_list[j_adj][3]

            flag_noun = -1
            flag_verb = -1
            flag_adj = -1
            line_number += 1
    source_file.close()
    target_file.close()
    return


def main():
    # parameters: ratio, filenames
    # percentage of lines for processing
    ratio = 0.5

    # prepare the stoplist
    stoplist = stopwords.words('english')


    # path for source text (before processing)
    source_txt_rd = './UNv1.0.testset.en-og'
    
    # path for source text(after processing)
    source_txt_wr = './UNv1.0.testset.en50plh'

    # path for target text(before processing) --not to process the tgt for now
    target_txt_rd = './UNv1.0.testset.zh-og'
    
    '''
    # path for source text (before processing)
    source_txt_rd = './UNv1.0.devset.en-og'
    
    # path for source text(after processing)
    source_txt_wr = './UNv1.0.devset.en10plh'

    # path for target text(before processing) --not to process the tgt for now
    target_txt_rd = './UNv1.0.devset.zh-og'

    
    # path for source text (before processing)
    source_txt_rd = './UNv1.0.en-zh.en-og'
    
    # path for source text(after processing)
    source_txt_wr = './UNv1.0.en-zh.en10plh'

    # path for target text(before processing) --not to process the tgt for now
    target_txt_rd = './UNv1.0.en-zh.zh-og'
    '''
    # path for target text(after processing)
    # target_txt_wr = './UNv1.0.testset.zhcho'

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

    # initial toke_list(one tokens a sentence maximum)
    src_noun_list = [[-1, False, -1, '', '']]  # line number, match, token position, token, pos
    src_verb_list = [[-1, False, -1, '', '']]  # line number, match, token position, token, pos
    src_adj_list = [[-1, False, -1, '', '']]  # line number, match, token position, token, pos
    # tgt_token_list = [[-1, -1, '']]  #line number, token position, token
    for i in range(total_lines - 1):
        src_noun_list.append([-1, False, -1, '', ''])
        src_verb_list.append([-1, False, -1, '', ''])
        src_adj_list.append([-1, False, -1, '', ''])
        # tgt_token_list.append([-1, -1, ''])
    # print(len(src_token_list))

    # generate the src token(xxx) and its corresponding POS token with the help of nltk

    # read src and tgt files to line lists
    src_total_list = ['']
    # tgt_total_list = ['']
    file_to_list(source_txt_rd, src_total_list)
    # file_to_list(target_txt_rd, tgt_total_list)
    src_total_list.pop(0)
    # tgt_total_list.pop(0)

    # for tokens generated, scan the whole file to get a pos-token list, then randomly pick from it
    for i in range(total_lines):
        if i % 3000 == 0:
            print(datetime.datetime.now(), 'check pos, line:', i, 'length= ', len(src_total_list[i]))
        if len(src_total_list[i]) > 4096:
            print('skip long sentence > 4096 char; line :', i)
            continue
        # process line by line,
        # return from 'check' : match= 1 true or -1 false, token position, token, its POS
        pos_tokens = check_pos_token(src_total_list[i], stoplist)
        src_noun_list[i][0] = i  # keep the line number for future sorting
        src_noun_list[i][1] = pos_tokens[0][0]  # match or not
        src_noun_list[i][2] = pos_tokens[0][1]  # token position
        src_noun_list[i][3] = pos_tokens[0][2]  # token
        src_noun_list[i][4] = pos_tokens[0][3]  # pos attribute
        src_verb_list[i][0] = i  # keep the line number for future sorting
        src_verb_list[i][1] = pos_tokens[1][0]  # match or not
        src_verb_list[i][2] = pos_tokens[1][1]  # token position
        src_verb_list[i][3] = pos_tokens[1][2]  # token
        src_verb_list[i][4] = pos_tokens[1][3]  # pos attribute
        src_adj_list[i][0] = i  # keep the line number for future sorting
        src_adj_list[i][1] = pos_tokens[2][0]  # match or not
        src_adj_list[i][2] = pos_tokens[2][1]  # token position
        src_adj_list[i][3] = pos_tokens[2][2]  # token
        src_adj_list[i][4] = pos_tokens[2][3]  # pos attribute

    # delete the no-match record in the token list
    for i in reversed(range(total_lines)):
        if i % 20000 == 0:
            print(datetime.datetime.now(), 'delete no-match records, line:', i)
        if not src_noun_list[i][1]:
            # src_noun_list.pop(i)
            del src_noun_list[i]
        if not src_verb_list[i][1]:
            # src_verb_list.pop(i)
            del src_verb_list[i]
        if not src_adj_list[i][1]:
            # src_adj_list.pop(i)
            del src_adj_list[i]
    # shuffle the list and get the first "n" of the token list
    list_length = len(src_noun_list)
    if list_length > total_process_lines:
        print('noun list larger than ratio')
        print(list_length)
        random.shuffle(src_noun_list)
        for i in range(list_length - total_process_lines):
            src_noun_list.pop(list_length - 1 - i)
    list_length = len(src_verb_list)
    if list_length > total_process_lines:
        print('verb list larger than ratio')
        print(list_length)
        random.shuffle(src_verb_list)
        for i in range(list_length - total_process_lines):
            src_verb_list.pop(list_length - 1 - i)
    list_length = len(src_adj_list)
    if list_length > total_process_lines:
        print('adj list larger than ratio')
        print(list_length)
        random.shuffle(src_adj_list)
        for i in range(list_length - total_process_lines):
            src_adj_list.pop(list_length - 1 - i)
    # sort the remaining token list using line number
    print(datetime.datetime.now(), 'sorting noun list')
    src_noun_list.sort(key=lambda x: x[0])
    print(datetime.datetime.now(), 'sorting verb list')
    src_verb_list.sort(key=lambda x: x[0])
    print(datetime.datetime.now(), 'sorting adj list')
    src_adj_list.sort(key=lambda x: x[0])
    print('line number after sorting: source xxx')
    print('noun list', len(src_noun_list))
    print(src_noun_list)
    print('verb list', len(src_verb_list))
    print(src_verb_list)
    print('adj list', len(src_adj_list))
    print(src_adj_list)

    # process ( insert tags) the source and target text file
    # process the source text
    pos_process_src(source_txt_rd, source_txt_wr, src_noun_list, src_verb_list, src_adj_list)
    print('finish processing!')
    return


if __name__ == '__main__':
    main()
