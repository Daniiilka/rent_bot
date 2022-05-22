start_message = (
    "<b>Привет!</b>\nЭтот бот позволит разместить "
    "Ваше объявление о сдаче жилья"
)


def result_message(data):
    result = (
        f'Владелец: {data["name"]}\n\n'
        f'Тип: {data["type"]}\n\n'
        f'Район: {data["district"]}\n\n'
        f'Состояние: {data["condition"]}\n\n'
        f'Животные: {data["pets"]}\n\n'
        f'Комментарий владельца: {data["pros"]}\n\n'
        f'Комнат: {data["rooms"]}\n\n'
        f'Отопление Baxi: {data["baxi"]}\n\n'
        f'Кондиционер: {data["conditioner"]}\n\n'
        f'Период: {data["period"]}\n\n\n'
        f'Стоимость: {data["price"]}\n\n'
        f'Контакты: {data["number"]}\n'
    )
    return result
