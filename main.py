import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Union, List, Dict
from pydantic import BaseModel


app = FastAPI()

# Crear usuarios 
class User(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Union[int, None] = None
    recommendations: List[str]
    ZIP: Union[int, None] = None


# Primer EndPoint
# Diccionario para almacenar los usuarios
users_dict: Dict[int, dict] = {}


@app.put('/user')
def CreateUser (user: User):
    user = user.dict()
    if user['user_id'] in users_dict:
        return {'Description':f'El usuario con user ID {user["user_id"]} ya existe '}
    else:
        users_dict[user['user_id']] = user
        return {"user_id": user, "message": "Usuario creado exitosamente"}


#Segundo EndPoint
@app.post('/user/{user_id}')
def UpdateUser(user_id: int, user_update: User):
    if user_id not in users_dict:
        return {'Description': f'El ID usuario {user_id} no existe '}
    else:
        user_data = user_update.dict()
        users_dict[user_id].update(user_data)
    return {"user_id": user_id, "message": "Usuario actualizado exitosamente"}


#Tercer EndPoint
@app.get('/user/{user_id}')
def GetUserInfo(user_id :int):
    if user_id not in users_dict:
        return {'Description':f'El user_id {user_id} no existe. '}
    else:
        userdata = users_dict[user_id]
        return userdata


# Cuarto Endpoint
@app.delete('/user/{user_id}')
def delete_user(user_id: int):
    if user_id not in users_dict:
        return {'Description': f'El user_id {user_id} no existe.'}
    else:
        users_dict.pop(user_id)

        return {"message": "Usuario eliminado exitosamente"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=False)