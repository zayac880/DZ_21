from entity.request import Request
from entity.shop import Shop
from entity.store import Store
from exceptions import RequestError, LogisticError

store = Store(
    items={
        "печенька": 30,
        "кружка": 25,
        "елка": 3,
        "лопата": 5,
        "кофе": 8,
        "собачка": 1,
    },
)

shop = Shop(
    items={
        "печенька": 2,
        "кружка": 5,
        "елка": 2,
        "лопата": 3,
        "кофе": 1,
    },
)

shop_2 = Shop(
    items={
        "печенька": 2,
        "кружка": 5,
        "елка": 2,
    },
)

storages = {
    "магазин": shop,
    "склад": store,
    "аптека": shop_2,
}


def main():
    print('\nДобрый день!\n')

    while True:
        """Вывод содержимое складов"""
        for storage_name in storages:
            print(f'Сейчас в {storage_name}:\n {storages[storage_name].get_items()}')

        """Запрос ввод от пользователя"""
        user_input = input(
            'Введите запрос в формате "Доставить 3 печеньки из склад в магазин"\n'
            'Введите "стоп" или "stop", если желаете закончить:\n'
        )
        if user_input in ('stop', 'стоп'):
            break

        """Распарсить и провалидировать ввод пользователя"""
        try:
            request = Request(request=user_input, storages=storages)
        except RequestError as error:
            print(error.message)
            continue

        """Запустить доставку"""
        try:
            storages[request.departure].remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} из {request.departure}')
        except LogisticError as error:
            print(error.message)
            continue

        try:
            storages[request.destination].add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в {request.destination}')
        except LogisticError as error:
            print(error.message)
            storages[request.departure].add(request.product, request.amount)
            print(f'Курьер вернул {request.amount} {request.product} в {request.departure}')
            continue


if __name__ == '__main__':
    main()
