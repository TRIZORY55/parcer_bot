import logging
import asyncio
from keys import api_id, api_hash, bot_token, target_user_id, monitored_chat_ids, keywords,group_mapping
from pyrogram import Client, filters
import pyrogram.utils as utils

def get_peer_type(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

utils.get_peer_type = get_peer_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_message(message):
    logger.info(f"Проверка сообщения на наличие ключевых слов: {message.text}")
    for keyword in keywords:
        if keyword.lower() in message.text.lower():
            logger.info(f"Найдено ключевое слово: {keyword}")
            return True
    return False

async def send_notification_by_group_id(client, group_id, message_text):
    group_info = group_mapping.get(str(group_id))
    if group_info:
        group_name = group_info.get("name")
        group_link = group_info.get("link")
        if group_link:
            notification_message = f"Ключевое слово найдено в группе {group_name}: {group_link}\n\n{message_text}"
            await client.send_message(target_user_id, notification_message)
            logger.info(f"Отправлено уведомление: {notification_message}")
        else:
            logger.error(f"Не удалось найти ссылку на группу с ID '{group_id}'.")
    else:
        logger.error(f"Группа с ID '{group_id}' не найдена в сопоставлении.")

async def list_chats(client):
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        if chat.type in ["group", "supergroup", "channel"]:
            logger.info(f"Вы участник чата: {chat.title} (ID: {chat.id}, Type: {chat.type})")

async def track_chats():
    client = Client(name='my_account', api_id=api_id, api_hash=api_hash)

    @client.on_message()
    async def process_message(client, message):
        logger.info(f"Получено сообщение в чате {message.chat.id}: {message.text}")
        if message.text:
            logger.info("Обработчик сообщений сработал.")
            if await check_message(message):
                logger.info("Ключевое слово найдено!")
                await send_notification_by_group_id(client, message.chat.id, message.text)
        else:
            logger.info("Сообщение не содержит текста или это не текстовое сообщение.")

    try:
        await client.start()
        logger.info("Подключение к серверам Telegram успешно установлено")

        await list_chats(client)

        for chat_id in monitored_chat_ids:
            logger.info(f"Проверка чата с ID: {chat_id}")
            try:
                chat = await client.get_chat(chat_id)
                logger.info(f"Доступ к чату {chat_id} получен: {chat.title}")
            except Exception as e:
                logger.error(f"Не удалось получить доступ к чату {chat_id}: {e}")

        await asyncio.Event().wait()
    except Exception as e:
        logger.error(f"Произошла ошибка при отслеживании чатов: {e}")
        if isinstance(e, asyncio.CancelledError):
            logger.info("Задача отменена, остановка...")
    finally:
        await client.stop()
        logger.info("Клиент Telegram отключен")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(track_chats())
    except KeyboardInterrupt:
        logger.info("Получен сигнал SIGINT, завершение выполнения...")
    except Exception as e:
        logger.error(f"Произошла ошибка при отслеживании чатов: {e}")
        if isinstance(e, asyncio.CancelledError):
            logger.info("Задача отменена, остановка...")
    finally:
        if 'client' in locals() and client.is_initialized:
            loop.run_until_complete(client.disconnect())
        loop.close()
