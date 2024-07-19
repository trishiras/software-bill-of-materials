import json
import traceback
import subprocess
from software_bill_of_materials.core.logger import logger
from software_bill_of_materials.core.models import Response
from software_bill_of_materials.support.enums import (
    STDInput,
    MixedTypeEnum,
    ResponseMessage,
)


def run(target: str):
    resp = Response()
    data = None
    value = {}
    try:
        value = subprocess.check_output(
            STDInput.SYFT.value.format(
                target=target,
            ),
            shell=True,
        ).decode("utf-8")
        data = json.loads(value)
        if data:
            resp.success = MixedTypeEnum.SUCCESS.value
            resp.data = data
    except Exception as err:
        resp.message = ResponseMessage.SYFT_MSG.value
        logger.error(err)
        logger.debug(traceback.format_exc())

    return resp
