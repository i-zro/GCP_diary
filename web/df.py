from datetime import datetime
from pytz import timezone
# fmt = "%Y-%m-%d %H:%M:%S %Z%z"
KST = datetime.now(timezone('Asia/Seoul'))
# fmt = "%Y/%m/%d %H:%M:%S"
fmtt="%Y%MYd%H%M%S"
# print(KST.strftime(fmt))
#
link = 'https://52.79.68.147:5275/sad/sender/{0}'.format(KST.strftime(fmtt)).replace(' ','+')
print(link)

# print(datetime.now())