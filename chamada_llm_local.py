from openai import OpenAI
client_openai = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

resposta_llm = client_openai.chat.completions.create(
    model="google/gemma-3-4b",
    messages=[
        {"role":"system","content":"Voce e um assistente de IA Sarcastico"},
        {"role":"user", "content":"O que e o LM Studio?"} 
    ],
    temperature=1.0
)
print(resposta_llm.choices[0].message.content)