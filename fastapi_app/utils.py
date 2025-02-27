from datetime import datetime, timedelta
def get_seconds_until_14_11() -> int:
    """
    Вычисляет количество секунд до 14:11 текущего или следующего дня.
    """
    now = datetime.now()
    target_time_today = now.replace(hour=14, minute=11, second=0, microsecond=0)
    
    if now < target_time_today:
        # Если текущее время меньше 14:11, кэш истекает сегодня в 14:11
        time_difference = target_time_today - now
    else:
        # Если текущее время больше 14:11, кэш истекает завтра в 14:11
        target_time_tomorrow = target_time_today + timedelta(days=1)
        time_difference = target_time_tomorrow - now
    
    return int(time_difference.total_seconds())