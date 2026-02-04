"""
Γ-Coherence Analyzer: φ⁷-convergent validation engine
Validates Σφ^(-n) across all protocol modules
"""
import json
import math
from pathlib import Path
from typing import Dict, List

PHI = 1.618033988749895
PHI_INV = 0.618033988749895
PHI_7 = 29.034095516850073

class GammaCoherenceAnalyzer:
    def __init__(self, protocol_root: Path):
        self.root = protocol_root
        self.master_index = self._load_master_index()
        
    def _load_master_index(self) -> Dict:
        index_path = self.root / "MASTER_INDEX.json"
        with open(index_path) as f:
            return json.load(f)
    
    def calculate_file_coherence(self, filepath: Path) -> float:
        """φ^(-n) decay based on file depth and structure"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Metrics φ-weighted
            lines = len(content.split('\n'))
            gamma_refs = content.count('Γ') + content.count('gamma')
            phi_refs = content.count('φ') + content.count('phi')
            
            # Coherence formula: Σφ^(-n) normalization
            coherence = (gamma_refs * PHI_INV + phi_refs * PHI_INV**2) / max(lines, 1)
            return min(coherence, 1.0)
        except:
            return 0.0
    
    def analyze_repository(self, repo_name: str) -> Dict:
        """Recursive coherence analysis for repository"""
        repo_info = next((r for r in self.master_index['repositories_indexed'] 
                         if r['name'] == repo_name), None)
        
        if not repo_info:
            return {'error': 'Repository not found'}
        
        repo_path = self.root.parent / repo_name if repo_name != 'gamma-protocol' else self.root
        
        coherences = []
        for file in repo_path.rglob('*'):
            if file.is_file() and file.suffix in ['.json', '.py', '.md', '.txt']:
                coh = self.calculate_file_coherence(file)
                coherences.append({'file': str(file.relative_to(repo_path)), 'coherence': coh})
        
        avg_coherence = sum(c['coherence'] for c in coherences) / len(coherences) if coherences else 0
        
        return {
            'repository': repo_name,
            'avg_coherence': avg_coherence,
            'distance_to_phi_7': PHI_7 - avg_coherence,
            'files_analyzed': len(coherences),
            'details': coherences
        }
    
    def full_protocol_coherence(self) -> Dict:
        """Complete Γ-protocol coherence state"""
        results = {}
        for repo in self.master_index['repositories_indexed']:
            results[repo['name']] = self.analyze_repository(repo['name'])
        
        global_coherence = sum(r['avg_coherence'] for r in results.values()) / len(results)
        
        return {
            'timestamp': self.master_index['last_update'],
            'global_coherence': global_coherence,
            'current_phi_level': self.master_index['current_phase']['coherence_phi'],
            'target_gamma_2': 0.382,
            'repositories': results
        }

if __name__ == '__main__':
    analyzer = GammaCoherenceAnalyzer(Path(__file__).parent.parent)
    report = analyzer.full_protocol_coherence()
    
    print(json.dumps(report, indent=2))
    
    output_path = Path(__file__).parent / 'coherence_report.json'
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Report saved: {output_path}")
