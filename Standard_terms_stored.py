import pandas as pd
import torch
from qrdant_client import QRDANT

# 读取CSV文件
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df['standard_word'].tolist()  

# 转换为M3E模型的向量（示例，需要根据实际模型进行调整）
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

res = m3e_emdedding(["hi","hhh"])
print(res)

# 将向量存储到QRDANT数据库
def store_vectors_in_qrdant(vectors):
    qrdant_client = QRDANT('your_qrdant_connection_string')
    for i, vector in enumerate(vectors):
        qrdant_client.insert(vector, metadata={"word_index": i})

# 主函数
def main():
    words = read_excel('国际疾病分类 ICD-10北京临床版v601.xlsx')
    vectors = words_to_vectors(words)
    store_vectors_in_qrdant(vectors)

if __name__ == '__main__':
    main()
