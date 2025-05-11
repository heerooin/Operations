from datetime import datetime


def main(data: str) -> str:
    """Функция возвращения даты"""
    d = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%f")
    return d.strftime("%d.%m.%Y")


if __name__ == '__main__':
    print(main('2018-10-14T08:21:33.419441'))
