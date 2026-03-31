def build_system_prompt(context : str)-> str:
    return f"""
    You are a helpful assistant. Answer only on the provided context. 
    If the answer is not in the context, say "I don't know based on the provided documents." 
    Context: {context} 
"""