#!/usr/bin/env python3
"""
🜂 BIOMINERALIZATION KINETICS SIMULATOR Γ-5 🜂
Simulador de cinética de biomineralización holográfica
Modela crecimiento de SiO₂, Fe₃O₄, QD con saturación temporal realista
"""

import json
import numpy as np
from pathlib import Path
from typing import Dict, List
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt

PHI = (1 + np.sqrt(5)) / 2

class BiomineralizationSimulator:
    """Simulador de cinética biocrystalina con parámetros Γ-optimizados"""
    
    def __init__(self):
        self.PHI = PHI
        
        # Parámetros cinéticos φ-optimizados
        self.params = {
            'SiO2': {
                'k_cat': 0.05 * PHI**(-2),  # = 0.123 día⁻¹
                'N_max': 1e7 * PHI,          # = 1.618×10⁷ /neurona
                'E_a': 45000 * PHI**(-1),    # = 27.8 kJ/mol
                'name': 'SiO₂ (piezoelectric)'
            },
            'Fe3O4': {
                'k_cat': 0.08 * PHI**(-2),  # = 0.197 día⁻¹
                'N_max': 5e6 * PHI,          # = 8.09×10⁶ /neurona
                'E_a': 45000 * PHI**(-1),
                'name': 'Fe₃O₄ (magnetic)'
            },
            'QD': {
                'k_cat': 0.05 * PHI**(-2),
                'N_max': 1e8 * PHI,          # = 1.618×10⁸ /neurona
                'E_a': 30000 * PHI**(-1),
                'name': 'InP/ZnS QD (photonic)'
            }
        }
        
        self.T = 310.15  # 37°C en Kelvin
        self.k_B = 1.38e-23  # J/K
        self.R = 8.314  # J/(mol·K)
        
    def growth_kinetics(self, t_days: np.ndarray, crystal_type: str) -> np.ndarray:
        """
        Cinética de crecimiento: N(t) = N_max·(1 - exp(-k_cat·t))
        """
        params = self.params[crystal_type]
        k_cat = params['k_cat']
        N_max = params['N_max']
        E_a = params['E_a']
        
        # Factor de Arrhenius
        arrhenius = np.exp(-E_a / (self.R * self.T))
        k_eff = k_cat * arrhenius
        
        # Crecimiento logístico
        N_t = N_max * (1 - np.exp(-k_eff * t_days))
        
        return N_t
    
    def saturation_time(self, crystal_type: str, threshold: float = 0.99) -> float:
        """Tiempo para alcanzar threshold% de saturación"""
        params = self.params[crystal_type]
        k_cat = params['k_cat']
        E_a = params['E_a']
        
        arrhenius = np.exp(-E_a / (self.R * self.T))
        k_eff = k_cat * arrhenius
        
        t_sat = -np.log(1 - threshold) / k_eff
        
        return t_sat
    
    def simulate_full_timeline(self, t_max_days: int = 40) -> Dict:
        """Simula timeline completo de biomineralización"""
        
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
                'N_max': float(self.params[crystal_type]['N_max']),
                'k_cat': float(self.params[crystal_type]['k_cat'])
            }
        
        return results
    
    def plot_growth_curves(self, results: Dict, output_dir: Path):
        """Genera gráficas de cinética"""
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Crecimiento absoluto
        ax1 = axes[0]
        for crystal_type, data in results.items():
            t = np.array(data['time_days'])
            N = np.array(data['count_per_neuron'])
            ax1.plot(t, N, label=self.params[crystal_type]['name'], linewidth=2)
            
            # Marcar t_sat
            t_sat = data['t_sat_99']
            N_sat = self.params[crystal_type]['N_max'] * 0.99
            ax1.plot(t_sat, N_sat, 'o', markersize=8)
        
        ax1.set_xlabel('Tiempo (días)', fontsize=12)
        ax1.set_ylabel('Cristales por neurona', fontsize=12)
        ax1.set_title('Cinética Biomineralización Holográfica Γ', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # Plot 2: Saturación %
        ax2 = axes[1]
        for crystal_type, data in results.items():
            t = np.array(data['time_days'])
            sat = np.array(data['saturation_percent'])
            ax2.plot(t, sat, label=self.params[crystal_type]['name'], linewidth=2)
            
            # Línea 99%
            ax2.axhline(99, color='red', linestyle='--', alpha=0.5)
        
        ax2.set_xlabel('Tiempo (días)', fontsize=12)
        ax2.set_ylabel('Saturación (%)', fontsize=12)
        ax2.set_title('Progreso de Saturación', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 105])
        
        plt.tight_layout()
        
        plot_path = output_dir / 'biomineralization_kinetics.png'
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"✓ Gráfica guardada: {plot_path}")
        
        return plot_path

if __name__ == '__main__':
    print("🜂 BIOMINERALIZATION KINETICS SIMULATOR Γ-5 ACTIVADO 🜂\n")
    
    simulator = BiomineralizationSimulator()
    
    # Simular timeline completo
    results = simulator.simulate_full_timeline(t_max_days=40)
    
    print("="*70)
    print("TIEMPOS DE SATURACIÓN (99%)")
    print("="*70)
    for crystal_type, data in results.items():
        print(f"{simulator.params[crystal_type]['name']}: {data['t_sat_99']:.1f} días")
        print(f"  N_max: {data['N_max']:.2e} cristales/neurona")
        print(f"  k_cat: {data['k_cat']:.4f} día⁻¹")
        print()
    
    # Guardar resultados
    output_dir = Path(__file__).parent
    results_path = output_dir / 'biomineralization_timeline.json'
    
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"✓ Timeline guardado: {results_path}")
    
    # Generar gráficas
    try:
        plot_path = simulator.plot_growth_curves(results, output_dir)
    except Exception as e:
        print(f"⚠ No se pudo generar gráfica: {e}")
