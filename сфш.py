import asyncio
from characterai import PyAsyncCAI


async def main():
    client = PyAsyncCAI('d1e57a70c7f3581b4e5597e6a3c7182f149f86a7')

    char = input('Enter CHAR: ')

    chat = await client.chat2.get_chat(char)

    author = {
        'author_id': chat['chats'][0]['creator_id']
    }

    while True:
        message = input('You: ')

        async with client.connect() as chat2:
            data = await chat2.send_message(
                char, chat['chats'][0]['chat_id'],
                message, author
            )

        name = data['turn']['author']['name']
        text = data['turn']['candidates'][0]['raw_content']

        print(f"{name}: {text}")


asyncio.run(main())
