from methods.company import BaseCompany


class dummy_company(BaseCompany):
    """ Dummy Company: -TEMPORARY- Used to allow backwards compatibility so a module can be
        called within the module code folder. All functionality in base class /sensors/deployment
    """

    def __init__(self, *args, **kwargs):
        super(dummy_company, self).__init__(*args, **kwargs)
