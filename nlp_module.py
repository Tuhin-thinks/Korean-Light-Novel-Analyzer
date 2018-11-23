from konlpy.tag import Kkma, Okt

def pos_Twitter(sentence) :
    """
    Twitter class를 이용해 문장의 tag를 분리하는 함수

    >> print(nlp_module.pos_Twitter('무직전생 1'))
    [('무직', 'Noun'), ('전생', 'Noun'), ('1', 'Number')]

    :param sentence: 분리할 문장
    :return: 분리된 각 tag의 list를 반환
    """
    nlp = Okt()
    result = nlp.pos(phrase=sentence)

    return result

def pos_Kkma(sentence) :
    """
    Kkma class를 이용해서 문장의 tag를 분리하는 함수

    >> print(nlp_module.pos_Kkma('무직전생 1'))
    [('무직', 'NNG'), ('전생', 'NNG'), ('1', 'NR')]

    :param sentence: 분리할 문장
    :return: 분리된 각 tag의 list를 반환
    """
    nlp = Kkma()
    result = nlp.pos(sentence)

    return result

def get_accuracy(title_list, ori_list) :
    """
    책 제목의 유사성을 확인하여 같은 책인지 다른 책인지 0~1 사이의 값으로 반환하는 함수
    두 개의 단어 list를 인자로 받아 책 정확도를 검사
    :param title_list: 비교할 책
    :param ori_list: 기준이 되는 책
    :return: 0.0~1.0 or -1(치명적 차이)
    """
    print(title_list)
    print(ori_list)

    accuracy = 0


    # 두 list의 단어가 비숫한 자리에 있는지
    title_len = len(title_list) - 1
    for i in range(len(ori_list)):
        try:
            if title_list[min(i, title_len)] == ori_list[i] or \
                            title_list[min(i - 1, title_len)] == ori_list[i] or \
                            title_list[min(i + 1, title_len)] == ori_list[i]:
                accuracy += 1
        except:
            print("tried to access index {}".format(i))
            break

    try:
        rate = accuracy / len(ori_list)
    except:
        print('zero devision error')
        return 0.0
    # 측정된 정확도가 일정 이상인데 끝의 숫자가 다르면(즉 같은 시리즈인데 다른 권수일 때)
    if rate >= 0.6 :
        if not ori_list[-1].isdigit() and title_list[-1].isdigit() and \
                        title_list[-1] != '1':
            # 치명적 결과(-1) 반환
            return -1
        elif ori_list[-1].isdigit() and title_list[-1].isdigit() and \
                        title_list[-1] != ori_list[-1]:
            return -1

    # 세트로 발매된 결과를 갖고 왔을 때
    if '세트' in title_list:
        return -1

    len_dif = abs(len(title_list) - len(ori_list))
    #rate -= (len_dif / max(len(title_list), len(ori_list))) * 0.5

    return rate

def search_accsuracy_examine(ori_title, title) :
    """
    검색한 책 제목이 크롤된 책 제목과 맞는지 정확도를 반환하는 함수
    :param book:
    :return:
    """
    # 검색된 제목(book.title)과 크롤된 제목(book.ori_title)을 각각 tagging한다
    ori_nlp = pos_Twitter(ori_title)
    title_nlp = pos_Twitter(title)

    title_list = list()
    ori_list = list()

    # 태그된 데서 단어, 영어, 숫자만 떼어 list화
    punc = False
    for i in title_nlp :
        if i[1] == 'Punctuation' :
            if i[0] == '('\
                    or i[0] == '/':
                punc = True
            else :
                punc = False

        if not punc :
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb'\
                    or i[1] == 'Alpha':
                if i[0] != '권' :
                    title_list.append(i[0])

    for i in ori_nlp :
        if i[1] == 'Noun'  or i[1] == 'Number' or i[1] == 'Verb' \
                or i[1] == 'Alpha':
            ori_list.append(i[0])

    # 정확도을 구한다.
    rate1 = get_accuracy(title_list, ori_list)

    title_list = []

    # 검색된 책제목에서 특수문자('(', '/', '~') 안에 있는 부분만 떼어낸다
    punc = False
    for i in title_nlp:
        if i[1] == 'Punctuation':
            if i[0] == '(' or i[0] == ')'\
                    or i[0] == '/' or i[0] == '~':
                punc = not punc

        if punc :
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb':
                if i[0] != '권' :
                    title_list.append(i[0])

    #정확도를 구한다
    rate2 = get_accuracy(title_list, ori_list)

    # 크롤된 제목에서 특수문자('(', '/', '~') 안에 있는 부분만 떼어낸다
    ori_list = []
    for i in ori_nlp:
        if i[1] == 'Punctuation':
            if i[0] == '(' or i[0] == ')' \
                    or i[0] == '/' or i[0] == '~':
                punc = not punc

        if punc:
            if i[1] == 'Noun' or i[1] == 'Number' or i[1] == 'Verb':
                if i[0] != '권':
                    ori_list.append(i[0])

    # 정확도를 구한다
    rate3 = get_accuracy(title_list, ori_list)

    # 치명적인 에러가 없다면 가장 큰 값을 반환한다.
    if rate1 == -1 :
        return 0
    else:
        return max(rate1, rate2, rate3)

