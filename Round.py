class Round:
    def __init__(self,round_name:str,round_number:int,country:str,circuit:str,round_date:str,round_type:str):
        self.round_name: str = round_name
        self.round_number: int = round_number
        self.country: str = country
        self.circuit: str = circuit
        self.round_date: str = round_date
        self.round_type: str = round_type