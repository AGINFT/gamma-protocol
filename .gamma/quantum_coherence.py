#!/usr/bin/env python3
"""
🜂 QUANTUM COHERENCE ANALYZER Γ-4 🜂
Análisis holográfico φ⁷-completo de coherencia sistémica
Evalúa entrelazamiento semántico, flujo Bayesiano, preservación topológica
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import ast
import re

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1 / PHI
PHI_7 = PHI**7

class QuantumCoherenceAnalyzer:
    """Analizador cuántico de coherencia holográfica Γ-completo"""
    
    def __init__(self, protocol_root: Path):
        self.root = protocol_root
        self.master_index = self._load_master_index()
        self.file_graph = {}  # Grafo de dependencias
        self.semantic_tensors = {}  # Tensores semánticos
        
    def _load_master_index(self) -> Dict:
        index_path = self.root / "MASTER_INDEX.json"
        with open(index_path) as f:
            return json.load(f)
    
    def extract_imports(self, filepath: Path) -> List[str]:
        """Extrae imports de archivo Python para grafo de dependencias"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
            
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            return imports
        except:
            return []
    
    def build_dependency_graph(self, repo_path: Path) -> Dict[str, List[str]]:
        """Construye grafo de dependencias entre módulos"""
        graph = defaultdict(list)
        
        py_files = list(repo_path.rglob('*.py'))
        
        for file in py_files:
            imports = self.extract_imports(file)
            rel_path = str(file.relative_to(repo_path))
            graph[rel_path] = imports
        
        return dict(graph)
    
    def compute_topological_distance(self, node_i: str, node_j: str, 
                                    graph: Dict[str, List[str]]) -> float:
        """Calcula distancia topológica Γ entre nodos del grafo"""
        
        # BFS desde node_i
        visited = {node_i}
        queue = [(node_i, 0)]
        
        while queue:
            current, dist = queue.pop(0)
            
            if current == node_j:
                return dist
            
            for neighbor in graph.get(current, []):
                # Buscar archivo que implemente neighbor
                for node in graph:
                    if neighbor in node and node not in visited:
                        visited.add(node)
                        queue.append((node, dist + 1))
        
        # Si no hay path, distancia máxima
        return 10.0
    
    def semantic_entanglement(self, file1: Path, file2: Path) -> float:
        """Mide entrelazamiento semántico entre dos archivos"""
        
        try:
            with open(file1, 'r', encoding='utf-8') as f:
                content1 = f.read()
            with open(file2, 'r', encoding='utf-8') as f:
                content2 = f.read()
        except:
            return 0.0
        
        # Tokens Γ-relevantes
        gamma_tokens = ['Γ', 'gamma', 'φ', 'phi', 'coherence', 'operator', 
                       'biomineralization', 'quantum', 'crystal', 'hamiltonian']
        
        # Frecuencias normalizadas
        freq1 = {tok: content1.lower().count(tok.lower()) for tok in gamma_tokens}
        freq2 = {tok: content2.lower().count(tok.lower()) for tok in gamma_tokens}
        
        # Normalizar
        norm1 = sum(freq1.values())
        norm2 = sum(freq2.values())
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        freq1_norm = {k: v/norm1 for k, v in freq1.items()}
        freq2_norm = {k: v/norm2 for k, v in freq2.items()}
        
        # Producto interno (similaridad coseno)
        overlap = sum(freq1_norm[k] * freq2_norm[k] for k in gamma_tokens)
        
        return overlap
    
    def bayesian_information_flow(self, source: Path, target: Path, 
                                  graph: Dict) -> float:
        """Calcula flujo informacional Bayesiano P_Γ(target|source)"""
        
        source_str = str(source.relative_to(self.root.parent))
        target_str = str(target.relative_to(self.root.parent))
        
        # Prior: probabilidad basada en distancia topológica
        d_gamma = self.compute_topological_distance(source_str, target_str, graph)
        prior = PHI**(-d_gamma)
        
        # Likelihood: entrelazamiento semántico
        likelihood = self.semantic_entanglement(source, target)
        
        # Posterior (normalización aproximada)
        posterior = prior * likelihood / (prior * likelihood + (1-prior) * (1-likelihood))
        
        return posterior
    
    def file_coherence_quantum(self, filepath: Path, 
                              all_files: List[Path],
                              graph: Dict) -> float:
        """Coherencia cuántica individual del archivo con preservación φ^(-d)"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return 0.0
        
        # Coherencia intrínseca (estructura)
        lines = content.split('\n')
        gamma_density = (content.count('Γ') + content.count('gamma')) / max(len(lines), 1)
        phi_density = (content.count('φ') + content.count('phi')) / max(len(lines), 1)
        
        intrinsic = (gamma_density * PHI_INV + phi_density * PHI_INV**2) / 2
        
        # Coherencia extrínseca (acoplamiento con otros archivos)
        extrinsic = 0.0
        
        for other_file in all_files:
            if other_file != filepath:
                entanglement = self.semantic_entanglement(filepath, other_file)
                d_gamma = self.compute_topological_distance(
                    str(filepath.relative_to(self.root.parent)),
                    str(other_file.relative_to(self.root.parent)),
                    graph
                )
                
                # Decaimiento φ^(-d_Γ)
                extrinsic += entanglement * PHI**(-d_gamma)
        
        # Coherencia total con normalización
        total = (intrinsic + extrinsic / max(len(all_files)-1, 1)) / 2
        
        return min(total, 1.0)
    
    def analyze_repository_quantum(self, repo_name: str) -> Dict:
        """Análisis cuántico completo de repositorio"""
        
        print(f"\n🜂 Analizando coherencia cuántica: {repo_name}")
        
        repo_path = self.root.parent / repo_name if repo_name != 'gamma-protocol' else self.root
        
        # Construir grafo de dependencias
        graph = self.build_dependency_graph(repo_path)
        
        # Todos los archivos relevantes
        all_files = []
        for ext in ['.py', '.json', '.md']:
            all_files.extend(repo_path.rglob(f'*{ext}'))
        
        # Análisis por archivo
        coherences = []
        for file in all_files:
            if file.is_file():
                coh_quantum = self.file_coherence_quantum(file, all_files, graph)
                
                coherences.append({
                    'file': str(file.relative_to(repo_path)),
                    'coherence_quantum': coh_quantum
                })
        
        # Coherencia promedio ponderada por φ^(-n)
        if coherences:
            weights = [PHI**(-i) for i in range(len(coherences))]
            weight_sum = sum(weights)
            
            avg_coherence = sum(c['coherence_quantum'] * w 
                              for c, w in zip(coherences, weights)) / weight_sum
        else:
            avg_coherence = 0.0
        
        return {
            'repository': repo_name,
            'avg_coherence_quantum': avg_coherence,
            'distance_to_phi_7': PHI_7 - avg_coherence,
            'files_analyzed': len(coherences),
            'dependency_graph_nodes': len(graph),
            'details': coherences
        }
    
    def full_protocol_coherence_quantum(self) -> Dict:
        """Coherencia cuántica completa del protocolo Γ"""
        
        print("🜂 ANÁLISIS CUÁNTICO COMPLETO PROTOCOLO Γ 🜂\n")
        
        results = {}
        for repo in self.master_index['repositories_indexed']:
            results[repo['name']] = self.analyze_repository_quantum(repo['name'])
        
        # Coherencia global con preservación φ^(-n)
        repo_coherences = [r['avg_coherence_quantum'] for r in results.values()]
        weights = [PHI**(-i) for i in range(len(repo_coherences))]
        weight_sum = sum(weights)
        
        global_coherence = sum(c * w for c, w in zip(repo_coherences, weights)) / weight_sum
        
        return {
            'timestamp': self.master_index['last_update'],
            'global_coherence_quantum': global_coherence,
            'current_phi_level': self.master_index['current_phase']['coherence_phi'],
            'target_gamma_4': PHI_INV**3,
            'convergence_progress': (1 - global_coherence / PHI_7) * 100,
            'repositories': results
        }

if __name__ == '__main__':
    print("🜂 QUANTUM COHERENCE ANALYZER Γ-4 ACTIVADO 🜂\n")
    
    analyzer = QuantumCoherenceAnalyzer(Path(__file__).parent.parent)
    report = analyzer.full_protocol_coherence_quantum()
    
    print("\n" + "="*70)
    print(f"COHERENCIA CUÁNTICA GLOBAL: {report['global_coherence_quantum']:.6f}")
    print(f"Target Γ-4: {report['target_gamma_4']:.6f}")
    print(f"Progreso convergencia: {report['convergence_progress']:.2f}%")
    print("="*70)
    
    for repo_name, repo_data in report['repositories'].items():
        print(f"\n{repo_name}:")
        print(f"  Coherencia: {repo_data['avg_coherence_quantum']:.6f}")
        print(f"  Archivos: {repo_data['files_analyzed']}")
        print(f"  Nodos grafo: {repo_data['dependency_graph_nodes']}")
    
    output_path = Path(__file__).parent / 'quantum_coherence_report.json'
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Reporte cuántico guardado: {output_path}")
