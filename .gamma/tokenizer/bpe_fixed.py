#!/usr/bin/env python3
"""Tokenizador BPE con gestión autónoma de rutas"""
import json
from pathlib import Path
import sys

PHI = (1 + 5**0.5) / 2

class MinimalBPETokenizer:
    def __init__(self, vocab_size=500):
        self.vocab_size = vocab_size
        self.vocab = {}
        self.merges = {}
        
        self.base_dir = Path(__file__).parent.parent
        (self.base_dir / 'tokenizer').mkdir(exist_ok=True)
        
    def get_stats(self, tokens):
        pairs = {}
        for i in range(len(tokens)-1):
            pair = (tokens[i], tokens[i+1])
            pairs[pair] = pairs.get(pair, 0) + 1
        return pairs
    
    def merge_pair(self, tokens, pair, idx):
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == pair[0] and tokens[i+1] == pair[1]:
                new_tokens.append(idx)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        return new_tokens
    
    def train(self, text):
        tokens = list(text.encode('utf-8'))
        self.vocab = {i: bytes([i]) for i in range(256)}
        next_idx = 256
        
        for _ in range(self.vocab_size - 256):
            pairs = self.get_stats(tokens)
            if not pairs:
                break
            
            best_pair = max(pairs, key=pairs.get)
            self.merges[best_pair] = next_idx
            self.vocab[next_idx] = self.vocab[best_pair[0]] + self.vocab[best_pair[1]]
            tokens = self.merge_pair(tokens, best_pair, next_idx)
            next_idx += 1
    
    def encode(self, text):
        tokens = list(text.encode('utf-8'))
        while True:
            pairs = self.get_stats(tokens)
            if not pairs:
                break
            pair = min(pairs, key=lambda p: self.merges.get(p, float('inf')))
            if pair not in self.merges:
                break
            tokens = self.merge_pair(tokens, pair, self.merges[pair])
        return tokens
    
    def decode(self, tokens):
        bytes_list = b''.join([self.vocab[t] for t in tokens])
        return bytes_list.decode('utf-8', errors='replace')
    
    def save(self, path=None):
        if path is None:
            path = self.base_dir / 'tokenizer/bpe_vocab.json'
        
        state = {
            'vocab_size': self.vocab_size,
            'vocab': {str(k): list(v) for k, v in self.vocab.items()},
            'merges': {f"{k[0]},{k[1]}": v for k, v in self.merges.items()}
        }
        
        with open(path, 'w') as f:
            json.dump(state, f, indent=2)
        
        return path

if __name__ == "__main__":
    print("🜂 ENTRENANDO TOKENIZADOR BPE MÍNIMO")
    
    tokenizer = MinimalBPETokenizer(vocab_size=500)
    corpus = "the fox jumps " * 100
    tokenizer.train(corpus)
    
    print(f"✓ Vocabulario entrenado: {len(tokenizer.vocab)} tokens")
    
    test = "the fox jumps"
    encoded = tokenizer.encode(test)
    decoded = tokenizer.decode(encoded)
    
    print(f"\n✓ Original: {test}")
    print(f"✓ Encoded: {encoded}")
    print(f"✓ Decoded: {decoded}")
    
    vocab_path = tokenizer.save()
    print(f"✓ Tokenizador guardado: {vocab_path}")
    print(f"\n🜂 Tokenizador BPE operacional - Sin dependencias binarias")
    
    sys.exit(0)
