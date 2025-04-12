class Result:
    def __init__(self,car_position:int,car_number:int,team:int,round_name: int,round_type: str,time: str):
       self.car_position: int = car_position
       self.car_number: int = car_number
       self.team: int = team
       self.round_name: int = round_name
       self.round_type: str = round_type
       self.time: str = time