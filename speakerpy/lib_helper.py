from time import process_time

# https://pypi.org/project/silero/#text-to-speech
settings_selero = {
    #  aidar, baya, kseniya, xenia, random
    "ru_man": {
        "sample_rate": 24000,
        "sp": dict(model_id="v3_1_ru", language="ru", speaker="aidar", device="cpu"),
    },
    "ru_noman": {
        "sample_rate": 8000,
        "sp": dict(model_id="v3_1_ru", language="ru", speaker="xenia", device="cpu"),
    },
    "en": {
        "sample_rate": 48000,
        "sp": dict(model_id="v3_en", language="en", speaker="en_6", device="cpu"),
    },
}


def timeit(func):
    """Декоратор для замера времени выполнения функции"""

    def wrapper(*args, **kwargs):
        start_time = process_time()
        result = func(*args, **kwargs)
        end_time = process_time()
        print(
            f"Время выполнения функции '{func.__name__}': {end_time - start_time} секунд"
        )
        return result

    return wrapper
