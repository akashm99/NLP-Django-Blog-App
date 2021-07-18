from transformers import GPT2LMHeadModel, GPT2Tokenizer, pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class NlpBlog():
    # def __init__(self, sentence):
    #     self.input = sentence

    def text_generation(self, input):
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2-large')
        model = GPT2LMHeadModel.from_pretrained('gpt2-large', pad_token_id=tokenizer.eos_token_id)
        input_ids = tokenizer.encode(input, return_tensors='pt')
        output = model.generate(input_ids, max_length=500, min_length=100, num_beams=5, no_repeat_ngram_size=2,
                                early_stopping=True)
        final = tokenizer.decode(output[0], skip_special_tokens=True)

        return final

    def text_summarization(self, input):
        summarizer = pipeline('summarization')
        ARTICLE = input.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')
        sentences = ARTICLE.split('<eos>')
        current_chunk = 0
        max_chunk = 500
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1:
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))
        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        res = summarizer(chunks, max_length=120, min_length=30, do_sample=False)
        final = ' '.join([summ['summary_text'] for summ in res])

        return final

    def text_sentiment(self, input):
        tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')
        tokens = tokenizer.encode(input, return_tensors='pt')
        result = model(tokens)
        final = int(torch.argmax(result.logits))+1

        return final




