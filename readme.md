Установка:
1. Запустить python-3.6.1.exe
2. Поставить галочку на Add Python 3.6 to PATH
3. НажатьInstall Now


Настройки бота (текстовый файл settings.cfg):
1. Самая первая строка отвечает за текущую "цель" - ссылка на группу или человека
2. В последующие строки помещаются токены аккаунтов, которые будут отправлять заявки


Как получить токен аккаунта:
1. Имеется ссылка: https://oauth.vk.com/token?grant_type=password&scope=friends&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=USER&password=PASS
2. Заменить в ссылке USER на телефон/email ВК аккаунта
3. Заменить PASS на пароль ВК аккаунта
4. Получаете ответ, если ваш ответ, схожий на {"access_token":"4795krd78ag1c369db1ea288743a110d8571379405435f0160c26493988c64d88c02fe8c887bcd53a9ac7","expires_in":0,"user_id":374996700}
5. Скопировать набор символов, расположенный в кавычках, после "access_token" не включая сами кавычки
6. Пример:
4795krd78ag1c369db1ea288743a110d8571379405435f0160c26493988c64d88c02fe8c887bcd53a9ac7
Внимание! Желательно, что бы токен был получен с того же IP адреса, где будет работать сам бот.