import openai

def determine_standard_word(input_word, similar_words, prompt_template, openai_api_key):
    prompt = prompt_template.format(input_word=input_word, similar_words=", ".join(similar_words))
    
    openai.api_key = openai_api_key
    response = openai.Completion.create(
        engine="Qwen-14B-chat",
        prompt=prompt,
        max_tokens=50
    )
    
    return response.choices[0].text.strip()

def process_file(input_file, output_file, openai_api_key,prompt_tem):
    # prompt_template = "Given an input word '{input_word}' and its similar words {similar_words}, identify the most likely standard word."

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            input_word, similar_words_str = line.strip().split(':')
            similar_words = similar_words_str.split(',')

            standard_word = determine_standard_word(input_word, similar_words, prompt_tem, openai_api_key)
            outfile.write(f"{input_word}: {standard_word}\n")

def main():
    input_file = 'data.csv'  
    output_file = 'data_output.csv' 

    # read prompt
    with open("./prompt_design") as f:
        prompts = f.read()
        prompts = prompts.split("/n/n")
        prompts = [i.split("##3#")[-1] for i in prompts]
        prompts_name=[i.split("##3#")[0] for i in prompts]


    for index,prompt in enumerate(prompts):
        process_file(input_file, prompts_name[index]+output_file, openai_api_key,prompt_tem=prompt)

if __name__ == '__main__':
    main()
