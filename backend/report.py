from models import Timestamp
from typing import Sequence, Optional
from openpyxl import Workbook
from openpyxl.drawing.image import Image

class Report:
    def __init__(self, timestamps : Sequence[Timestamp]):
        self.timestamps: Sequence[Timestamp] = timestamps

    def generate_report(self) -> Optional[Workbook]:
        wb = Workbook()
        ws = wb.active
        if not ws:
            return None
        
        data = [[ts.id, ts.employee_id, ts.position, ts.start_time, ts.end_time] for ts in self.timestamps]
        ws.append(data)

        start_images = [Image(ts.start_photo_path) for ts in self.timestamps]
        end_images = [Image(ts.end_photo_path) for ts in self.timestamps]

        for i, img in enumerate(start_images):
            ws.add_image(img, f"F{i+1}")

        for i, img in enumerate(end_images):
            ws.add_image(img, f"J{i+1}")
        return wb