# 1. Імпорт необхідних бібліотек
import paho.mqtt.client as mqtt
import requests  # Для надсилання повідомлень в Telegram
import datetime,json,config

SEND_VALUE = "ON"

# 2. Налаштування

def load_topics():
    file_path = 'topics.json'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(f"✅ Дані успішно завантажено зі '{file_path}' у змінну.")
        print(f"Тип змінної: {type(data)}")
        # print(f"Ключі у змінній: {data.keys()}")
        return data
    except FileNotFoundError:
        print(f"❌ Помилка: Файл '{file_path}' не знайдено.")
    except json.JSONDecodeError:
        print(f"❌ Помилка: Неправильний формат JSON у файлі '{file_path}'.")
    except Exception as e:
        print(f"❌ Виникла несподівана помилка: {e}")

# 3. Функція для надсилання повідомлення в Telegram
def send_telegram_message(message,chat_id):
    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'  # Або 'HTML', якщо потрібно форматування
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # Викликати помилку для поганих відповідей
    except requests.exceptions.RequestException as e:
        print(f"Помилка надсилання Telegram: {e}")


# 4. MQTT-Колбек: Що робити при отриманні повідомлення
def on_message(client, userdata, msg):
    try:
        # Декодуємо отримані дані
        payload = msg.payload.decode("utf-8")
        topic = msg.topic
        if SEND_VALUE == payload:
            # Формуємо повідомлення для Telegram
            date = datetime.datetime.now()
            telegram_text = f"🚨 **СПОВІЩЕННЯ MQTT** 🚨\n" \
                            f"**Дата:**  `{date}`\n" \
                            f"**Топік:** `{topic}`\n" \
                            f"**Дані:**  `{payload} `"

            # Надсилаємо
            chat_id = MQTT_CHATS.get(topic)
            send_telegram_message(telegram_text,chat_id)
            print(f"Отримано: {date}: {topic} -> {payload}. Надіслано в чат {chat_id} ")

    except Exception as e:
        print(f"Помилка обробки повідомлення: {e}")



data= load_topics()
mqtt_topics_list = data.get("MQTT_TOPICS", [])
MQTT_TOPIC = [
    (item["topic"], item["qos"])
    for item in mqtt_topics_list
]
MQTT_CHATS = {
    item["topic"]: item["chat_id"]
    for item in mqtt_topics_list
}


# 5. Налаштування MQTT-Клієнта
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username=config.MQTT_USERNAME, password=config.MQTT_PASSWORD)
client.on_message = on_message

# # 6. Підключення та запуск
try:
    client.connect(config.MQTT_BROKER, int(config.MQTT_PORT), 60)  # Порт за замовчуванням 1883
    client.subscribe(MQTT_TOPIC)

    # Запуск циклу клієнта. Він блокує, тому це має бути остання команда.
    # Для неблокуючого виконання можна використати client.loop_start()
    print(f"Підключено до MQTT-брокера {config.MQTT_BROKER}. Очікування повідомлень на {MQTT_TOPIC}...")
    client.loop_forever()
except Exception as e:
    print(f"Помилка підключення/запуску: {e}")

