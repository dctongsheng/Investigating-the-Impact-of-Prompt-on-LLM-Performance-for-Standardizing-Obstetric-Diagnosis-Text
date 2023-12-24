
# Investigating the Impact of Prompt Engineering on LLM Performance for Standardizing Obstetric Diagnosis Text: A Comparative Study 

## 1. Download and Install the Vector Database Qdrant
Download and run
First, download the latest Qdrant image from Dockerhub:
```bash
docker pull qdrant/qdrant
```

Then, run the service:
```bash
docker run -p 6333:6333 -p 6334:6334     -v $(pwd)/qdrant_storage:/qdrant/storage:z     qdrant/qdrant
```

Under the default configuration all data will be stored in the ./qdrant_storage directory. This will also be the only directory that both the Container and the host machine can both see.

## 2. Download the Vector Model from Hugging Face and Store the Vectors in the Vector Database
```bash
git clone hf@git.co:bert-base-chinese
```
To write embeddings into the database, run the following code:
```python
qdrant.recreate_collection(
    collection_name="term_standardization_20231122",
    vectors_config=models.VectorParams(
        size=model.get_sentence_embedding_dimension(), # Vector size is defined by used model
        distance=models.Distance.COSINE
    )
)
```

## 3. Deploy Large Models
Download the Qwen large model and the GLM large model
```bash
git clone hf@git.co:THUDM/chatglm2-6b
git clone hf@git.co:Qwen/Qwen-14B-Chat
```
Deploy large models based on FastChat
```bash
python3 -m fastchat.serve.controller
python3 -m fastchat.serve.model_worker --model-path Qwen/Qwen-14B-Chat
python3 -m fastchat.serve.gradio_web_server
```
Run example
```python
import openai
model_name="Qwen-14B-Chat"
openai.api_key="sk-vCZwJqT9Sviz******************89224D3F7F9"
openai.api_base="http://124.222.128.207:3000/v1"
completion = openai.ChatCompletion.create(model=model_name,
                                          messages=[{"role":"user","content":"Who created you?"}],
                                          temperature=0.7,
                                          max_tokens=512,
                                          top_p=0.7)
print(completion.choices[0].message.content)
# output: I am a large-scale language model from Alibaba Cloud, my name is Tongyi Qianwen.
```

## 4. Input Diagnostic Vocabulary, Match from the Vector Database, and Combine with Large Model to Output Standard Vocabulary
Four Prompt Schemes
* Zero-shot-learning Prompt
* In-context-learning Prompt
* Chain-of-thought learning Prompt
* Self-consistency Prompt
