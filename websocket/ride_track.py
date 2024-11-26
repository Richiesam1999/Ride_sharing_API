# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from typing import List

# router = APIRouter()

# # Keep track of active WebSocket connections
# active_connections: List[WebSocket] = []


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()


# @router.websocket("/ws/ride_tracking")
# async def ride_tracking(websocket: WebSocket):
#     """
#     WebSocket endpoint for ride tracking.
#     """
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"Received: {data}")
#             # Broadcast the received message to all clients
#             await manager.broadcast(f"Broadcasting: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         print("Client disconnected")
