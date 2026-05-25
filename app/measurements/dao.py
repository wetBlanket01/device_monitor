from app.dao.base import BaseDAO
from app.measurements.models import Measurement


class MeasurementDAO(BaseDAO):
    model = Measurement
