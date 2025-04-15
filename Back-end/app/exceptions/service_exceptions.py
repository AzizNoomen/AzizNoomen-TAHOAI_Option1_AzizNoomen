class ModelNotFoundException(Exception):
    def __init__(self, model_name:str):
        self.message = f"Model '{model_name}' doesn't exist, please specify the tag or change the model"
        super().__init__(self.message)

class ModelAlreadyExistsException(Exception):
    def __init__(self, model_name:str):
        self.message = f"Model '{model_name}' already exists"
        super().__init__(self.message)
