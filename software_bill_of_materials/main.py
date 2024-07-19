import os
import json
from argparse import Namespace
from software_bill_of_materials.services import syft
from software_bill_of_materials.core.logger import logger
from software_bill_of_materials.core.input import parse_args
from software_bill_of_materials.support.enums import MixedTypeEnum


class SoftwareBillOfMaterials(object):
    def __init__(
        self,
        arguments: Namespace,
    ):
        self.data = {}
        self.target = arguments.target
        self.output_via = arguments.output_via
        self.webhook = arguments.webhook
        self.output_file_path = arguments.output_file_path

    def run(self):

        logger.info(
            f"Started generating software bill of materials for target :- {self.target}"
        )

        if self.webhook:
            logger.info(f"Webhook URL :- {self.webhook}")

        if self.output_file_path:
            logger.info(f"Output file path :- {self.output_file_path}")

        output_dir = os.path.join(
            os.getcwd(),
            MixedTypeEnum.OUTPUT.value,
        )
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        syft_response = syft.run(target=self.target)

        if syft_response.success:
            self.data = syft_response.data
        else:
            logger.error(syft_response.message)

        with open(self.output_file_path, "w") as fp:
            json.dump(self.data, fp, indent=4, default=str)

        logger.info(
            f"Finished generating software bill of materials for target :- {self.target}"
        )


def main():

    arguments, unknown = parse_args()

    software_bill_of_materials = SoftwareBillOfMaterials(arguments=arguments)
    software_bill_of_materials.run()
