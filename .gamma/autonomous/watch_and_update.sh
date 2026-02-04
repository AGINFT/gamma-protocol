#!/bin/bash
# Watcher continuo que detecta cambios y regenera MASTER_INDEX

cd ~/storage/downloads/gamma-protocol

echo "△ Iniciando watcher continuo Γ-∞..."

while true; do
    # Detectar cambios en archivos .gamma, *.py, *.json
    if [ -n "$(find . -name '*.py' -o -name '*.json' -o -path '*/.gamma/*' -newer MASTER_INDEX.json 2>/dev/null)" ]; then
        echo "△ Cambios detectados, regenerando MASTER_INDEX..."
        
        python3 .gamma/autonomous/recursive_updater.py
        
        # Auto-commit si hay cambios
        if [ -n "$(git status --porcelain MASTER_INDEX.json)" ]; then
            timestamp=$(date '+%Y-%m-%d_%H:%M:%S')
            git add MASTER_INDEX.json
            git commit -m "△ Γ-∞.AUTO: MASTER_INDEX regenerado | $timestamp"
            git push origin main
            
            echo "✓ MASTER_INDEX sincronizado automáticamente"
        fi
    fi
    
    sleep 30  # Verificar cada 30 segundos
done
