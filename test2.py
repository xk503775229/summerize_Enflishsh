# -*- coding:utf-8 -*-
import codecs
import math
import re
import nltk
# text1 = "This game is one of the very best. games ive  played. the  ;pictures? " \
#         "cant describe the real graphics in the game."
# text2 = "this game have/ is3 one of the very best. games ive  played. the  ;pictures? " \
#         "cant describe now the real graphics in the game."
# text3 = "So in the picture i saw a nice size detailed metal puzzle. Eager to try since I enjoy 3d wood puzzles, i ordered it. Well to my disappointment I got in the mail a small square about 4 inches around. And to add more disappointment when I built it it was smaller than the palm of my hand. For the price it should of been much much larger. Don't be fooled. It's only worth $5.00.Update 4/15/2013I have bought and completed 13 of these MODELS from A.C. Moore for $5.99 a piece, so i stand by my comment that thiss one is overpriced. It was still fun to build just like all the others from the maker of this brand.Just be warned, They are small."
# text4 = "I love it when an author can bring you into their made up world and make you feel like a friend, confidant, or family. Having a special child of my own I could relate to the teacher and her madcap class. I've also spent time in similar classrooms and enjoyed the uniqueness of each and every child. Her story drew me into their world and had me laughing so hard my family thought I had lost my mind, so I shared the passage so they could laugh with me. Read this book if you enjoy a book with strong women, you won't regret it."

def compute_cosine(text_a, text_b):
    # 找单词及词频
    words1 = text_a.split(' ')
    words2 = text_b.split(' ')
    # print(words1)
    words1_dict = {}
    words2_dict = {}
    for word in words1:
        # word = word.strip(",.?!;")
        word = re.sub('[^a-zA-Z]', '', word)
        word = word.lower()
        # print(word)
        if word != '' and word in words1_dict.keys():
            num = words1_dict[word]
            words1_dict[word] = num + 1
        elif word != '':
            words1_dict[word] = 1
        else:
            continue
    for word in words2:
        # word = word.strip(",.?!;")
        word = re.sub('[^a-zA-Z]', '', word)
        word = word.lower()
        if word != '' and word in words2_dict.keys():
            num = words2_dict[word]
            words2_dict[word] = num + 1
        elif word != '':
            words2_dict[word] = 1
        else:
            continue

    dic1 = sorted(words1_dict.items(), key=lambda asd: asd[1], reverse=True)
    dic2 = sorted(words2_dict.items(), key=lambda asd: asd[1], reverse=True)
    # print(dic1)
    # print(dic2)

    # 得到词向量
    words_key = []
    for i in range(len(dic1)):
        words_key.append(dic1[i][0])  # 向数组中添加元素
    for i in range(len(dic2)):
        if dic2[i][0] in words_key:
            # print 'has_key', dic2[i][0]
            pass
        else:  # 合并
            words_key.append(dic2[i][0])
    # print(words_key)
    vector_1 = []
    vector_2 = []
    for word in words_key:
        if word in words1_dict.keys():
            vector_1.append(words1_dict[word])
        else:
            vector_1.append(0)
        if word in words2_dict.keys():
            vector_2.append(words2_dict[word])
        else:
            vector_2.append(0)



    return calCosine(vector_1, vector_2)
# 计算余弦相似度
def calCosine(vector1, vector2):
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(vector1)):
        sum += vector1[i] * vector2[i]
        sq1 += pow(vector1[i], 2)
        sq2 += pow(vector2[i], 2)
    try:
        result = round(float(sum) / (math.sqrt(sq1) * math.sqrt(sq2)), 2)
    except ZeroDivisionError:
        result = 0.0
    # print(result)
    return result

#求某一句话对所有句子余弦的平均值
def avg(result):
    sum = 0
    n = len(result)
    for i in result:
        sum += i
    if sum > 0 :
        result = round(sum/n,2)
    else: result = 0
    #print(result)
    return result

#处理文章,并写入fp
def handleArticle(line_str,fp):
        sentences = [s for s in nltk.tokenize.sent_tokenize(line_str)]
        # print(sentences)
        n = len(sentences)
        # print(n)
        resultDic = {}
        #嵌套循环，计算每个句子与其他句子的相似度
        for i in range(0, n):
            # print(i)
            resultTotal = []
            for j in range(i + 1, n):
                result = compute_cosine(sentences[i], sentences[j])
                resultTotal.append(result) #将一个句子与其他句子余弦相似度放到一起
            resultDic.update({i:avg(resultTotal)})#将每个句子的平均相似度放入字典中
        top_n = sorted(resultDic.items(),key=lambda s:s[1],reverse = True)[:2]#从大到小排序，取出前两句作为总结
        print('abstract : ')
        print([sentences[idx] for (idx,score) in top_n] )
        #for i in range(0 , len(top_n)):
        #只输出大于2句话的总结
        if len(top_n)>=2:
            fp.write('abstract : '+sentences[top_n[0][0]] + sentences[top_n[1][0]]+'\n'+'\n')#写入文档
        print('\n')


if __name__ == '__main__':
    fr = codecs.open('D:/downloads/data/newData2.txt','rb')
    fw = codecs.open('D:/downloads/data/result.txt','w',encoding='utf-8')
    lines = fr.readlines()
    #每一行就是一篇文章
    for line in lines:
        line_str = str(line, encoding="utf-8")
        if 'article' not in line_str and len(line_str) > 10:
            handleArticle(line_str,fw)
            #break
    fr.close()
    fw.close()
