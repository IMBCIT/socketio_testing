import httpx

url = 'http://127.0.0.1:8000'

sim_params = {
   "step_num":3600,
   "game_config":{
      "duration":{
         "type":"day",
         "value":150
      },
      "human_agent":{
         "amount":1
      },
      "food_storage":{
         "ration":300
      },
      "eclss":{
         "amount":1
      },
      "solar_pv_array_mars":{
         "amount":100
      },
      "power_storage":{
         "kwh":1000
      },
      "nutrient_storage":{
         "fertilizer":300
      },
      "single_agent":1,
      "plants":[
         {
            "species":"rice",
            "amount":2
         },
         {
            "species":"cabbage",
            "amount":8
         },
         {
            "species":"tomato",
            "amount":8
         },
         {
            "species":"sweet_potato",
            "amount":5
         }
      ],
      "greenhouse":"greenhouse_sam",
      "habitat":"crew_habitat_sam"
   }
}

request_data = {
        "game_id": "",
        "min_step_num": 0,
        "n_steps": sim_params['step_num']
        }


async def login_and_run():
    async with httpx.AsyncClient() as client:
        _ = await client.post(f'{url}/register', json={"username": "test1", "password": "testing12345"}, timeout=None)
        _ = await client.post(f'{url}/login', json={"username": "test1", "password": "testing12345"}, timeout=None)
        r = await client.post(f'{url}/new_game', json=sim_params, timeout=None)

        response = r.json()
        if 'game_id' in response:
            request_data['game_id'] = response['game_id']
            print(f"game_id: {request_data['game_id']}")

        # _ = await client.post(f'{url}/get_step_to', data={'step_num': request_data['n_steps'], 'game_id': request_data['game_id']})


async def kill_game():
    async with httpx.AsyncClient() as client:
        _ = await client.post(f'{url}/login', json={"username": "test1", "password": "testing12345"}, timeout=None)
        _ = await client.post(f'{url}/kill_game', json=request_data, timeout=None)
