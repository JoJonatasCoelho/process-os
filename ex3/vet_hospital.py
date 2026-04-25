from shared.json_reader import load_json
#IREI ASSUMIR QUE NÃO É NECESSÁRIO IMPLEMENTAR VALIDAÇÃO DE DADOS/ENTRADA JÁ QUE O ENUNCIADO NÃO PEDE
# E QUE OS ANIMAIS ESTÃO ORDENADOS NA ORDEM DE CHEGADA

class Hospital:
    def __init__(self, file_path):
        self.data = load_json(file_path)

        self.waiting_queue = []
        self.resting_room = []
        self.finished_pets = []

        self.room_state = self.data["room"]["initial sign state"]
        self.time = 0

    def species_to_state(self, species):
        if species == "DOG":
            return "DOGS"
        return "CATS"

    def same_group(self, pet):
        return self.species_to_state(pet["species"]) == self.room_state

    def room_is_empty(self):
        return len(self.resting_room) == 0

    def add_to_room(self, pet):
        self.resting_room.append({
            **pet,
            "start_time": self.time,
            "exit_time": self.time + pet["rest duration"]
        })

        self.room_state = self.species_to_state(pet["species"])

    def remove_finished_pets(self):
        still_resting = []

        for pet in self.resting_room:
            if pet["exit_time"] <= self.time:
                self.finished_pets.append(pet)
            else:
                still_resting.append(pet)

        self.resting_room = still_resting

        if self.room_is_empty():
            self.room_state = "EMPTY"

    def print_result(self, title):
        print("\n" + title)
        print("-" * len(title))

        for pet in sorted(self.finished_pets, key=lambda p: p["id"]):
            print(
                f'{pet["id"]} ({pet["species"]}) '
                f'entrou em {pet["start_time"]} '
                f'e saiu em {pet["exit_time"]}'
            )

