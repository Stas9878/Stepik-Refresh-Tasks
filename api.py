from writer_urls import writer_urls
import aiohttp
import asyncio

async def get_lessons_api(session, unit):
    async with session.get(f'https://stepik.org/api/units/{unit}') as response:
        #Получаем json с данными о unit
        info_unit_json = await response.json()

        #Узнаём какой lesson привязан к конкретному unit
        lesson = info_unit_json['units'][0]['lesson']

        #Возвращаем ссылку на урок, чтобы обойти его в файле parser.py
        return f'https://stepik.org/lesson/{lesson}/step/1'

async def get_units_api(session, section, section_id):
    async with session.get(f'https://stepik.org/api/sections/{section}') as response:
        #Получаем json с данными о section
        info_section_json = await response.json()

        #Находим все юниты курса
        units = info_section_json['sections'][0]['units']

        #Создаём задачи для обхода каждого unit
        tasks = [asyncio.create_task(get_lessons_api(session, unit)) for unit in units]

        #Выполняем задачи и возвращаем словарь
        return {f'{section_id}_section_{section}': {'lessons_url': await asyncio.gather(*tasks)}}

async def get_sections_api(course_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://stepik.org/api/courses/{course_id}') as response:
            #Получаем json с данными о курсе
            info_cource_json = await response.json()

            #Находим все секции курса
            sections = info_cource_json['courses'][0]['sections']

            #Создаём задачи для обхода каждой section
            tasks = [asyncio.create_task(get_units_api(session, section, section_id)) for section_id, section  in enumerate(sections, 1)]
            
            #Выполняем задачи и возвращаем словарь
            course = {'cource_id': course_id,
                    'sections': await asyncio.gather(*tasks)}

            #Запись всех ссылок курса в файл (по желанию)
            # await writer_urls(course, course_id)

            return course
