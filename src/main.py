#! /bin/env python3
from src.parser import parse_cisjr_folder


def main():
	connections = parse_cisjr_folder("sample")

if __name__ == "__main__":
	main()
