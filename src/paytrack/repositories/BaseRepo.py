# from typing import TYPE_CHECKING
# from ..models import Base
# from ..core import Engine
#
#
# if TYPE_CHECKING:
#     from sqlalchemy.orm import Session
#
#
# class AbstractBaseRepository:
#     _model: Base
#     __engine: Engine
#
#     def __init__(self, engine: Engine, model: Base):
#         self.__engine = engine
#         self._model = model
#
#     def get_by_id(self, id_: int) -> Base | None:
#         session: Session = next(self.__engine.get_session())
#
#         return session.get(self._model, id_)
