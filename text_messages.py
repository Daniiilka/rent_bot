start_message = (
    "<b>Привет!</b>\nЭтот бот позволит разместить "
    "Ваше объявление о сдаче жилья"
)


def result_message(data):
    result = (
        "Здравствуйте!\n\n"
        f'Меня зовут: {data["name"]}\n'
        f'Тип жилья: {data["type"]}\n'
        f'Район: {data["district"]}\n'
        f'Состояние жилья: {data["condition"]}\n'
        f'Отношение к животным: {data["pets"]}\n'
        f'Стоимость жилья: {data["price"]}\n'
        f'Комментарий от владельца: {data["pros"]}\n'
        f'Количество комнат: {data["rooms"]}\n'
        f'Наличие отопления (Baxi): {data["baxi"]}\n'
        f'Наличие кондиционера: {data["conditioner"]}\n'
        f'Сдаю на период: {data["period"]}\n'
        f'Контактный номер телефона: {data["number"]}\n'
    )
    return result
