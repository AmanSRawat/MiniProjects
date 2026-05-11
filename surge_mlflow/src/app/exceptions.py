class ModelError(Exception):
    pass

class ModelLoadingError(ModelError): 
    pass

class PredictionError(ModelError):
    pass

class InvalidInputDataError(ModelError):
    pass