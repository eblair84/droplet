from sec import Sec
import sys

for index in range(0, len(sys.argv)):
	print('Command line argument: [{}][{}]'.format(index, sys.argv[index]))

transType = sys.argv[1]
# myCo = Sec('aapl', transType)
# myCo = Sec('fb', transType)
myCo = Sec('vxrt', transType)
