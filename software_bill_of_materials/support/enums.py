from enum import Enum


class MixedTypeEnum(Enum):
    # Boolean constants
    SUCCESS = True

    # String constants
    OUTPUT = "output"


class ResponseMessage(Enum):
    SYFT_MSG = "SYFT did not return any response"


class STDInput(Enum):
    SYFT = "syft {target} --scope all-layers -o syft-json"
