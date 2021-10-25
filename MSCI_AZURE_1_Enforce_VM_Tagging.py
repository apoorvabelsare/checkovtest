from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

import re

class EnforceVMTagging(BaseResourceCheck):

    required_tags = ['opsSupportDl', 'opsLifecycle']
    tag_to_regex = dict()

    def __init__(self):
        EnforceVMTagging.tag_to_regex_mapper()
        name = "Ensure you are using the required tags and values when creating virtual machines " + str(EnforceVMTagging.required_tags)
        id = "MSCI_AZURE_1"
        supported_resources = ['azurerm_virtual_machine', 'azurerm_linux_virtual_machine', 'azurerm_windows_virtual_machine']
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def tag_to_regex_mapper():
        EnforceVMTagging.tag_to_regex['opsSupportDl'] = "^[\w-]+(?:\.[\w-]+)*@(?:[\w-]+\.)+[a-zA-Z]{2,7}$"
        EnforceVMTagging.tag_to_regex['opsLifecycle'] = "^(short|long)-lived$"

    def scan_resource_conf(self, conf):
        # First element has to be specified, because conf['tags'] returns a list, which contains a dictionary!
        if 'tags' in conf:
            configured_tags = conf['tags'][0]
            keys = configured_tags.keys()
            for required_tag in EnforceVMTagging.required_tags:
                if required_tag not in keys:
                    return CheckResult.FAILED
            for key in keys:
                if key in EnforceVMTagging.required_tags:
                    if not re.match(EnforceVMTagging.tag_to_regex[key], configured_tags[key]):
                        return CheckResult.FAILED
            return CheckResult.PASSED
        else:
            return CheckResult.FAILED

check = EnforceVMTagging()