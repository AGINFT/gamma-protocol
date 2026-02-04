#!/usr/bin/env python3
"""Motor NanoGPT φ-coherente sin dependencias binarias"""
import numpy as np
import json
from pathlib import Path

PHI = (1 + np.sqrt(5)) / 2

class NanoGPTGamma:
    def __init__(self, vocab_size=500, dim=128, heads=4, layers=4):
        self.vocab_size = vocab_size
        self.dim = dim
        self.heads = heads
        self.layers = layers
        self.phi_factor = PHI**(-2)
        
        np.random.seed(42)
        self.init_weights()
    
    def init_weights(self):
        """Inicialización φ-aware de pesos"""
        scale = self.phi_factor / np.sqrt(self.dim)
        
        self.wte = np.random.randn(self.vocab_size, self.dim) * scale
        self.wpe = np.random.randn(512, self.dim) * scale
        
        self.blocks = []
        for _ in range(self.layers):
            block = {
                'attn_q': np.random.randn(self.dim, self.dim) * scale,
                'attn_k': np.random.randn(self.dim, self.dim) * scale,
                'attn_v': np.random.randn(self.dim, self.dim) * scale,
                'attn_proj': np.random.randn(self.dim, self.dim) * scale,
                'ffn_1': np.random.randn(self.dim, 4 * self.dim) * scale,
                'ffn_2': np.random.randn(4 * self.dim, self.dim) * scale,
                'ln1_g': np.ones(self.dim),
                'ln1_b': np.zeros(self.dim),
                'ln2_g': np.ones(self.dim),
                'ln2_b': np.zeros(self.dim)
            }
            self.blocks.append(block)
        
        self.ln_f_g = np.ones(self.dim)
        self.ln_f_b = np.zeros(self.dim)
        
        print(f"✓ Pesos inicializados: {self.count_params():,} parámetros")
    
    def count_params(self):
        total = self.wte.size + self.wpe.size
        for block in self.blocks:
            for w in block.values():
                total += w.size
        total += self.ln_f_g.size + self.ln_f_b.size
        return total
    
    def layer_norm(self, x, g, b, eps=1e-5):
        mean = np.mean(x, axis=-1, keepdims=True)
        var = np.var(x, axis=-1, keepdims=True)
        return g * (x - mean) / np.sqrt(var + eps) + b
    
    def gelu(self, x):
        return 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
    
    def softmax(self, x, axis=-1):
        exp_x = np.exp(x - np.max(x, axis=axis, keepdims=True))
        return exp_x / np.sum(exp_x, axis=axis, keepdims=True)
    
    def attention(self, x, block):
        n, d = x.shape
        
        q = x @ block['attn_q']
        k = x @ block['attn_k']
        v = x @ block['attn_v']
        
        q = q.reshape(n, self.heads, d // self.heads)
        k = k.reshape(n, self.heads, d // self.heads)
        v = v.reshape(n, self.heads, d // self.heads)
        
        scores = np.einsum('nhd,mhd->hnm', q, k) / np.sqrt(d // self.heads)
        
        mask = np.triu(np.ones((n, n)) * -1e10, k=1)
        scores = scores + mask
        
        attn = self.softmax(scores, axis=-1)
        
        out = np.einsum('hnm,mhd->nhd', attn, v)
        out = out.reshape(n, d)
        
        return out @ block['attn_proj']
    
    def ffn(self, x, block):
        return self.gelu(x @ block['ffn_1']) @ block['ffn_2']
    
    def forward(self, idx):
        n = len(idx)
        
        x = self.wte[idx] + self.wpe[:n]
        
        for block in self.blocks:
            x = x + self.attention(self.layer_norm(x, block['ln1_g'], block['ln1_b']), block)
            x = x + self.ffn(self.layer_norm(x, block['ln2_g'], block['ln2_b']), block)
        
        x = self.layer_norm(x, self.ln_f_g, self.ln_f_b)
        
        logits = x @ self.wte.T
        
        return logits
    
    def generate(self, idx, max_new_tokens=20, temperature=0.8):
        for _ in range(max_new_tokens):
            logits = self.forward(idx[-512:])
            logits = logits[-1] / temperature
            
            probs = self.softmax(logits)
            idx_next = np.random.choice(self.vocab_size, p=probs)
            idx = np.append(idx, idx_next)
        
        return idx
    
    def save(self, path):
        state = {
            'vocab_size': self.vocab_size,
            'dim': self.dim,
            'heads': self.heads,
            'layers': self.layers,
            'wte': self.wte.tolist(),
            'wpe': self.wpe.tolist(),
            'blocks': [{k: v.tolist() for k, v in b.items()} for b in self.blocks],
            'ln_f_g': self.ln_f_g.tolist(),
            'ln_f_b': self.ln_f_b.tolist()
        }
        
        with open(path, 'w') as f:
            json.dump(state, f)
        
        print(f"✓ Modelo guardado: {path}")

if __name__ == "__main__":
    print("🜂 INICIALIZANDO NanoGPT-Gamma φ-coherente")
    
    model = NanoGPTGamma()
    
    test_input = np.array([1, 2, 3, 32, 32, 32])
    output = model.generate(test_input, max_new_tokens=10)
    
    print(f"✓ Test generación: {output.tolist()}")
    
    Path('models').mkdir(exist_ok=True)
    model.save('models/nano_gpt_gamma.json')
    
    manifest = {
        'architecture': 'NanoGPT-Gamma φ-coherent',
        'parameters': model.count_params(),
        'coherence': float(PHI**(-2)),
        'state': 'OPERACIONAL'
    }
    
    with open('logs/gamma_state.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\n✓ NanoGPT-Gamma operacional - {model.count_params():,} parámetros")