def preprocess_title(title) :
    """
    검색된 제목에서 함께 발매된 권수를 때어내기 위한 함수
    ex. 빙결경계의 에덴 1, 2 -> 빙결경계의 에덴 1, 빙결경계의 에덴 2
    :param title: 검색된 책 제목
    :return: titles list
    """
    result = pos_Twitter(title)
    title_list = []

    print(result)

    comma_found = False
    first_comma = 0
    # pos 태깅한 어절을 순회
    for i, chunk in enumerate(result):
        # 만약 현재 어절이 ','이고
        # 제목 전체 길이에 비해 0.6보다 뒤에 있다면
        # 분해한다
        if chunk[1] == 'Punctuation' and \
                        chunk[0] == ',' \
                and chunk != result[-1]\
                and ((i + 1) / len(result)) >= 0.6:

            if not comma_found :
                # 만약 현재까지 다른 ,이 없었다면
                first_comma = i - 1
                comma_found = True

                print(first_comma)

                # new_title을 선언하고, 콤마가 등장하기 이전까지의
                # 문자열을 저장한다
                new_title = ""
                for j in range(first_comma):

                    new_title += result[j][0]
                new_title += result[i - 1][0]
                # title_list에 만들어진 제목을 집어넣는다
                title_list.append(new_title)
            else :
                # 다른 ,가 없었다면
                # 처음으로 ,가 등장한 부분까지의 제목을 집어넣고, 권수를 그 뒤에 붙인다.
                new_title = ""
                for j in range(first_comma) :
                    new_title += result[j][0]

                new_title += result[i + 1][0]
                title_list.append(new_title)

        i += 1


    if len(title_list) == 0 :
        # 제대로 분해되지 않았다면 원제목을 다시 넣는다
        title_list.append(title)
    else:

        ori_str = title[:title.find(',')]
        for i in range(len(title_list)) :
            title_list[i] = revive_ori_space(ori_str, title_list[i])

    return title_list

def revive_ori_space(ori_str, new_str) :
    """

    :param ori_str:
    :param new_str:
    :return:
    """
    for i in range(len(ori_str)) :
        if ori_str[i] == ' ' and \
                i < len(new_str) and new_str[i] != ' ':
            new_str = new_str[:i] + ' ' + new_str[i:]

    return new_str

def make_alterative_search_set(title) :
    """
    책을 검색할 때 검색하는 책이 발견되지 않으면 원 제목에서 대체할 검색용 문자열을
    만들어내 반환하는 함수
    :param title:
    :return:
    """
    result = pos_Twitter(title)
    title_list = []

    print(result)

    # pos 태깅된 원제목을 순회
    i = 0
    for chunk in result :
        # '시리즈'라는 단어가 나오기 전까지를 대체 검색어로 삼는다
        if chunk[0] == '시리즈' :
            new_title = ""
            for j in range(len(result)) :
                if result[j][0] != '시리즈' :
                    new_title += result[j][0]

            title_list.append(new_title)
        
        # '~'이나 ''' 같은 기호가 나오면 그 다음에 오는 말을 
        # 대체 검색어로 삼는다
        # ex. 쓰르라미 울적에 ~메아카시 편~
        if chunk[1] == 'Punctuation' and \
                chunk[0] == '~' or chunk[0] == "'" :
            new_title = ""
            for j in range(i + 1, len(result)) :
                if result[j][1] == 'Punctuation' :
                    break
                new_title += result[j][0]
            title_list.append(new_title)

            new_title = ""
            for j in range(i) :
                new_title += result[j][0]
            title_list.append(new_title)

            new_title = ""
            for j in range(len(result)) :
                if j > i - 1 :
                    if result[j][1] != 'Punctuation' :
                        new_title += result[j][0]
                else :
                    new_title += result[j][0]
            title_list.append(new_title)

            break

        i += 1
    
    # 만약 끝 자리가 숫자 1이면 (1권이면)
    # 숫자를 삭제한 것을 대체 검색어로 삼는다
    if result[-1][1] == 'Number' and result[-1][0] == '1' :
        new_title = ""
        for i in range(len(result) - 1) :
            new_title += result[i][0]

        title_list.append(revive_ori_space(title, new_title))

    return title_list