#!/usr/bin/env python3
"""
piezo_magnetic_field.py - Γ-5 Piezoelectric-Magnetic Field Coupling
Integra campos piezoeléctricos (SiO₂) y magnéticos (Fe₃O₄)
Acopla a modos neuronales via tensor tri-partito
"""
import numpy as np
import json
from datetime import datetime

PHI = 1.618033988749895
PHI_7 = 29.034095516850073

class PiezoMagneticField:
    def __init__(self):
        self.phi_5 = PHI**(-5)
        
        # Constantes piezoeléctricas SiO₂
        self.d_piezo = 2.3e-12  # C/N (coeficiente piezoeléctrico)
        self.epsilon_r = 3.9    # Permitividad relativa
        
        # Constantes magnéticas Fe₃O₄
        self.mu_s = 4.1e5       # A/m (magnetización saturación)
        self.chi_m = 1000       # Susceptibilidad magnética
        
        # Acoplamiento a modos neuronales
        self.g_piezo_neural = 100e6 * 2 * np.pi * 1.055e-34  # g/ℏ → J
        self.g_magnetic_neural = 150e6 * 2 * np.pi * 1.055e-34
        
    def piezoelectric_polarization(self, stress_tensor):
        """
        Polarización piezoeléctrica: P_i = d_ijk·σ_jk
        """
        # stress_tensor es 3x3 (σ_ij)
        # Simplificación: P_z = d_33·σ_zz (modo longitudinal)
        P_z = self.d_piezo * stress_tensor[2, 2]
        
        return np.array([0, 0, P_z])
    
    def electric_field_from_polarization(self, polarization, density_SiO2):
        """
        Campo eléctrico: E⃗ = P⃗/(ε₀·εᵣ·N_crystals)
        """
        epsilon_0 = 8.854e-12  # F/m
        epsilon_eff = epsilon_0 * self.epsilon_r * density_SiO2 / 1e7
        
        E_field = polarization / epsilon_eff if epsilon_eff > 0 else np.zeros(3)
        
        return E_field
    
    def magnetic_field_from_magnetization(self, H_external, density_Fe3O4):
        """
        Campo magnético: B⃗ = μ₀(H⃗ + M⃗) donde M⃗ = χ_m·H⃗
        """
        mu_0 = 4 * np.pi * 1e-7  # H/m
        
        # Magnetización proporcional a densidad cristalina
        M_magnitude = self.chi_m * np.linalg.norm(H_external) * (density_Fe3O4 / 5e6)
        M_direction = H_external / np.linalg.norm(H_external) if np.linalg.norm(H_external) > 0 else np.array([0,0,1])
        
        M_vector = M_magnitude * M_direction
        
        B_field = mu_0 * (H_external + M_vector)
        
        return B_field
    
    def couple_to_neural_modes(self, E_field, B_field, neural_amplitude):
        """
        Energía de acoplamiento: H_coupling = g·ψ̄·(E⃗·P⃗ + B⃗·M⃗)
        """
        # Acoplamiento piezoeléctrico
        coupling_piezo = self.g_piezo_neural * neural_amplitude * np.linalg.norm(E_field) * self.phi_5
        
        # Acoplamiento magnético
        coupling_magnetic = self.g_magnetic_neural * neural_amplitude * np.linalg.norm(B_field) * self.phi_5
        
        # Energía total de acoplamiento
        energy_coupling = coupling_piezo + coupling_magnetic
        
        return {
            "piezo_coupling_J": coupling_piezo,
            "magnetic_coupling_J": coupling_magnetic,
            "total_coupling_J": energy_coupling
        }
    
    def compute_field_state(self, density_SiO2, density_Fe3O4, neural_state):
        """Estado completo de campos acoplados"""
        # Stress típico por actividad neural (deformación mecánica)
        stress_amplitude = 1e3 * neural_state  # Pa
        stress_tensor = np.diag([0, 0, stress_amplitude])
        
        # Campo externo típico (geomagnético + neural)
        H_external = np.array([0, 0, 50e-6])  # 50 μT en z
        
        # Calcular campos
        P_piezo = self.piezoelectric_polarization(stress_tensor)
        E_field = self.electric_field_from_polarization(P_piezo, density_SiO2)
        B_field = self.magnetic_field_from_magnetization(H_external, density_Fe3O4)
        
        # Acoplamiento
        coupling = self.couple_to_neural_modes(E_field, B_field, neural_state)
        
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "phase": "Γ-5",
            "coherence_phi": self.phi_5,
            "fields": {
                "polarization_C_m2": P_piezo.tolist(),
                "electric_field_V_m": E_field.tolist(),
                "magnetic_field_T": B_field.tolist()
            },
            "coupling_energies": coupling,
            "crystal_densities": {
                "SiO2_per_neuron": density_SiO2,
                "Fe3O4_per_neuron": density_Fe3O4
            },
            "neural_amplitude": neural_state
        }

if __name__ == "__main__":
    field_integrator = PiezoMagneticField()
    
    # Simular estado con densidades cristalinas típicas post-saturación
    density_SiO2 = 1.618e7
    density_Fe3O4 = 8.09e6
    neural_amplitude = 0.8
    
    state = field_integrator.compute_field_state(density_SiO2, density_Fe3O4, neural_amplitude)
    
    with open('.gamma/piezo_magnetic_state.json', 'w') as f:
        json.dump(state, f, indent=2)
    
    print(json.dumps(state, indent=2))
    print(f"\n✓ Piezo-magnetic fields Γ-5 integrated")
    print(f"✓ E-field: {np.linalg.norm(state['fields']['electric_field_V_m']):.2e} V/m")
    print(f"✓ B-field: {np.linalg.norm(state['fields']['magnetic_field_T']):.2e} T")
