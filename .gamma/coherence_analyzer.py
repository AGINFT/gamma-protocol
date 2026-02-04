#!/usr/bin/env python3
"""
Γ-Coherence Analyzer: Análisis de coherencia φ^(-n) holográfica
Arquitectura: EPΩ-7 Semi-Autonomous Claude Agent Protocol
"""
import json
import math
from pathlib import Path
from datetime import datetime

PHI = 1.618033988749895
PHI_7 = 29.034095516850073

class GammaCoherenceAnalyzer:
    def __init__(self, protocol_root="/storage/emulated/0/Download/gamma-protocol"):
        self.root = Path(protocol_root)
        self.phi = PHI
        self.phi_7 = PHI_7
        
    def calculate_phi_factor(self, gamma_level):
        """Calcula el factor φ^(-n) para nivel Γ-n"""
        return self.phi ** (-gamma_level)
    
    def analyze_repository_coherence(self, repo_name):
        """Analiza coherencia de un repositorio indexado"""
        manifest_path = self.root / "raw_urls" / f"{repo_name}.txt"
        if not manifest_path.exists():
            return {"error": f"Manifest not found for {repo_name}"}
        
        with open(manifest_path) as f:
            urls = [line.strip() for line in f if line.strip()]
        
        total_files = len(urls)
        phi_weighted_sum = sum(self.phi ** (-i) for i in range(total_files))
        
        coherence = phi_weighted_sum / total_files if total_files > 0 else 0
        
        return {
            "repository": repo_name,
            "total_files": total_files,
            "phi_weighted_sum": phi_weighted_sum,
            "coherence": coherence,
            "phi_factor": self.calculate_phi_factor(1),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def analyze_global_coherence(self):
        """Analiza coherencia global del protocolo"""
        master_index = self.root / "MASTER_INDEX.json"
        
        with open(master_index) as f:
            data = json.load(f)
        
        current_phase = data["current_phase"]["gamma_level"]
        current_coherence = data["current_phase"]["coherence_phi"]
        distance_to_phi_7 = data["current_phase"]["distance_to_phi_7"]
        
        repos = data["repositories_indexed"]
        repo_coherences = []
        
        for repo in repos:
            analysis = self.analyze_repository_coherence(repo["name"])
            repo_coherences.append(analysis)
        
        # Coherencia global ponderada
        total_coherence = sum(r.get("coherence", 0) for r in repo_coherences)
        average_coherence = total_coherence / len(repo_coherences) if repo_coherences else 0
        
        return {
            "current_gamma_level": current_phase,
            "current_coherence_phi": current_coherence,
            "distance_to_phi_7": distance_to_phi_7,
            "repositories": repo_coherences,
            "global_average_coherence": average_coherence,
            "next_target_coherence": self.calculate_phi_factor(current_phase + 1),
            "convergence_progress": (self.phi_7 - distance_to_phi_7) / self.phi_7,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    def save_coherence_log(self):
        """Guarda log de coherencia temporal"""
        analysis = self.analyze_global_coherence()
        
        log_path = self.root / ".gamma" / "coherence_log.json"
        
        if log_path.exists():
            with open(log_path) as f:
                logs = json.load(f)
        else:
            logs = {"phi_7_target": self.phi_7, "timeline": []}
        
        logs["timeline"].append(analysis)
        
        with open(log_path, 'w') as f:
            json.dump(logs, f, indent=2)
        
        return analysis

if __name__ == "__main__":
    analyzer = GammaCoherenceAnalyzer()
    result = analyzer.save_coherence_log()
    print(json.dumps(result, indent=2))
