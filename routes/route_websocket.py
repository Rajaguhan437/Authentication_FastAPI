from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import JSONResponse, HTMLResponse

from pydantic import BaseModel
from typing import List


class Connection_manager():
    def __init__(self):
        self.active_conn: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_conn.append(websocket)
    

    async def disconnect(self, websocket: WebSocket):
        self.active_conn.remove(websocket)


    async def send_msg(self, msg: str, websocket: WebSocket):
        await websocket.send_text(msg)

    
    async def broadcast(self, client_id: int, message: str):
        for conn in self.active_conn:
            await conn.send_json({
                "data":{
                    "client_id": client_id,
                    "message": message
                }
            })
            

    async def send_notification(self, client_id: int, message:str):
        for conn in self.active_conn.values():
                message = {
                    "data":{
                        "client_id": client_id,
                        "message": message
                    }
                }
        await conn.send_json(message)

manager = Connection_manager()


with open('/home/rajaguhan/Projects/Authentication_FastAPI/static/index2.html', 'r') as f:
    html = f.read()


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}}, # need to check
)


@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/{client_id}")
async def simpole_chat(
    websocket: WebSocket, 
    client_id: int,
    background_tasks: BackgroundTasks
):
    await manager.connect(websocket)
    try: 
        while True:
            data = await websocket.receive_text()
            #await manager.send_msg("You messaged: "+data, websocket)
            await manager.broadcast(client_id=client_id, message=data)

            async def send_notification_task(client_id: int, message:str):
                await manager.send_notification(client_id, message)
                print({"message": "Notification queued for delivery"})

            background_tasks.add_task(send_notification_task, client_id, data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast("Client "+str(client_id)+" has left the chat")