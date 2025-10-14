# embedding_cost_calculator.py
# simple_embedding version 0.1
# src/embedding_cost_calculator.py - FIXED VERSION
import tiktoken

def calculate_embedding_cost(texts, model="text-embedding-3-small"):
    """
    Calculate estimated cost for embedding texts
    
    Args:
        texts: List of text strings to embed
        model: OpenAI embedding model name
    
    Returns:
        cost: Estimated cost in USD
    """
    # Tokenizer for the specified model
    encoding = tiktoken.encoding_for_model(model)
    
    # Count tokens across all texts
    total_tokens = 0
    for text in texts:
        total_tokens += len(encoding.encode(text))
    
    # Cost per token (approximate)
    cost_per_token = 0.0000001  # $0.0001 per 1000 tokens = $0.0000001 per token
    
    # Calculate total cost
    total_cost = total_tokens * cost_per_token
    
    print(f"📊 Cost Calculation:")
    print(f"   - Number of texts: {len(texts)}")
    print(f"   - Total tokens: {total_tokens}")
    print(f"   - Model: {model}")
    
    return total_cost

# Alternative simple version if you prefer:
def calculate_embedding_cost_simple(texts, model="text-embedding-3-small"):
    """Simplified cost calculation"""
    total_chars = sum(len(text) for text in texts)
    estimated_tokens = total_chars / 4  # Rough approximation
    cost_per_1k_tokens = 0.0001  # $0.0001 per 1000 tokens
    return (estimated_tokens / 1000) * cost_per_1k_tokens

# Even simpler one-liner for quick estimates
def quick_cost(text):
    """Ultra-simple cost calculation"""
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = len(encoding.encode(text))
    cost = (tokens / 1000) * 0.00002
    return tokens, cost