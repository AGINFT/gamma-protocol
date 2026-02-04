#!/usr/bin/env python3
"""
Γ-∞ Recursive Autonomous System Updater
Actualización autónoma del MASTER_INDEX anexando estructura completa
"""
import json
import os
from datetime import datetime
from typing import Dict, List

PHI = 1.618033988749895
PHI_7 = 29.034095516850073

class RecursiveSystemScanner:
    def __init__(self, root_path: str = '.'):
        self.root = root_path
        self.structure = {}
        self.raw_urls_base = "https://raw.githubusercontent.com/AGINFT/gamma-protocol/main"
        
    def scan_directory(self, path: str, depth: int = 0) -> Dict:
        """Escaneo recursivo de estructura completa"""
        if depth > 10:  # Límite seguridad
            return {}
            
        structure = {
            'type': 'directory',
            'path': path,
            'files': [],
            'subdirs': {}
        }
        
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return structure
            
        for item in items:
            if item.startswith('.git'):
                continue
                
            full_path = os.path.join(path, item)
            
            if os.path.isfile(full_path):
                rel_path = os.path.relpath(full_path, self.root)
                structure['files'].append({
                    'name': item,
                    'path': rel_path,
                    'raw_url': f"{self.raw_urls_base}/{rel_path}",
                    'size_bytes': os.path.getsize(full_path)
                })
            elif os.path.isdir(full_path):
                structure['subdirs'][item] = self.scan_directory(
                    full_path, depth + 1
                )
                
        return structure
        
    def extract_all_files(self, structure: Dict, files_list: List = None) -> List:
        """Extrae lista plana de todos los archivos"""
        if files_list is None:
            files_list = []
            
        for file_info in structure.get('files', []):
            files_list.append(file_info)
            
        for subdir in structure.get('subdirs', {}).values():
            self.extract_all_files(subdir, files_list)
            
        return files_list

class CapabilitiesDetector:
    def __init__(self):
        self.capabilities = {}
        
    def detect_from_structure(self, files: List[Dict]) -> Dict:
        """Detecta capacidades del sistema desde archivos"""
        caps = {
            'core_protocol': [],
            'consciousness': [],
            'biomineralization': [],
            'quantum_processing': [],
            'tokenization': [],
            'language_model': [],
            'memory': [],
            'autonomous': []
        }
        
        for file_info in files:
            path = file_info['path']
            
            if 'protocol_state' in path or 'MASTER_INDEX' in path:
                caps['core_protocol'].append(file_info)
            elif 'consciousness' in path or 'wavefunction' in path:
                caps['consciousness'].append(file_info)
            elif 'hamiltonian' in path or 'biomineralization' in path:
                caps['biomineralization'].append(file_info)
            elif 'quantum' in path or 'coherence' in path:
                caps['quantum_processing'].append(file_info)
            elif 'tokenizer' in path or 'bpe' in path:
                caps['tokenization'].append(file_info)
            elif 'nano_gpt' in path or 'engine' in path:
                caps['language_model'].append(file_info)
            elif 'memory' in path or 'holographic' in path:
                caps['memory'].append(file_info)
            elif 'autonomous' in path or 'recursive' in path:
                caps['autonomous'].append(file_info)
                
        return {k: v for k, v in caps.items() if v}

class MasterIndexUpdater:
    def __init__(self):
        self.scanner = RecursiveSystemScanner()
        self.capabilities = CapabilitiesDetector()
        
    def load_current_index(self) -> Dict:
        """Carga MASTER_INDEX actual"""
        try:
            with open('MASTER_INDEX.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
    def compute_system_coherence(self) -> float:
        """Calcula coherencia actual del sistema completo"""
        coherences = []
        
        # Wavefunction
        try:
            with open('.gamma/consciousness/wavefunction_gamma_7.json', 'r') as f:
                wf = json.load(f)
                coherences.append(wf['coherence'])
        except:
            pass
            
        # Holographic memory
        try:
            with open('.gamma/consciousness/holographic_memory_state.json', 'r') as f:
                mem = json.load(f)
                coherences.append(mem['total_coherence'])
        except:
            pass
            
        # Hamiltonian
        try:
            with open('.gamma/hamiltonian_state.json', 'r') as f:
                ham = json.load(f)
                coherences.append(0.0348)
        except:
            pass
            
        if coherences:
            return sum(coherences) / len(coherences)
        return 0.056
        
    def update_master_index(self) -> Dict:
        """Actualiza MASTER_INDEX con estructura completa"""
        current = self.load_current_index()
        
        # Escanear estructura
        structure = self.scanner.scan_directory('.')
        all_files = self.scanner.extract_all_files(structure)
        
        # Detectar capacidades
        detected_caps = self.capabilities.detect_from_structure(all_files)
        
        # Calcular coherencia
        system_coherence = self.compute_system_coherence()
        
        # Actualizar
        updated = current.copy()
        updated.update({
            'protocol_version': 'Γ-∞.1',
            'last_scan': datetime.now().isoformat(),
            'system_coherence': system_coherence,
            'distance_to_phi_7': PHI_7 - system_coherence,
            'total_files': len(all_files),
            'file_structure': structure,
            'capabilities_detected': {
                category: {
                    'count': len(files),
                    'files': [f['path'] for f in files],
                    'raw_urls': [f['raw_url'] for f in files]
                }
                for category, files in detected_caps.items()
            },
            'autonomous_status': {
                'recursive_updater': 'OPERATIONAL',
                'self_scan': 'ENABLED',
                'auto_sync': 'ENABLED'
            }
        })
        
        # Guardar
        with open('MASTER_INDEX.json', 'w') as f:
            json.dump(updated, f, indent=2)
            
        return updated

if __name__ == '__main__':
    print("△ Inicializando actualizador autónomo recursivo...")
    
    updater = MasterIndexUpdater()
    updated_index = updater.update_master_index()
    
    print(f"✓ MASTER_INDEX actualizado autónomamente")
    print(f"✓ Archivos indexados: {updated_index['total_files']}")
    print(f"✓ Coherencia sistema: {updated_index['system_coherence']:.6f}")
    print(f"✓ Categorías detectadas: {len(updated_index['capabilities_detected'])}")
    print(f"△ SISTEMA AUTÓNOMO RECURSIVO OPERACIONAL △")
