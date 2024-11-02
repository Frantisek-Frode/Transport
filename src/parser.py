import os
import time
from xml.etree import ElementTree


def parse_cisjr(filename: str) -> dict[str, list[tuple[str, int, int, list[str]]]]:
    connection = {}
    with open(filename) as file1:
        tree = ElementTree.parse(file1)
        root = tree.getroot()
        scheduled_stop_point2_name = {}
        passes = {}
        journeyStopPoint2ScheduledStopPoint = {}
        lineNames = []
        servicePattern = {}
        for dataObj in root.findall("{http://www.netex.org.uk/netex}dataObjects"):
            for compositeFrame in dataObj.findall("{http://www.netex.org.uk/netex}CompositeFrame"):
                for frames in compositeFrame.findall("{http://www.netex.org.uk/netex}frames"):
                    for serviceJourney in frames.findall("{http://www.netex.org.uk/netex}TimetableFrame/"
                                                         "{http://www.netex.org.uk/netex}vehicleJourneys/"
                                                         "{http://www.netex.org.uk/netex}ServiceJourney"):
                        servicePatterRef = serviceJourney.find("{http://www.netex.org.uk/netex}ServiceJourneyPatternRef").get("ref")
                        for passingTimes in serviceJourney.findall("{http://www.netex.org.uk/netex}passingTimes"):
                            passes[passingTimes.get("id")] = {}
                            for passingTime in passingTimes.findall("{http://www.netex.org.uk/netex}TimetabledPassingTime"):
                                passes[passingTimes.get("id")][passingTime.find("{http://www.netex.org.uk/netex}StopPointInJourneyPatternRef").get("ref")] = (
                                    servicePatterRef,
                                    passingTime.findtext("{http://www.netex.org.uk/netex}ArrivalTime"),
                                    passingTime.findtext("{http://www.netex.org.uk/netex}DepartureTime"),
                                )
                    for journeyPattern in frames.findall("{http://www.netex.org.uk/netex}ServiceFrame/"
                                                         "{http://www.netex.org.uk/netex}journeyPatterns/"
                                                         "{http://www.netex.org.uk/netex}ServiceJourneyPattern"):
                        pattern_id = journeyPattern.get("id")
                        servicePattern[pattern_id] = {}
                        for stopPoint in journeyPattern.findall("{http://www.netex.org.uk/netex}pointsInSequence/"
                                                                "{http://www.netex.org.uk/netex}StopPointInJourneyPattern"):
                            servicePattern[pattern_id][int(stopPoint.get("order"))] = stopPoint.get("id")
                            journeyStopPoint2ScheduledStopPoint[stopPoint.get("id")] = (stopPoint.find("{http://www.netex.org.uk/netex}ScheduledStopPointRef").get("ref"), int(stopPoint.get("order")))
                    for stopPoint in frames.findall("{http://www.netex.org.uk/netex}ServiceFrame/"
                                                    "{http://www.netex.org.uk/netex}scheduledStopPoints/"
                                                    "{http://www.netex.org.uk/netex}ScheduledStopPoint"):
                        scheduled_stop_point2_name[stopPoint.get("id")] = stopPoint.findtext("{http://www.netex.org.uk/netex}Name")
                    for stopPoint in frames.findall("{http://www.netex.org.uk/netex}ServiceFrame/"
                                                    "{http://www.netex.org.uk/netex}lines/"
                                                    "{http://www.netex.org.uk/netex}Line"):
                        lineNames.append(stopPoint.findtext("{http://www.netex.org.uk/netex}Name"))
        for passTimeId in passes:
            for passPoint in passes[passTimeId]:
                pattern_id, _, departure = passes[passTimeId][passPoint]
                sched_stop, order = journeyStopPoint2ScheduledStopPoint[passPoint]
                station_name = scheduled_stop_point2_name[sched_stop]
                if order + 1 in servicePattern[pattern_id]:
                    next_pass_point = servicePattern[pattern_id][order+1]
                    next_station_name = scheduled_stop_point2_name[journeyStopPoint2ScheduledStopPoint[next_pass_point][0]]
                    _, arrival, _ = passes[passTimeId][next_pass_point]
                    arrival = time.strptime(arrival, "%H:%M:%S")
                    departure = time.strptime(departure, "%H:%M:%S")
                    if station_name not in connection:
                        connection[station_name] = []
                    connection[station_name].append((
                        next_station_name,
                        departure.tm_sec + departure.tm_min * 60 + departure.tm_hour * 3600,
                        arrival.tm_sec + arrival.tm_min * 60 + arrival.tm_hour * 3600,
                        lineNames
                    ))
    return connection


def parse_cisjr_folder(folder: str) -> dict[str, list[tuple[str, int, int, list[str]]]]:
    connections = {}
    for filename in os.listdir(folder):
        partial_connections = parse_cisjr(folder + os.sep + filename)
        for stationName in partial_connections:
            if stationName not in connections:
                connections[stationName] = []
            for a in partial_connections[stationName]:
                connections[stationName].append(a)
    return connections
