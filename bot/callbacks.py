from aiogram.filters.callback_data import CallbackData

class AttendanceCallback(CallbackData, prefix="atd"):
    record_id: int
    action: str
    
class ReviewCallback(CallbackData, prefix="rev"):
    record_id: int
    mark: str
    text: str