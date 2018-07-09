#!/usr/bin/python
# -*- coding: UTF-8 -*-
import codecs
import re

f = codecs.open('D:/downloads/data/train_257.bin','rb')
fw = codecs.open('D:/downloads/data/newData.txt','w')
text = f.readlines()
i = 0
for line in text:
    new_str = re.compile(u'[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]').sub('', line.decode('utf-8',"ignore"))
    new_str = new_str.replace('<s>',' ')
    new_str = new_str.replace('\n',' ')
    new_str = new_str.replace('</s>', ' ')
    new_str = new_str.lower()
    if(len(new_str)<5):
        continue

    if('article' in new_str and len(new_str)<10):
        i += 1
        #continue
        new_str = 'article'
        print(new_str)
        fw.write(new_str + '\n')

        continue
    if(i >= 1):
        if 'abstract' not in new_str and len(new_str)>10:

            if(new_str[0].isalpha()):
                print(new_str)

            else:
                new_str = new_str.replace(new_str[0],'')
                print(new_str)
            fw.write(new_str.encode('utf-8'))
            fw.write('\n')
            i += 1
            continue
        else:
            i = 0
            #print('\n')

f.close()
fw.close()

