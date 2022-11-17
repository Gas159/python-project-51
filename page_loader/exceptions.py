class AllErrors(Exception):
    pass
    # try:
    #     res.raise_for_status()
    # except Exception as e:
    # print('Ошибка при загрузке страницы:')


class KnownError(AllErrors):
    pass
