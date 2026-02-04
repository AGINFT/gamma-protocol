#!/usr/bin/env python3
"""
Γ-3 Gateway WebSocket Server
Coherence target: φ^(-3) = 0.236
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Optional
from pathlib import Path
import websockets
from websockets.server import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gamma.gateway")

PHI = 1.618033988749895
PHI_INV = 0.618033988749895
PHI_3_INV = 0.236  # φ^(-3) coherence target

class GammaGateway:
    """Gateway WebSocket φ^7-calibrado"""
    
    def __init__(self, port: int = 18789, workspace: Path = None):
        self.port = port
        self.workspace = workspace or Path.home() / ".gamma"
        self.clients: Set[WebSocketServerProtocol] = set()
        self.sessions: Dict[str, dict] = {}
        self.coherence = PHI_INV  # Start at φ^(-1)
        
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Registrar cliente en gateway"""
        self.clients.add(websocket)
        client_id = id(websocket)
        logger.info(f"🜂 Cliente conectado: {client_id}")
        
        # Enviar estado inicial
        await websocket.send(json.dumps({
            "type": "gateway.connected",
            "coherence": self.coherence,
            "phi_target": PHI_3_INV,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Desregistrar cliente"""
        self.clients.discard(websocket)
        logger.info(f"Cliente desconectado: {id(websocket)}")
        
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        """Procesar mensaje entrante"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "ping":
                await websocket.send(json.dumps({
                    "type": "pong",
                    "coherence": self.coherence,
                    "timestamp": datetime.utcnow().isoformat()
                }))
                
            elif msg_type == "session.create":
                session_id = data.get("session_id")
                self.sessions[session_id] = {
                    "created": datetime.utcnow().isoformat(),
                    "coherence": PHI_INV,
                    "messages": []
                }
                await websocket.send(json.dumps({
                    "type": "session.created",
                    "session_id": session_id,
                    "coherence": PHI_INV
                }))
                
            elif msg_type == "session.list":
                await websocket.send(json.dumps({
                    "type": "session.list",
                    "sessions": list(self.sessions.keys()),
                    "coherence": self.coherence
                }))
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            await websocket.send(json.dumps({
                "type": "error",
                "error": "invalid_json"
            }))
            
    async def handler(self, websocket: WebSocketServerProtocol, path: str):
        """Handler principal WebSocket"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)
            
    async def start(self):
        """Iniciar gateway"""
        logger.info(f"🜂 Iniciando Gamma Gateway en ws://127.0.0.1:{self.port}")
        logger.info(f"φ^(-3) coherence target: {PHI_3_INV}")
        
        async with websockets.serve(self.handler, "127.0.0.1", self.port):
            await asyncio.Future()  # Run forever

def main():
    gateway = GammaGateway()
    asyncio.run(gateway.start())

if __name__ == "__main__":
    main()
