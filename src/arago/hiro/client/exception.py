from typing import Mapping, Any, List


class HiroClientError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class OntologyValidatorError(HiroClientError):
    message: str
    warnings: List[str]
    errors: List[str]

    def __init__(self, data: Mapping[str, Any]) -> None:
        super().__init__()
        error = data['error']
        self.message = error['message']
        result = error['result']
        self.warnings = result['warnings']
        self.errors = result['errors']

    @staticmethod
    def is_validator_error(data: Mapping[str, Any]) -> bool:
        # {
        #     'error': {
        #         'message': 'validation failed',
        #         'result': {
        #             'errors': [
        #                 'attribute ogit/description is invalid'
        #             ],
        #             'warnings': [
        #             ]
        #         }
        #     }
        # }
        if 'error' not in data:
            return False

        error = data['error']
        if 'message' not in error or 'result' not in error:
            return False

        message = error['message']
        result = error['result']
        if message != 'validation failed' or 'errors' not in result or 'warnings' not in result:
            return False

        warnings = result['warnings']
        errors = result['errors']
        if not isinstance(warnings, list) or not isinstance(errors, list):
            return False

        return True


class HiroServerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
