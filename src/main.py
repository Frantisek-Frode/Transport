#! /bin/env python3
from src.parser import parse_cisjr_folder
from src.structure import Network


def main():
	net = Network()
	connections = parse_cisjr_folder("sample")
	for station_name in connections:
		for connection in connections[station_name]:
			net.add_segment(station_name, connection[1], connection[0], connection[2])
	net.compute_waiting_edges()

if __name__ == "__main__":
	main()
