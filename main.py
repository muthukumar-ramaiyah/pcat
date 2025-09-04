from sample_ptc import StringUtils
from sample_ptc.clients import ReqResClient

print(StringUtils.reverse("Hello, World!"))

print(ReqResClient.get_user(2))