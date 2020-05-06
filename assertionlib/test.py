from assertionlib import assertion


class Bob(AssertionError): ...


a = assertion.eq(1, 1)
b = assertion.eq(1, 1, 1, exception=TypeError)
c = assertion.eq(1, 1, 1, exception=AssertionError)
d = assertion.eq(1, 1, 1, exception=Bob)
