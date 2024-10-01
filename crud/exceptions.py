class CreateModelException(Exception):
    error_code = "CREATE_MODEL"

class UpdateModelException(Exception):
    error_code = "UPDATE_MODEL"

class DeleteModelException(Exception):
    error_code = "DELETE_MODEL"