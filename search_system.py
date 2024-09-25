from sentence_transformers import SentenceTransformer, util
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class SmartSearch:
    def __init__(self):
        self.courses = self.load_courses()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.course_embeddings = self.model.encode([c['title'] + " " + c['description'] for c in self.courses])
        
        self.llm_model = AutoModelForCausalLM.from_pretrained("gpt2")
        self.llm_tokenizer = AutoTokenizer.from_pretrained("gpt2")

    def load_courses(self):
        with open('courses.json', 'r') as f:
            return json.load(f)

    def search(self, query):
        query_embedding = self.model.encode(query)
        cos_scores = util.pytorch_cos_sim(query_embedding, self.course_embeddings)[0]
        top_results = torch.topk(cos_scores, k=3)
        
        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            results.append({
                'course': self.courses[idx],
                'score': score.item()
            })
        
        return results

    def generate_response(self, query, results):
        prompt = f"User query: {query}\n\nRelevant courses:\n"
        for r in results:
            prompt += f"- {r['course']['title']}: {r['course']['description']}\n"
        prompt += "\nBased on the user's query and the relevant courses, provide a helpful response:"

        inputs = self.llm_tokenizer(prompt, return_tensors="pt")
        outputs = self.llm_model.generate(**inputs, max_length=200, num_return_sequences=1, temperature=0.7)
        response = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response

search_system = SmartSearch()
