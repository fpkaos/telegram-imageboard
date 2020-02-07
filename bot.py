import telebot
from telebot.apihelper import get_chat_member
import config

bot = telebot.TeleBot(config.token)

def login_required(f):
    def wrap(msg):
        ans = get_chat_member(config.token, config.channel, msg.chat.id)
        if ans['status'] != 'left':
            f(msg)
        else:
            err = f"Станьте учатником канала {config.channel} чтобы отправлять сообщения!"
            bot.send_message(msg.chat.id, err)
    return wrap

@bot.message_handler(commands=["start"])
def start(msg):
    hello = f"Добро пожаловать на доску {config.channel}!\n\nПрисоединитесь, чтобы отправить сообщение"
    bot.send_message(msg.chat.id, hello)

@bot.message_handler(content_types='text')
@login_required
def echo_text(msg):
    bot.send_message(config.channel, msg.text)

@bot.message_handler(content_types='sticker')
@login_required
def echo_sticker(msg):
    bot.send_sticker(config.channel, msg.sticker.file_id)

@bot.message_handler(content_types='photo')
@login_required
def echo_photo(msg):
    if msg.caption is not None:
        bot.send_photo(
            config.channel,
            msg.photo[len(msg.photo) - 1].file_id,
            msg.caption
            )
    else:
        bot.send_photo(
            config.channel,
            msg.photo[len(msg.photo) - 1].file_id
            )

@bot.message_handler(content_types='location')
@login_required
def echo_location(msg):
    bot.send_location(
        config.channel,
        msg.location.latitude,
        msg.location.longitude
        )

@bot.message_handler(content_types='document')
@login_required
def echo_document(msg):
    if msg.caption is not None:
        bot.send_document(
            config.channel,
            msg.document[len(msg.photo) - 1].file_id,
            msg.caption
            )
    else:
        bot.send_document(config.channel, msg.document.file_id)

@bot.message_handler(content_types='audio')
@login_required
def echo_audio(msg):
    bot.send_audio(
        config.channel,
        msg.audio.file_id,
        msg.audio.performer,
        msg.audio.title
        )

@bot.message_handler(content_types='voice')
@login_required
def echo_voice(msg):
    bot.send_voice(config.channel, msg.voice.file_id)

@bot.message_handler(content_types='contact')
@login_required
def echo_contact(msg):
    bot.send_contact(
        config.channel,
        msg.contact.phone_number,
        msg.contact.first_name,
        msg.contact.last_name
        )

@bot.message_handler(content_types='video_note')
@login_required
def echo_video_note(msg):
    bot.send_video_note(
        config.channel,
        msg.video_note.file_id,
        msg.video_note.duration,
        msg.video_note.length
        )

@bot.message_handler(content_types='video')
@login_required
def echo_video(msg):
    if msg.caption is not None:
        bot.send_video(
            config.channel,
            msg.video.file_id,
            msg.video.duration,
            msg.caption
            )

    else:
        bot.send_video(
            config.channel,
            msg.video.file_id,
            msg.video.duration
            )

if __name__ == '__main__':
    bot.polling(none_stop=True)
