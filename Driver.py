class Driver:
    def __init__(self,name: str,trigramme: str,car_number: int,nationality: str):
        self.name: str = name
        self.trigramme: str = trigramme
        self.car_number: int = car_number
        self.nationality: str = nationality
    
    def updateCarNumber(self,new_car_number: int):
        self.car_number = new_car_number

