# 程序功能：爬取百度热搜榜数据
# 原创作者：马哥python说
# 联系方式：公众号"老男孩的平凡之路"

import requests
import pandas as pd


def get_hot_items(json_data):
	"""兼容百度热搜新旧接口结构，返回热搜条目列表。"""
	card = json_data['data']['cards'][0]

	if 'topContent' in card or card.get('content') and isinstance(card['content'][0], dict) and 'query' in card['content'][0]:
		return card.get('topContent', []) + card.get('content', [])

	content = card.get('content', [])
	if content and isinstance(content[0], dict) and 'content' in content[0]:
		return content[0]['content']

	return content

# 百度热搜榜接口地址
url = 'https://top.baidu.com/api/board?platform=wise&tab=realtime'
# 请求头
header = {
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36',
	'Host': 'top.baidu.com',
	'Accept': 'application/json, text/plain, */*',
	'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
	'Accept-Encoding': 'gzip, deflate, br',
	'Referer': 'https://top.baidu.com/board?tab=novel',
}
# 发送请求
r = requests.get(url, headers=header)
print("响应码：", r.status_code)
r.raise_for_status()
# 用json格式接收请求数据
json_data = r.json()
title_list = []  # 标题
order_list = []  # 排名
top_list = []  # 是否置顶
hot_tag_list = []  # 热度标签代码
hot_name_list = []  # 热度标签名
label_name_list = []  # 内容标签名
feed_floor_type_list = []  # 特殊内容类型
url_list = []  # 链接地址
logid_list = []  # 批次logid
board_name_list = []  # 榜单名称

logid = json_data.get('data', {}).get('logid', '')
board_name = json_data.get('data', {}).get('currentBoard', {}).get('text', '')

# 爬取热搜
content_list = get_hot_items(json_data)
for item in content_list:
	title = item.get('query') or item.get('word', '')
	print("热搜标题: ", title)
	title_list.append(title)
	order_list.append(item.get('index', 0 if item.get('isTop') else ''))
	top_list.append(item.get('isTop', ''))
	hot_tag_list.append(item.get('hotTag', ''))
	hot_name_list.append(item.get('newHotName', ''))
	label_name_list.append(item.get('labelTagName', ''))
	feed_floor_type_list.append(item.get('feedFloorType', ''))
	url_list.append(item.get('url', ''))
	logid_list.append(logid)
	board_name_list.append(board_name)
# 拼装爬取到的数据为DataFrame
df = pd.DataFrame(
	{
		'热搜标题': title_list,
		'热搜排名': order_list,
		'是否置顶': top_list,
		'热度标签代码': hot_tag_list,
		'热度标签名': hot_name_list,
		'内容标签名': label_name_list,
		'特殊内容类型': feed_floor_type_list,
		'链接地址': url_list,
		'批次logid': logid_list,
		'榜单名称': board_name_list
	}
)
# 保存结果数据
df.to_excel('百度热搜榜.xlsx', index=False)
print('爬取结束！已保存至：百度热搜榜.xlsx')
