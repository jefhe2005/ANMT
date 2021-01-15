
# Calculate the total number of lines in a text file
def cal_lines(source_txt):
    number_lines = 0
    with open(source_txt, 'r', encoding='utf-8') as source_file:
        for line in source_file:
            number_lines += 1
    source_file.close()
    return number_lines


# check a tag between two lines;
def check_sentence_pair(line_src, line_tgt, tag):
    # if tag == copy
    if tag == 'COPY':
        open_copy = '<copy>'
        close_copy = '</copy>'
        src_tokens = line_src.split()
        tgt_tokens = line_tgt.split()
        try:
            open_pos_src = src_tokens.index(open_copy)
        except:
            open_pos_src = -1
        try:
            clos_pos_src = src_tokens.index(close_copy)
        except:
            clos_pos_src = -1
        try:
            open_pos_tgt = tgt_tokens.index(open_copy)
        except:
            open_pos_tgt = -1
        try:
            clos_pos_tgt = tgt_tokens.index(close_copy)
        except:
            clos_pos_tgt = -1

        # do statistics; false_positive = src has no tag, tgt has tag ; false_negative = src has tag, tgt has no tag;
        # false_positive = result_list.count(3)
        # false_negative = result_list.count(5)
        # correct = result_list.count(1); 2 if tag is correct, but token inside has changed
        # no_match = result_list.count(9)
        src_tag = False
        tgt_tag = False
        if open_pos_src >= 0 and clos_pos_src == (open_pos_src + 2):
            src_tag = True
        if open_pos_tgt >= 0 and clos_pos_tgt == (open_pos_tgt + 2):
            tgt_tag = True

        if src_tag == True and tgt_tag == False:
            return 5  # false negative
        if src_tag == False and tgt_tag == True:
            return 3  # false positive
        if src_tag == False and tgt_tag == False:
            return 9  # no match
        if src_tag == True and tgt_tag == True:
            if src_tokens[open_pos_src + 1] == tgt_tokens[open_pos_tgt + 1]:
                return 1  # correct
            else:
                print('copy tag is good, but token inside is wrong')
                print(src_tokens[open_pos_src + 1])
                print('to')
                print(tgt_tokens[open_pos_tgt + 1])
                return 2
        return -1

def main():
    # parameters: ratio, filenames
    # percentage of lines for processing
    ratio = 0.01

    # path for source text (before processing)
    source_txt_rd = './UNv1.0.testset.en2'

    # path for target text(before processing)
    target_txt_rd = './UNv1.0.testset.zh2'

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

    # initialize result list
    result_list = [-1]
    for i in range(total_lines-1):
        result_list.append(-1)
    print('initial result list = ')
    print(result_list)

    i = 0
    with open(source_txt_rd, 'r', encoding='utf-8') as source_file, open(target_txt_rd, 'r',
                                                                        encoding='utf-8') as target_file:
        for line_src in source_file:
            line_tgt = target_file.readline()
            print(line_src)
            print(line_tgt)
            result_list[i] = check_sentence_pair(line_src, line_tgt, 'COPY')
            i += 1

    print('real result list = ')
    print(result_list)
    # do statistics; false_positive = src has no tag, tgt has tag ; false_negative = src has tag, tgt has no tag;
    false_positive = result_list.count(3)
    false_negative = result_list.count(5)
    correct = result_list.count(1)
    half_correct = result_list.count(2)
    no_match = result_list.count(9)
    if (correct + false_negative + false_positive) != 0:
        ratio_correct = correct/(correct + false_negative + false_positive)
    else:
        print('(correct + false_negative + false_positive) = 0 ! ')
        ratio_correct = -1
    print('correct = ')
    print(correct)
    print('half correct = ')
    print(half_correct)
    print('false_positive = ')
    print(false_positive)
    print('false_negative = ')
    print(false_negative)
    print('ratio_correct = ')
    print(ratio_correct)
    print('finish processing!')
    return


if __name__ == '__main__':
    main()
