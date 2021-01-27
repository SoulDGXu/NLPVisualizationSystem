import time
import business
from business import Business

'''
运行前需要从以下百度网盘链接下载

https://pan.baidu.com/s/1hSFBjQHLhYDw9jPBDNH6pw&shfl=sharepset
这个路径包含data文件夹下的内容
business.json
glove.6B.100d.txt
review.json

https://pan.baidu.com/s/1gnANAnoGv5GHQKWwAIVE4Q&shfl=sharepset
这个路径包含data文件夹下的模型文件
svm_clf.pkl


'''


def get_review_summary_for_business(biz_id):
	# 获取每一个business的评论总结
	return business_module.aspect_based_summary(biz_id)

def main():

	bus_ids = ["tstimHoMcYbkSC4eBA1wEg","gnKjwL_1w79qoiV3IC_xQQ"]  # 指定几个business ids

	for bus_id in bus_ids:
		# print ("Working on biz_id %s" % bus_id)
		start = time.time()

		summary = get_review_summary_for_business(bus_id)

		print("\n")

		normal_print_list = ["business_id","business_name","business_rating", "rating"]
		for item in summary.items():
			if item[0] in normal_print_list:
				print(str(item[0]) + ": " + str(item[1]))
			else:
				print(str(item[0]) + ": ")
				# for content in item[1]:
				# 	print(content)
				for data in item[1].items():
					# print(str(data[0]) + ": " + str(data[1]))
					print("------------------" + str(data[0]) + "------------------")
					for data_1 in data[1].items():
						if data_1[0] in normal_print_list:
							print(str(data_1[0]) + ": " + str(data_1[1]))
						else:
							review_list = []
							for item_1 in data_1[1]:
								review_list.append(item_1)
							print(str(data_1[0]) + ": " + ";  ".join(review_list))

if __name__ == "__main__":
	business_module = Business()
	main()




