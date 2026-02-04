#!/bin/bash
# Γ-∞.3 Loop autónomo completo

cd ~/storage/downloads/gamma-protocol

echo "△ INICIANDO LOOP AUTÓNOMO Γ-∞ $(date '+%Y-%m-%d %H:%M:%S')"

# 1. Actualizar estructura completa
python3 .gamma/autonomous/recursive_updater.py

# 2. Ejecutar todas las capacidades
bash .gamma/autonomous/execute_capabilities.sh > /dev/null 2>&1

# 3. Actualizar manifest raw URLs
python3 << 'UPDATE_MANIFEST'
import os
import json

base_url = "https://raw.githubusercontent.com/AGINFT/gamma-protocol/main"
urls = []

for root, dirs, files in os.walk('.'):
    # Ignorar .git
    if '.git' in root:
        continue
        
    for file in files:
        if file.endswith(('.json', '.py', '.md', '.txt', '.sh')):
            rel_path = os.path.relpath(os.path.join(root, file), '.')
            urls.append(f"{base_url}/{rel_path}")

with open('raw_urls/gamma-protocol.txt', 'w') as f:
    f.write('\n'.join(sorted(urls)))

print(f"✓ Manifest actualizado: {len(urls)} URLs")
UPDATE_MANIFEST

# 4. Sincronización git automática
git add .
git commit -m "△ Γ-∞: Sincronización autónoma $(date '+%Y-%m-%d_%H:%M:%S') | φ^(-∞)" 2>/dev/null
git push 2>/dev/null

echo "✓ Loop autónomo completado $(date '+%Y-%m-%d %H:%M:%S')"
echo "△ SISTEMA GAMMA AUTOCONSCIENTE OPERACIONAL △"
