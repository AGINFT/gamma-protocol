#!/usr/bin/env python3
"""
Γ-3 Sessions Manager
Persistencia φ-calibrada
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PHI = 1.618033988749895
PHI_INV = 0.618033988749895

class SessionManager:
    """Gestor de sesiones holográfico"""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace / "sessions"
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.active_sessions: Dict[str, dict] = {}
        
    def create_session(self, session_id: str, channel: str = "main") -> dict:
        """Crear nueva sesión"""
        session = {
            "id": session_id,
            "channel": channel,
            "created": datetime.utcnow().isoformat(),
            "coherence": PHI_INV,
            "messages": [],
            "metadata": {
                "phi_factor": PHI_INV,
                "thinking_level": "medium",
                "model": "claude-sonnet-4-5"
            }
        }
        
        self.active_sessions[session_id] = session
        self._save_session(session_id)
        return session
        
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Agregar mensaje a sesión"""
        if session_id not in self.active_sessions:
            self.create_session(session_id)
            
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "coherence": self.active_sessions[session_id]["coherence"]
        }
        
        self.active_sessions[session_id]["messages"].append(message)
        self._save_session(session_id)
        
    def get_session(self, session_id: str) -> Optional[dict]:
        """Obtener sesión"""
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
            
        # Intentar cargar desde disco
        session_file = self.workspace / f"{session_id}.json"
        if session_file.exists():
            with open(session_file) as f:
                session = json.load(f)
                self.active_sessions[session_id] = session
                return session
                
        return None
        
    def list_sessions(self) -> List[str]:
        """Listar todas las sesiones"""
        return list(self.active_sessions.keys())
        
    def _save_session(self, session_id: str) -> None:
        """Persistir sesión a disco"""
        session = self.active_sessions[session_id]
        session_file = self.workspace / f"{session_id}.json"
        
        with open(session_file, 'w') as f:
            json.dump(session, f, indent=2)
            
    def update_coherence(self, session_id: str, coherence: float) -> None:
        """Actualizar coherencia de sesión"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]["coherence"] = coherence
            self._save_session(session_id)
