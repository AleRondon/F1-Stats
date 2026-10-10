# F1 Stats

This is my first python project.

The purpose of this project is to keep the standings and basic analysis of the F1 Championship.

Updates and fixes will be on a best effort basis.


## Basic Concepts

This app will be made with the main purpose of following the F1 Championship, by not only giving a general standing of both drivers' and constructors', but also including some statistical information such as: 
- Percentage of points for 1st place (both Drivers and Constructors).
- Mathematical change of winning the Championship.
- Head to Head comparison of drivers for any type of event -GP, Qualification, Sprint, Sprint Qualification- (Including count -times ahead-, average position, and average delta).

The inputs will be the results of each race, including position by event (Round number, Event Type, Position and timings by driver). There must be also a starter input with drivers information (Driver Name, abbreviation, Car number & Team),  and round information (Number of rounds of the championship, Name and types of events included in the round -GP, Qualification, Sprint, Sprint Qualification-).

There should be a way to upgrade mid-season the drivers and team (Red Bull Clause). Adapting the points to the driver, and to the right team during the season.

The application should also allows to modify the placement of drivers post race, this should work by specifying the drivers that got disqualified, and then recalculating the total in the standing.

The application should calculate then the general standings of the drivers, general standings of the constructors and any other necessary calculation or tables to support the statistical information required. When calculating the general standings, the application should take into account the tie braker rules of the F1 championship.

## Desired Results

- The application should be developed in Python and is desired to be deployed as a docker container.
- The database of the application should be stored in PostgreSQL. 
- The interface could be either a windows application user interface with support for graphs and different inputs, or a web interface.