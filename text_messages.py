start_message = (
    "<b>Привет!</b>\nЭтот бот позволит разместить "
    "Ваше объявление о сдаче жилья"
)


def result_message(data):
    result = (
        f'• <b>Имя:</b> {data["name"]} ({data["person"].lower()})\n\n'
        f'• <b>Тип:</b> {data["type"]}\n'
        f'• <b>Район:</b> {data["district"]}\n'
        f'• <b>Комнат:</b> {data["rooms"]}\n'
        f'• <b>Отопление Baxi:</b> {data["baxi"]}\n'
        f'• <b>Кондиционер:</b> {data["conditioner"]}\n'
        f'• <b>Животные:</b> {data["pets"]}\n\n'
        f'• <b>Состояние:</b> {data["condition"]}\n\n'
        f'• <b>Комментарий:</b> {data["pros"]}\n\n'
        f'• <b>Период:</b> {data["period"]}\n'
        f'• <b>Стоимость:</b> {data["price"]}\n'
        f'• <b>Контакты:</b> {data["number"]}\n\n'
        f'#сдаю_жилье #{data["person"].lower()} #{data["type"].lower()}\n'
        "@yerevan_rent_channel\n"
        "@yerevan_rent_bot"
    )
    return result
