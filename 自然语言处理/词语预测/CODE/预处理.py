# -*- coding: UTF-8 -*-
import re
import jieba
import os

word_dict = {}
# 读取停止词
stop_words = []
with open('停止词.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip()
        if len(line) == 0:
            continue
        stop_words.append(line)

# print(len(stop_words))
# 1732


for i in range(1, 1001):
    # 工作路径和代码路径可能不同，最好不用相对路径
    cur_path = os.getcwd()
    file_path = cur_path + r'/爬取的新闻/' + str(i) + '.txt'
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        article = f.read()
        # 去标点 去除数字字母
        punctuation = "A-Za-z0-9;,：:＃＄％＆＇（）＊＋，－：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】" \
                      "〔〕〖〗〘〙〚〛〜〝〞–—‘’‛“”„‟…‧﹏"
        article = re.sub(r'[{}]+'.format(punctuation), '', article)
        # 分句 句子以以下符号分句
        # [字符集]， + 扩展
        after_process = ''
        # \n 也可以这样用
        pattern = r'[\r|。|！|!|?|？|｡|\n]+'
        result_list = re.split(pattern, article)
        for sentence in result_list:
            result = list(jieba.cut(sentence, cut_all=False))
            sentence_after_p = ''
            for word in result[::-1]:
                word_strip = word.strip().lstrip()
                # 该词空 或者是 停止词，就删除掉
                if not word_strip or word_strip in stop_words:
                    result.remove(word)
                    continue
                else:
                    if word_dict.get(word_strip, None):
                        word_dict[word_strip] += 1
                    else:
                        word_dict[word_strip] = 1

            sentence_after_p = " ".join(result)
            after_process = after_process + sentence_after_p + '\n'
            # result = " ".join(result)
            # print(result)

        # print(after_process)
        cur_path2 = os.getcwd()
        file_path2 = cur_path2 + r'/预处理结果去停止词/' + str(i) + '.txt'
        with open(file_path2, 'w', encoding='utf-8') as f_save:
            f_save.write(after_process)


# 建立词表
final_word_dict = ''
n = 0
for word in word_dict.keys():
    n += 1
    final_word_dict = final_word_dict + str(n) + ' ' + word + ' ' + str(word_dict[word]) + '\n'

# print(len(word_dict_without_stop_word))
# 52465

cur_path3 = os.getcwd()
file_path3 = cur_path3 + r'/word_dict2.txt'
with open(file_path3, 'w', encoding='utf-8') as f_save:
    f_save.write(final_word_dict)
