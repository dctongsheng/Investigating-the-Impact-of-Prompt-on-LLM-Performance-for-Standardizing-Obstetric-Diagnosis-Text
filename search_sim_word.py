import torch
from qrdant_client import QRDANT

# 假设的模型，用于将词转化为向量
def m3e_emdedding(data_input):
    url = 'http://172.28.114.24:6008/v1/embeddings'
    headers = {
        'Authorization': 'Bearer sk-*********************',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'm3e',
        'input': data_input
    }

    response = requests.post(url, headers=headers, json=data)
    result = json.loads(response.text)

    return result

# 查询QRDANT数据库
def query_similar_words(vector, threshold=0.855, top_k=10):
    qrdant_client = QRDANT('your_qrdant_connection_string')
    results = qrdant_client.search(vector, min_similarity=threshold, limit=top_k)
    return results

def main():
    input_word = input("请输入一个非标准化的词：")
    input_vector = m3e_emdedding(input_word)

    similar_words = query_similar_words(input_vector)
    print("相似的标准词：")
    for word in similar_words:
        print(word)

if __name__ == '__main__':
    main()
