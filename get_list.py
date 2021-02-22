import Baidu
class json_list:
    def __init__(self, json):
        self.json = json

    def turn_list(self):
        liju_list = []
        fanyi_list = []
        # 选出json数据的例句部分
        sentence_list = eval(self.json['liju_result']['double'])
        # 将例句部分拼合在一起
        for sentence in sentence_list:
            liju = ''
            fanyi = ''
            for sen in sentence[0]:
                liju = liju + sen[0] + ' '
            # print(liju + '\n')
            liju_list.append(liju)
            for sen in sentence[1]:
                fanyi = fanyi + sen[0]
            # print(fanyi + '\n')
            fanyi_list.append(fanyi)

        return liju_list, fanyi_list

if __name__ == '__main__':
    baidu = Baidu.getJson('teacher')
    json = baidu.fetch_json() # 获取json值
    
    if json['trans_result'] == 0:
        print('请求失败 Baidu.py')
    else:
        root = json_list(json)
        liju_list = []
        fanyi_list = []
        liju_list, fanyi_list = root.turn_list() # 得到例句和翻译的列表
        print(liju_list)
        print(fanyi_list)
            