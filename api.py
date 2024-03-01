import aiohttp
import asyncio

async def get_units_api(session, section):
    async with session.get(f'https://stepik.org/api/sections/{section}') as response:
        info_section_json = await response.json()
        units = info_section_json['sections'][0]['units']
        print(units)

async def get_sections_api(cource_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://stepik.org/api/courses/{cource_id}') as response:
            #Получаем json с данными о курсе
            info_cource_json = await response.json()
            #Находим все секции курса
            sections = [section for section in info_cource_json['courses'][0]['sections']]
            #Создаём задачи для обхода каждой секции
            tasks = [asyncio.create_task(get_units_api(session, i)) for i in sections]
            #Выполняем задачи
            await asyncio.gather(*tasks)
            

asyncio.run(get_sections_api(58852))
