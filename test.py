import requests
from telethon import events

from core.bot import bot
from util.config import CHAT_ID


# element = '<a href="https://daring.uin-suka.ac.id/attc/199013" class="downloadfile downloadfileset" rel="https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/get_file_stats/199013" title="">Pertemuan_2-MBDBQ-2024-up.pdf</a>'
# # parsed = BeautifulSoup(element, 'html.parser')
# # print(parsed)
# file = File(element)
# print(file.link)
# print(file.link)

@bot.on(events.NewMessage(pattern='/komen(?:\s|$)(.*)'))
async def handler(event):
    msg_value = str(event.pattern_match.group(1)).strip()
    split = msg_value.split(" ")
    post_id = split[0]
    komen_value = " ".join(split[1:])
    await send_komen(post_id, komen_value)


async def send_komen(post_id, value):
    url = "https://daring.uin-suka.ac.id/01_dashboard/s04_ct_dashboard2/comment_stats"

    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    payload = f"jenistampilan=0&content={value}&id_post={post_id}&kd_group=1"

    # cks = get_php_cookie()
    cookies = {'PHPSESSID': "83gu8phl3h4fprkv5juj752of6"}
    response = requests.post(url, headers=headers,
                             data=payload, cookies=cookies)
    if response.status_code == 200 and response.text != "err_k" and response != "":
        await bot.send_message(CHAT_ID, f"Berhasil kirim komentar `{value}` di postingan **{post_id}**")
    else:
        await bot.send_message(CHAT_ID, "Gagal kirim komentar !")


bot.run_until_disconnected()
