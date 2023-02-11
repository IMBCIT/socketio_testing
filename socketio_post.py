import asyncio
import socketio
import time

from httpx_post import login_and_run, request_data, kill_game

# https://github.com/miguelgrinberg/flask-socketio/issues/18
namespace = 'test'

sio = socketio.AsyncClient(logger=True, engineio_logger=True, request_timeout=30)


@sio.event
async def connect():
    print('Connection to server established')
    print('Send game config requests now')
    await sio.emit('Client connected')


@sio.event
async def disconnect():
    print('Server disconnected')


@sio.on('step_data_handler')
async def handle_step_data(data):
    print(data)


@sio.on('steps_sent')
async def steps_sent(data):
    print(data)
    print('All steps have been sent')
    sio.emit('user_disconnected')


@sio.on('user_disconnected')
async def cleanup():
    print('Client disconnected and cleaning up resources')
    await kill_game()


async def get_steps():
    print('Getting steps from server')
    await sio.emit('get_steps', {'data': request_data})


async def main():
    await sio.connect(f'http://localhost:8000/{namespace}')
    await sio.sleep(5.0)
    await login_and_run()
    await get_steps()
    await sio.wait()

asyncio.run(main())
