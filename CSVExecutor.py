import csv


def read_csv(path):
    data = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        first = True
        for row in file:
            if first:
                row[0] = row[0][1:]
                first = False
            # if row[1] == "anger":
            #     row[1] = 1
            # elif row[1] == "joy":
            #     row[1] = 2
            # elif row[1] == "fear":
            #     row[1] = 3
            # elif row[1] == "sad":
            #     row[1] = 4
            # else:
            #     row[1] = 5
            data.append(row)
    return data


def read_csv_emo(path,emo):
    data = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        for row in file:
            if  row[1] == emo :
                data.append(row)
    return data


# def read_csv_emoji(path):
#     data = []
#     with open(path, newline='', encoding='utf-8') as csvfile:
#         file = csv.reader(csvfile, delimiter=',')
#         for row in file:
#             first = True
#             emoji = []
#             for item in row:
#                 if first:
#                     emoji.append(item[2:])
#                     first = False
#                 else:
#                     emoji.append(item[1:])
#             data.append(emoji)
#     return data

def read_csv_without_first_strange_char(path):
    data = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        file = csv.reader(csvfile, delimiter=',')
        first = True
        for row in file:
            data.append(row)
    return data


def write_csv(path, data):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        file = csv.writer(csvfile)
        for item in data:
            file.writerow(item)


def to_dataset_format(data, header):
    formatted = []
    header.append('class')
    formatted.append(header)
    for item in data:
        freq_t = []
        for h in header:
            if h != 'class':
                freq_t.append(item[0].get(h))
        freq_t.append(item[1])
        formatted.append(freq_t)
    return formatted

# print(read_csv('sad_test.csv'))
