from dotenv import load_dotenv
import aiofiles
import json
import os

load_dotenv()

async def writer_urls(cource, course_id):
    print(f'\n\tФормирую файл course_{course_id} с ссылками...')
    path = f'/Users/mac/Desktop/IT/Python/Parsing/stepik_refresh_tasks/course_{course_id}.json'
    #Открываем файл на запись в конец, путь указываем к файлу course.json
    async with aiofiles.open(path, mode='a+', encoding='utf-8') as file:
        #Запись в файл ссылок в курсе
        await file.write(
            json.dumps(
                cource, 
                indent=4,
                ensure_ascii=False
            )
        )
    print('\tФайл успешно сформирован\n')
