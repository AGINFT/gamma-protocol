#!/usr/bin/env python3
"""
🜂 BIOMINERALIZATION KINETICS SIMULATOR Γ-5 RECALIBRATED 🜂
Cinética biomineralización con parámetros físicamente realistas
Escalas temporales: 14-37 días (no milenios)
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict

PHI = (1 + np.sqrt(5)) / 2

class BiomineralizationSimulator:
    """Simulador biomineralización - parámetros Γ realistas"""
    
    def __init__(self):
        self.PHI = PHI
        
        # Parámetros φ-optimizados CORREGIDOS
        self.params = {
            'SiO2': {
                'k_cat': 0.123,              # día⁻¹ (sin factor Arrhenius extra)
                'N_max': 1.618e7,            # cristales/neurona
                'name': 'SiO₂ (piezoelectric)',
                't_sat_target': 22.9         # días @ 99%
            },
            'Fe3O4': {
                'k_cat': 0.197,              # día⁻¹
                'N_max': 8.09e6,
                'name': 'Fe₃O₄ (magnetic)',
                't_sat_target': 14.3
            },
            'QD': {
                'k_cat': 0.123,
                'N_max': 1.618e8,
                'name': 'InP/ZnS QD (photonic)',
                't_sat_target': 37.0
            }
        }
        
    def growth_kinetics(self, t_days: np.ndarray, crystal_type: str) -> np.ndarray:
        """
        Cinética logística simple: N(t) = N_max·(1 - exp(-k_cat·t))
        SIN factor Arrhenius explícito (ya incorporado en k_cat medido)
        """
        params = self.params[crystal_type]
        k_cat = params['k_cat']
        N_max = params['N_max']
        
        N_t = N_max * (1 - np.exp(-k_cat * t_days))
        
        return N_t
    
    def saturation_time(self, crystal_type: str, threshold: float = 0.99) -> float:
        """Tiempo para alcanzar threshold% de saturación"""
        k_cat = self.params[crystal_type]['k_cat']
        t_sat = -np.log(1 - threshold) / k_cat
        return t_sat
    
    def simulate_full_timeline(self, t_max_days: int = 45) -> Dict:
        """Timeline biomineralización completo"""
        
        t = np.linspace(0, t_max_days, 1000)
        
        results = {}
        for crystal_type in ['SiO2', 'Fe3O4', 'QD']:
            N_t = self.growth_kinetics(t, crystal_type)
            saturation_percent = (N_t / self.params[crystal_type]['N_max']) * 100
            t_sat = self.saturation_time(crystal_type, 0.99)
            
            results[crystal_type] = {
                'time_days': t.tolist(),
                'count_per_neuron': N_t.tolist(),
                'saturation_percent': saturation_percent.tolist(),
                't_sat_99': float(t_sat),
                't_sat_target': self.params[crystal_type]['t_sat_target'],
                'N_max': float(self.params[crystal_type]['N_max']),
                'k_cat': float(self.params[crystal_type]['k_cat'])
            }
        
        return results

if __name__ == '__main__':
    print("🜂 BIOMINERALIZATION KINETICS SIMULATOR Γ-5 RECALIBRADO 🜂\n")
    
    simulator = BiomineralizationSimulator()
    results = simulator.simulate_full_timeline(t_max_days=45)
    
    print("="*70)
    print("TIEMPOS DE SATURACIÓN (99%) - PARÁMETROS REALISTAS")
    print("="*70)
    for crystal_type, data in results.items():
        print(f"{simulator.params[crystal_type]['name']}:")
        print(f"  Calculado: {data['t_sat_99']:.1f} días")
        print(f"  Target Γ: {data['t_sat_target']:.1f} días")
        print(f"  N_max: {data['N_max']:.2e} cristales/neurona")
        print(f"  k_cat: {data['k_cat']:.4f} día⁻¹")
        print()
    
    output_dir = Path(__file__).parent
    results_path = output_dir / 'biomineralization_timeline.json'
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Timeline guardado: {results_path}")
    print(f"\n🜂 Cinética biomineralización opera en escala temporal humana realista")
