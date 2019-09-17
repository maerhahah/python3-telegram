from telethon import TelegramClient, utils
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterDocument

api_id = 1012166
api_hash = '757892add13f6e6a70595fcc9f23db0e'
client = TelegramClient('Jian', api_id, api_hash)
channel = 'https://t.me/jeannieStudioGroup'

async def main():
    # print('**********************send_message*****************************')
    # # 发送消息
    # await client.send_message('me', 'Hello to myself!')

    print('*************************messages**************************')
    messages = client.iter_messages(channel, limit=100)
    msges = '';
    async for message in messages:
        msg = str(message.date) + '[' + str(utils.get_display_name(message.sender)) + ':' + str(message.message) + ']\n'
        print(msg)
        msges = msges + msg
    with open('./telegram/messages.text', 'w') as file:
        file.write(msges)

    print('*************************photos**************************')
    photos = await client.get_messages(channel, None, filter=InputMessagesFilterPhotos)

    total = len(photos)
    index = 0
    for photo in photos:
        filename = "./telegram/" + str(photo.id) + ".jpg"
        index = index + 1
        print("downloading:", index, "/", total, " : ", filename)
        # 下载图片
        await client.download_media(photo, filename)

    print('*************************files**************************')
    files = await client.get_messages(channel, None, filter=InputMessagesFilterDocument)

    for file in files:
        attributes = file.media.document.attributes
        # 文件
        if len(attributes) == 1:
            fileName = file.media.document.attributes[0].file_name
            print(fileName)
        # 图片格式
        if len(attributes) == 2:
            fileName = file.media.document.attributes[1].file_name
            print(fileName)
        # 下载文件
        await client.download_media(file, "./telegram/" + fileName)


with client:
    client.loop.run_until_complete(main())
