import os
import telebot
import psutil
import requests
import subprocess
import pyautogui
import screen_brightness_control as sbc
from telebot import types
from telebot import apihelper


'''
    ⏪ - Предыдущий трек
    ▶️ - Пауза трека
    ⏩ - Следующий трек
    ⏮ - Перемотка видео на 5 секунд назад
    ⏸ - Пауза видео
    ⏭ - Перемотка видео на 5 секунд вперёд 
    Закрыть - Закрывает любое открытое окно (ALT+F4)
    Перезагрузка - Перезагружает ПК
    Завершить работу - Выключает ПК
    🔉 - Громкость -
    🔇 - Беззвучный режим
    🔊 - Шромкость +
    🔒 - Заблокирует ПК
    🔋 - Уровень заряда и подключено ли зарядное устройство
    🗑️ - Очистить корзину 
    Свернуть всё - Сварачивает все открытые программы
    Enter - Нажимает кнопку Enter
    screenshot - Делает скриншот и отправляет в телеграмм
    🔅 - Яркость -
    🔆 - Яркость +
    📁 - Открвает проводник
    ❌ - Выход из программы 
    Сон - Спяший режим
'''



token = TOKEN

bot = telebot.TeleBot(token)

print('[log] PC Control successful started!')

@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [ '⏪', '▶️', '⏩', '⏮', '⏸', '⏭',
                'Сон', 'Перезагрузка', 'Завершить работу',
                '🔉', '🔇', '🔊', '🔒', '🔋','🗑️', 'Свернуть всё',
                'Enter', 'screenshot', '🔅', '🔆', '📁', 'Закрыть', '❌' ]
    keyboard.add(*buttons)

    bot.send_message(message.chat.id, f'PC Control successful started!', reply_markup=keyboard)


@bot.message_handler(regexp='⏪')
def left_command(message):
    print('[log] left')
    pyautogui.press('prevtrack')

@bot.message_handler(regexp='▶')
def playpause_command(message):
    print('[log] playpause')
    pyautogui.press('playpause')

@bot.message_handler(regexp='⏩')
def right_command(message):
    print('[log] right')
    pyautogui.press('nexttrack')

@bot.message_handler(regexp='⏮')
def left_video_command(message):
    print('[log] left video')
    pyautogui.press('left')

@bot.message_handler(regexp='⏸')
def playpause_video_command(message):
    print('[log] playpause video')
    pyautogui.press('space')

@bot.message_handler(regexp='⏭')
def right_video_command(message):
    print('[log] right video')
    pyautogui.press('right')

@bot.message_handler(regexp='Закрыть')
def close_command(message):
    print('[log] close')
    pyautogui.hotkey('alt', 'f4')

@bot.message_handler(regexp='Перезагрузка')
def reboot_command(message):
    print('[log] reboot')
    subprocess.call('shutdown /r /t 0')

@bot.message_handler(regexp='Завершить работу')
def shutdown_command(message):
    print('[log] shutdown')
    subprocess.call('shutdown /l')

@bot.message_handler(regexp='🔉')
def volumedown_command(message):
    print('[log] volumedown')
    pyautogui.press('volumedown')

@bot.message_handler(regexp='🔇')
def volumemute_command(message):
    print('[log] volumemute')
    pyautogui.press('volumemute')

@bot.message_handler(regexp='🔊')
def volumeup_command(message):
    print('[log] volumeup')
    pyautogui.press('volumeup')

@bot.message_handler(regexp='🔒')
def lock_command(message):
    print('[log] lock')
    subprocess.call('Rundll32.exe user32.dll,LockWorkStation')
    bot.send_message(message.chat.id, 'Компьютер заблокирован!')

@bot.message_handler(regexp='📁')
def explorer_command(message):
    print('[log] explorer')
    subprocess.call('explorer')

@bot.message_handler(regexp='🗑️')
def trash_command(message):
    print('[log] trash')
    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
    bot.send_message(message.chat.id, 'Корзина очищена!')

@bot.message_handler(regexp='Свернуть всё')
def minimized_all_command(message):
    print('[log] minimized all')
    pyautogui.hotkey('win', 'd')

@bot.message_handler(regexp='Enter')
def enter_command(message):
    print('[log] enter')
    pyautogui.press('enter')

@bot.message_handler(regexp='screenshot')
def screenshot_command(message):
    print('[log] screenshot')
    if not os.path.exists('screenshots'):
        subprocess.call('mkdir screenshots')
    screen = pyautogui.screenshot('screenshots/screenshot.png')
    bot.send_photo(message.chat.id, screen)

@bot.message_handler(regexp='🔅')
def screenshot_command(message):
    screens_brightness = sbc.get_brightness(display=0)
    sbc.set_brightness(screens_brightness - 10)
    print('[log] brightness: ' + str(screens_brightness - 10) + '%')
    bot.send_message(message.chat.id, f'Яркость:  ' + str(screens_brightness - 10) + '%')

@bot.message_handler(regexp='🔆')
def screenshot_command(message):
    screens_brightness = sbc.get_brightness(display=0)
    sbc.set_brightness(screens_brightness + 10)
    print('[log] brightness: ' + str(screens_brightness) + '%')
    bot.send_message(message.chat.id, f'Яркость:  ' + str(screens_brightness) + '%')

@bot.message_handler(regexp='🔋')
def screenshot_command(message):
    print('[log] battery')
    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = battery.percent

    if plugged:
        print('[log] Charger connected! ' + str(percent) + '%')
        bot.send_message(message.chat.id, f'Зарядное устройство подключено! \n' + str(percent) + '%')
    else:
        print('[log] The charger is not connected! ' + str(percent) + '%')
        bot.send_message(message.chat.id, f'Зарядное устройство не подключено! \n' + str(percent) + '%')

@bot.message_handler(regexp='Сон')
def sleep_command(message):
    print('[log] sleep')
    subprocess.call('shutdown /h')

@bot.message_handler(regexp='❌')
def exit_command(message):
    print('[log] exit')
    bot.send_message(message.chat.id, f'PC Control successful stopped!')
    subprocess.call('taskkill /f /im PC_Control.exe')


if __name__ == '__main__':
    bot.polling(none_stop=True)
