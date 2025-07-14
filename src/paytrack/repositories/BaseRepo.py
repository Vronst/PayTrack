class AbstractBaseRepository:
    _model: Base 
    __engine: Engine 

    def __init__(self, engine: Engine, model: Base):
        self.__engine = engine 
        self._model = model


    def get_by_id(id_: int) -> Base:

