#!/usr/bin/env python3
"""
biomineralization_kinetics.py - Γ-5 Crystal Growth Temporal Dynamics
Simula crecimiento SiO₂-Fe₃O₄-QD con ecuaciones diferenciales acopladas
Modela transporte iónico, saturación enzimática y retroalimentación Γ
"""
import numpy as np
import json
from datetime import datetime
from scipy.integrate import odeint

PHI = 1.618033988749895
PHI_7 = 29.034095516850073

class BiomineralizationKinetics:
    def __init__(self):
        self.phi_5 = PHI**(-5)  # 0.090
        
        # Parámetros cinéticos Γ-modulados
        self.k_cat_silicatein = 0.05 * PHI**(-2)  # 0.123 día⁻¹
        self.k_cat_ferritin = 0.08 * PHI**(-2)    # 0.197 día⁻¹
        self.k_cat_qdot = 0.06 * PHI**(-2)        # 0.148 día⁻¹
        
        # Capacidades máximas Γ-amplificadas
        self.N_max_SiO2 = 1e7 * PHI              # 1.618×10⁷ /neurona
        self.N_max_Fe3O4 = 5e6 * PHI             # 8.09×10⁶ /neurona
        self.N_max_QD = 1e8 * PHI                # 1.618×10⁸ /neurona
        
        # Energías de activación Γ-optimizadas
        self.E_a_SiO2 = 45000 * PHI_INV          # 27.8 kJ/mol
        self.E_a_Fe3O4 = 48000 * PHI_INV         # 29.7 kJ/mol
        self.E_a_QD = 42000 * PHI_INV            # 26.0 kJ/mol
        
        # Temperatura fisiológica
        self.T = 310.15  # K (37°C)
        self.R = 8.314   # J/(mol·K)
        
        # Concentraciones iniciales enzimáticas
        self.enzyme_silicatein = 1.0  # μM
        self.enzyme_ferritin = 1.0    # μM
        self.enzyme_qdot_ligase = 0.8 # μM
        
        # Sustratos iónicos
        self.Si_substrate = 10.0   # mM silicato
        self.Fe_substrate = 5.0    # mM Fe²⁺
        self.InP_substrate = 2.0   # mM precursor QD
        
    def arrhenius_factor(self, E_a):
        """Factor de Arrhenius exp[-E_a/RT]"""
        return np.exp(-E_a / (self.R * self.T))
    
    def growth_rate_SiO2(self, N_SiO2, t):
        """
        Tasa crecimiento SiO₂:
        dN/dt = k_cat·[E]·[S]·(1 - N/N_max)·exp[-E_a/RT]·Ψ_Γ(t)
        """
        saturation = 1 - N_SiO2 / self.N_max_SiO2
        if saturation < 0:
            saturation = 0
        
        arrhenius = self.arrhenius_factor(self.E_a_SiO2)
        
        # Modulación Γ-holográfica: incorpora oscilación de modos Γ
        omega_gamma = 2 * np.pi * 40  # Hz
        psi_gamma_modulation = 1 + 0.1 * np.cos(omega_gamma * t * 86400)  # t en días
        
        rate = (self.k_cat_silicatein * 
                self.enzyme_silicatein * 
                self.Si_substrate * 
                saturation * 
                arrhenius * 
                psi_gamma_modulation)
        
        return rate
    
    def growth_rate_Fe3O4(self, N_Fe3O4, t):
        """Tasa crecimiento magnetita Fe₃O₄"""
        saturation = 1 - N_Fe3O4 / self.N_max_Fe3O4
        if saturation < 0:
            saturation = 0
        
        arrhenius = self.arrhenius_factor(self.E_a_Fe3O4)
        
        # Modulación magnética: Fe₃O₄ responde a campo externo
        B_external = 0.05  # Tesla (campo magnético cerebral típico ~50 μT)
        magnetic_enhancement = 1 + 0.05 * B_external * PHI**(-3)
        
        rate = (self.k_cat_ferritin * 
                self.enzyme_ferritin * 
                self.Fe_substrate * 
                saturation * 
                arrhenius * 
                magnetic_enhancement)
        
        return rate
    
    def growth_rate_QD(self, N_QD, t):
        """Tasa crecimiento quantum dots InP/ZnS"""
        saturation = 1 - N_QD / self.N_max_QD
        if saturation < 0:
            saturation = 0
        
        arrhenius = self.arrhenius_factor(self.E_a_QD)
        
        # Modulación fotónica: QD responde a iluminación neural
        photon_flux = 1e15  # fotones/s típico en corteza activa
        photonic_coupling = 1 + 0.08 * np.log10(photon_flux / 1e14)
        
        rate = (self.k_cat_qdot * 
                self.enzyme_qdot_ligase * 
                self.InP_substrate * 
                saturation * 
                arrhenius * 
                photonic_coupling)
        
        return rate
    
    def coupled_growth_equations(self, state, t):
        """
        Sistema acoplado de EDOs para crecimiento tri-cristal:
        dN_SiO2/dt = f_SiO2(N_SiO2, N_Fe3O4, N_QD, t)
        dN_Fe3O4/dt = f_Fe3O4(N_SiO2, N_Fe3O4, N_QD, t)
        dN_QD/dt = f_QD(N_SiO2, N_Fe3O4, N_QD, t)
        
        Acoplamiento: cristales se influencian mutuamente vía campos
        """
        N_SiO2, N_Fe3O4, N_QD = state
        
        # Tasas base individuales
        r_SiO2 = self.growth_rate_SiO2(N_SiO2, t)
        r_Fe3O4 = self.growth_rate_Fe3O4(N_Fe3O4, t)
        r_QD = self.growth_rate_QD(N_QD, t)
        
        # Acoplamiento inter-cristal con factores φ
        # SiO₂ piezoeléctrico estimula Fe₃O₄ magnético
        piezo_to_magnetic = 0.02 * (N_SiO2 / self.N_max_SiO2) * PHI**(-2)
        
        # Fe₃O₄ magnético orienta QD fotónicos
        magnetic_to_photonic = 0.03 * (N_Fe3O4 / self.N_max_Fe3O4) * PHI**(-2)
        
        # QD fotónicos retroalimentan SiO₂ (fotoactivación)
        photonic_to_piezo = 0.01 * (N_QD / self.N_max_QD) * PHI**(-3)
        
        # EDOs acopladas
        dN_SiO2_dt = r_SiO2 * (1 + photonic_to_piezo)
        dN_Fe3O4_dt = r_Fe3O4 * (1 + piezo_to_magnetic)
        dN_QD_dt = r_QD * (1 + magnetic_to_photonic)
        
        return [dN_SiO2_dt, dN_Fe3O4_dt, dN_QD_dt]
    
    def simulate_growth(self, t_days=50, dt=0.1):
        """Simula crecimiento temporal hasta saturación"""
        t_span = np.arange(0, t_days, dt)
        
        # Condiciones iniciales (pequeñas semillas)
        N0 = [1e4, 5e3, 1e5]  # Núcleos de cristalización iniciales
        
        # Integrar EDOs
        solution = odeint(self.coupled_growth_equations, N0, t_span)
        
        N_SiO2_t = solution[:, 0]
        N_Fe3O4_t = solution[:, 1]
        N_QD_t = solution[:, 2]
        
        # Detectar tiempo de saturación (95% de N_max)
        sat_threshold = 0.95
        
        t_sat_SiO2 = t_span[np.where(N_SiO2_t >= sat_threshold * self.N_max_SiO2)[0][0]] \
                     if any(N_SiO2_t >= sat_threshold * self.N_max_SiO2) else t_days
        t_sat_Fe3O4 = t_span[np.where(N_Fe3O4_t >= sat_threshold * self.N_max_Fe3O4)[0][0]] \
                      if any(N_Fe3O4_t >= sat_threshold * self.N_max_Fe3O4) else t_days
        t_sat_QD = t_span[np.where(N_QD_t >= sat_threshold * self.N_max_QD)[0][0]] \
                   if any(N_QD_t >= sat_threshold * self.N_max_QD) else t_days
        
        return {
            "time_days": t_span.tolist(),
            "N_SiO2": N_SiO2_t.tolist(),
            "N_Fe3O4": N_Fe3O4_t.tolist(),
            "N_QD": N_QD_t.tolist(),
            "saturation_times": {
                "SiO2_days": float(t_sat_SiO2),
                "Fe3O4_days": float(t_sat_Fe3O4),
                "QD_days": float(t_sat_QD)
            },
            "final_densities": {
                "SiO2_per_neuron": float(N_SiO2_t[-1]),
                "Fe3O4_per_neuron": float(N_Fe3O4_t[-1]),
                "QD_per_neuron": float(N_QD_t[-1])
            }
        }
    
    def generate_kinetics_report(self):
        """Genera reporte completo de cinética Γ-5"""
        simulation = self.simulate_growth(t_days=50, dt=0.1)
        
        report = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "phase": "Γ-5",
            "coherence_phi": self.phi_5,
            "kinetic_parameters": {
                "k_cat_silicatein_per_day": self.k_cat_silicatein,
                "k_cat_ferritin_per_day": self.k_cat_ferritin,
                "k_cat_qdot_per_day": self.k_cat_qdot,
                "E_a_SiO2_kJ_mol": self.E_a_SiO2 / 1000,
                "E_a_Fe3O4_kJ_mol": self.E_a_Fe3O4 / 1000,
                "E_a_QD_kJ_mol": self.E_a_QD / 1000
            },
            "saturation_times": simulation["saturation_times"],
            "final_crystal_densities": simulation["final_densities"],
            "simulation_data": {
                "time_span_days": [simulation["time_days"][0], simulation["time_days"][-1]],
                "data_points": len(simulation["time_days"])
            }
        }
        
        return report, simulation

PHI_INV = PHI**(-1)

if __name__ == "__main__":
    kinetics = BiomineralizationKinetics()
    report, simulation = kinetics.generate_kinetics_report()
    
    with open('.gamma/biomineralization_kinetics_state.json', 'w') as f:
        json.dump({
            "report": report,
            "full_simulation": simulation
        }, f, indent=2)
    
    print(json.dumps(report, indent=2))
    print(f"\n✓ Biomineralization kinetics Γ-5 simulated")
    print(f"✓ SiO₂ saturation: {report['saturation_times']['SiO2_days']:.1f} days")
    print(f"✓ Fe₃O₄ saturation: {report['saturation_times']['Fe3O4_days']:.1f} days")
    print(f"✓ QD saturation: {report['saturation_times']['QD_days']:.1f} days")
