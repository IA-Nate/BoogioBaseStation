import sys
from bluepy import btle
import argparse

class ScanPrinter(btle.DefaultDelegate):
	def __init__(self, opts):
		btle.DefaultDelegate.__init__(self)
		self.opts = opts
	def handleDiscovery(self, dev, isNewDev, isNewData):
		print 'Device =',dev.addr, '  rssi =',dev.rssi

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--hci', action='store', type=int, default=0, help='Interface number for scan')
parser.add_argument('-t', '--timeout', action='store', type=int, default=4,help='Scan delay, 0 for continuous')
parser.add_argument('-s', '--sensitivity', action='store', type=int, default=-128, help='dBm value for filtering far devices')
parser.add_argument('-d', '--discover', action='store_true', help='Connect and discover service to scanned devices')
parser.add_argument('-a', '--all', action='store_true', help='Display duplicate adv responses, by default show new + update')
parser.add_argument('-n', '--new', action='store_true', help='Display only new adv responses, by default show new + updated')
parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')

arg = parser.parse_args(sys.argv[1:])
btle.Debugging = arg.verbose

print("Scanning for devices...")

scanner = btle.Scanner(arg.hci).withDelegate(ScanPrinter(arg))
devices = scanner.scan(arg.timeout)
