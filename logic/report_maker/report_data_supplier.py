from dataclasses import dataclass, asdict


@dataclass
class ReportDataSupplier:
    periodfrom: str
    periodto: str
    nip: str
    contractor: str
    ordernumber: str
    orderscope: str
    netamountdue: str
    pivottable: str

    def __init__(self, period_from, period_to, nip, contractor, order_number, order_scope, net_amount_due, pivot_table):
        self.periodfrom = period_from
        self.periodto = period_to
        self.nip = nip
        self.contractor = contractor
        self.ordernumber = order_number
        self.orderscope = order_scope
        self.netamountdue = net_amount_due
        self.pivottable = pivot_table

    def supply(self):
        return asdict(self)
