 # Пример декоратора (если потребуется)
def log_game_event(func):
    def wrapper(*args, **kwargs):
        print(f"Вызвана функция {func.name}")
        return func(*args, **kwargs)
    return wrapper
