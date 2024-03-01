import aiohttp
import asyncio

async def get_lessons_api(session, unit):
    async with session.get(f'https://stepik.org/api/units/{unit}') as response:
        info_unit_json = await response.json()
        lesson = info_unit_json['units'][0]['lesson']
        return f'https://stepik.org/lesson/{lesson}/step/1'

async def get_units_api(session, section):
    async with session.get(f'https://stepik.org/api/sections/{section}') as response:
        #Получаем json с данными о секции
        info_section_json = await response.json()
        #Находим все юниты курса
        units = info_section_json['sections'][0]['units']
        #Создаём задачи для обхода каждого юнита
        tasks = [asyncio.create_task(get_lessons_api(session, unit)) for unit in units]
        #Выполняем задачи
        return await asyncio.gather(*tasks)

async def get_sections_api(cource_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://stepik.org/api/courses/{cource_id}') as response:
            #Получаем json с данными о курсе
            info_cource_json = await response.json()
            #Находим все секции курса
            sections = info_cource_json['courses'][0]['sections']
            #Создаём задачи для обхода каждой секции
            tasks = [asyncio.create_task(get_units_api(session, section)) for section in sections]
            #Выполняем задачи
            urls = await asyncio.gather(*tasks)

            #Запись всех ссылок курс в файл (по желанию)
            print(urls)
            

asyncio.run(get_sections_api(58852))
