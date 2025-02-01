1. Для начала заберем проект к себе на машину:
 - git clone https://github.com/VladislavMironenko/botTest.git 

2. После этого нужно переименовать файл .env.example в .env

3. После этого нужно перейти в папку куда вы выгрузили проект и сделать:
 - docker-compose up --build  (Важный момент - при использование этой команды у вас должен быть открыт Docker Desktop - https://www.docker.com/products/docker-desktop/)

4. После этого нужно немного подождать для подгрузки всех библиотек , и вы сможете взаимодействовать с ботом ( бот - t.me/testTqaskBot )

5. Чтоб смотреть изменения в базе , вам нужно:
 - в терминале прописать следущюю коману - ( docker exec -it postgres-db psql -U user -d mydatabase )
 - после этого - ( SELECT * FROM poll_table2; )