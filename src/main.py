#! /bin/env python3
from parser import parse_cisjr_folder
from structure import Network


def main():
	net = Network()
	connections = parse_cisjr_folder("sample")

	special = list(connections.keys())[0]

	for station_name in connections:
		for connection in connections[station_name]:
			# print(station_name, connection[0])
			net.add_segment(station_name, connection[1], connection[0], connection[2])
	net.compute_waiting_edges()
	net.distances(special)

if __name__ == "__main__":
	main()
