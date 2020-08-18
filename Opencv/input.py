with open('out.txt', 'r') as f:
    content = f.read()

# content = content.strip().replace('\n', '')
content = content.replace('\n','').replace(' ','').replace(",device='cuda:0'", '')
content = content.replace("'boxes'",'')
content = content.replace("'labels'",'')
content = content.replace("'scores'",'')
content = content.replace(":tensor",'')

content1 = content.split('}')

dic = {}

for content2 in content1[:-1]:
    id = content2.split('{')[0]
    content3 = content2.split('{')[1].strip('(').split(')')
    boxes = content3[0].strip('[').strip(']').split('],[')
    lables = content3[1].strip(',(').strip('[').strip(']').split(',')
    scores = content3[2].strip(',(').strip('[').strip(']').split(',')
    result = zip(boxes, lables, scores)
    dic[int(id)] = list(result)

final = sorted(dic.items(), key=lambda obj: obj[0])
print(final[0][1])
for i in final[0][1]:
    print(i[0])
    print(i[1])
    print(i[2])


# for i in final:
#     print(i[0])
#     for j in i[1]:
#         print(j)

#     content2 = content1.split('{')[1]
#     content2 = content2.split(':')
#     boxes = content2[1]
#     lables = content2[2]
#
#     for content3 in content2:
#         print(content3)

# for content_1 in contents_1:
#     print(content_1)


# result = content.split('}')

# print(content)
# print(result)