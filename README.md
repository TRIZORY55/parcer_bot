## Документация к Parcer_bot

Этот бот предназначен для отслеживания сообщений в заданных чатах Telegram на наличие ключевых слов и отправки уведомлений в личные сообщения указанному пользователю в случае обнаружения ключевого слова.

## <b>Основные компоненты:</b>
<b>Использованные библиотеки и зависимости:</b>

<li>logging: Для ведения логов работы бота.
<li>asyncio: Для асинхронного выполнения задач.
<li>pyrogram: Клиент Telegram API для работы с Telegram.

<b>Настройки, импортированные из внешнего модуля keys:</b>

<li>api_id: ID приложения Telegram.
<li>api_hash: Хэш приложения Telegram.
<li>bot_token: Токен вашего бота Telegram.
<li>target_user_id: ID пользователя, которому будут отправляться уведомления.
<li>monitored_chat_ids: Список ID чатов, в которых происходит отслеживание сообщений.
<li>keywords: Список ключевых слов для поиска в сообщениях.
<li>group_mapping: Сопоставление ID групп с их названиями и ссылками.

## <b>Функции:</b>

<li>get_peer_type(peer_id): Определяет тип пира (чата) по его ID (пользователь, канал или группа).
<li>check_message(message): Проверяет сообщение на наличие ключевых слов.
<li>send_notification_by_group_id(client, group_id, message_text): Отправляет уведомление о найденном ключевом слове в указанный чат.
<li>list_chats(client): Выводит список чатов, в которых участвует бот.

##  <b>Основной процесс работы бота:</b>

<li>Создается клиент pyrogram.Client для работы с Telegram API.
<li>Подключение к серверам Telegram и получение списка чатов, в которых бот является участником.
<li>Для каждого чата из monitored_chat_ids проверяется доступ и добавляется в список отслеживаемых чатов.
<li>При получении нового сообщения в отслеживаемом чате проверяется наличие ключевых слов. Если слово найдено, отправляется уведомление с информацией о чате и сообщении.

## <b>Логирование:</b>

<li>Ведется детальное логирование действий бота, включая получение сообщений, обработку и отправку уведомлений.
<li>Логи позволяют отслеживать работу бота и выявлять возможные проблемы в случае ошибок.

## <b>Запуск бота:</b>

<li>Для запуска бота необходимо запустить скрипт track_chats() с помощью asyncio.
<li>Бот будет работать в фоновом режиме, отслеживая сообщения в чатах и отправляя уведомления при необходимости.
<li>Программа будет работать до получения сигнала прерывания (например, Ctrl+C) или до возникновения ошибки.

## <b>Примечание:</b>

<li>Для корректной работы бота убедитесь, что все необходимые зависимости установлены.
<li>Предоставьте боту доступ к отслеживаемым чатам и убедитесь, что ID чатов и другие настройки указаны корректно в файле keys.py.
<li>Это основная информация по боту для отслеживания ключевых слов в чатах Telegram. Подробнее смотрите код для дополнительных настроек и настройки логирования.
