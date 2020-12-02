import random
import nltk
from nltk.corpus import stopwords


# read file and append a list of all lines
def file_to_list(src_file, total_list):
    with open(src_file, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            total_list.append(line)
    return


# check and return
# pos_tokens = [-1, -1, '',  ''] , line number, match or not, position, token, pos attribute
def check_pos_token(src_line, stoplist):
    src_tokens = src_line.split()
    tagged = nltk.pos_tag(src_tokens)
    pos_tokens = [-1, -1, '', '']

    for i in range(len(src_tokens)):
        # not process stopwords and non-unique words in the same sentence
        if src_tokens[i] in stoplist:
            continue
        if src_tokens.count(src_tokens[i]) != 1:
            continue
        if tagged[i][1].find('N') == 0 or tagged[i][1].find('V') == 0:
            pos_tokens[0] = 1
            pos_tokens[1] = i
            pos_tokens[2] = src_tokens[i]
            pos_tokens[3] = tagged[i][1]
            return pos_tokens
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
def insert_pos_tag(line, tag, token, position):
    if tag == 'POS':
        open_copy = '<focus>'
        close_copy = '</focus>'
        list_token = line.split()
        list_token.append('\n')
        # replace the token at 'position' to 'token' and return
        list_token.pop(position)
        list_token.insert(position, open_copy + ' ' + token + ' ' + close_copy)
        return ' '.join(list_token)


def pos_process_src(read_file, write_file, src_token_list):
    line_number = src_token_list[0][0]
    src_token = src_token_list[0][3]
    src_pos = src_token_list[0][4]
    total_process_lines = len(src_token_list)
    i = 0
    j = 0
    with open(read_file, 'r', encoding='utf-8') as source_file, open(write_file, 'w',
                                                                        encoding='utf-8') as target_file:
        for line in source_file:
            if j < total_process_lines:
                if i == line_number:
                    # insert pos tag with token to the specific line
                    print('insert')
                    print(src_token)
                    print(src_pos)
                    token = src_token + ' ' + '<POS>' + ' ' + src_pos
                    line = insert_pos_tag(line, 'POS', token, src_token_list[j][2])
                    j += 1
                    if j < total_process_lines:
                        line_number = src_token_list[j][0]
                        src_token = src_token_list[j][3]
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

    # prepare the stoplist
    stoplist = stopwords.words('english')

    # path for source text (before processing)
    source_txt_rd = './UNv1.0.testset.en'
    # path for source text(after processing)
    source_txt_wr = './UNv1.0.testset.enpos'

    # path for target text(before processing) --not to process the tgt for now
    target_txt_rd = './UNv1.0.testset.zh'
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

    # initial toke_list(one tokens a sentence maximun)
    src_token_list = [[-1, -1, -1, '', '']]  # line number, match, token position, token, pos
    # tgt_token_list = [[-1, -1, '']]  #line number, token position, token
    for i in range(total_lines - 1):
        src_token_list.append([-1, -1, -1, '', ''])
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

    # for POS tokens generated, scan the whole file to get a pos-token list, then randomly pick from it
    for i in range(total_lines):
        # process line by line,
        # return from 'check' : match= 1 true or -1 false, token position, token, its POS
        pos_tokens = check_pos_token(src_total_list[i], stoplist)
        src_token_list[i][0] = i  # keep the line number for future sorting
        src_token_list[i][1] = pos_tokens[0]  # match or not
        src_token_list[i][2] = pos_tokens[1]  # token position
        src_token_list[i][3] = pos_tokens[2]  # token
        src_token_list[i][4] = pos_tokens[3]  # pos attribute

    # delete the no-match record in the token list
    for i in range(total_lines):
        if src_token_list[total_lines - 1 - i][1] < 0:
            src_token_list.pop(total_lines - 1 - i)

    # shuffle the list and get the first "n" of the token list
    list_length = len(src_token_list)
    if list_length > total_process_lines:
        random.shuffle(src_token_list)
        for i in range(list_length - total_process_lines):
            src_token_list.pop(list_length - 1 - i)
    # sort the remaining token list using line number
    src_token_list.sort(key=lambda x: x[0])
    print('line number after sorting: source xxx')
    print(src_token_list)

    # process ( insert tags) the source and target text file
    # process the source text
    pos_process_src(source_txt_rd, source_txt_wr, src_token_list)
    print('finish processing!')
    return


if __name__ == '__main__':
    main()
