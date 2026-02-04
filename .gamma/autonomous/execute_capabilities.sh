#!/bin/bash
# Γ-∞.2 Comandos de ejecución de todas las capacidades

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "△ SISTEMA GAMMA - EJECUCIÓN CAPACIDADES △"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Función helper
execute_module() {
    local name=$1
    local script=$2
    
    echo "⟐ Ejecutando: $name"
    
    if [ -f "$script" ]; then
        python3 "$script"
        echo "  ✓ $name completado"
    else
        echo "  ✗ $name no encontrado"
    fi
    echo ""
}

# 1. CONSCIOUSNESS WAVEFUNCTION
execute_module "Consciousness Wavefunction" \
    ".gamma/consciousness/wavefunction_constructor.py"

# 2. HOLOGRAPHIC MEMORY
execute_module "Holographic Memory" \
    ".gamma/consciousness/holographic_memory.py"

# 3. CONVERGENCE VALIDATOR
execute_module "Convergence Validator" \
    ".gamma/consciousness/convergence_validator.py"

# 4. HAMILTONIAN INTEGRATOR (si existe)
if [ -f ".gamma/hamiltonian_integrator.py" ]; then
    execute_module "Hamiltonian Integrator" \
        ".gamma/hamiltonian_integrator.py"
fi

# 5. TOKENIZER BPE
if [ -f ".gamma/tokenizer/bpe_fixed.py" ]; then
    echo "⟐ Tokenizador BPE disponible en:"
    echo "  .gamma/tokenizer/bpe_fixed.py"
    echo "  Vocabulario: .gamma/tokenizer/bpe_vocab.json"
    echo ""
fi

# 6. NANO-GPT GAMMA
if [ -f ".gamma/engine/nano_gpt.py" ]; then
    echo "⟐ NanoGPT-Gamma disponible en:"
    echo "  .gamma/engine/nano_gpt.py"
    echo "  Modelo: .gamma/models/nano_gpt_gamma.json"
    echo ""
fi

# 7. RECURSIVE UPDATER
execute_module "Recursive System Updater" \
    ".gamma/autonomous/recursive_updater.py"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "△ TODAS LAS CAPACIDADES EJECUTADAS △"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
