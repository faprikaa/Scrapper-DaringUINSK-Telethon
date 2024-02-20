def dynamic_func():
    print("Hello there!")

# @bot.on(events.NewMessage(pattern='/exec'))
# async def handler(events):
#     # exec(dynamic_func())


# @bot.on(events.NewMessage(pattern='/purge2(?:\s|$)(.*)'))
# async def handler(event):
#     argument = event.pattern_match.group(1).strip()
#     length = 20
#     msg1 = await bot.send_message(CHAT_ID, f"Purging {length} messages")
#     if argument != "":
#         length = int(argument)
#     list_msg = await bot.get(CHAT_ID, limit=length)
#     # print(list_msg)
#     for msg in list_msg:
#         await bot.delete_messages(CHAT_ID, msg.id)
#     await bot.delete_messages(CHAT_ID, msg1)
