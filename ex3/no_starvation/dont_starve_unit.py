from ex3.vet_hospital import Hospital

class HospitalNoStarvation(Hospital):

    def can_enter(self, pet):
        pet_state = self.species_to_state(pet["species"])

        if self.room_state == "EMPTY":
            return self.waiting_queue and self.waiting_queue[0]["id"] == pet["id"]

        if self.room_state == pet_state:
            for waiting_pet in self.waiting_queue:
                waiting_state = self.species_to_state(waiting_pet["species"])

                if waiting_state != pet_state:
                    return False

                if waiting_pet["id"] == pet["id"]:
                    return True

        return False

    def run(self):
        animals = self.data["workload"]["animals"]
        animals = sorted(
        self.data["workload"]["animals"],
        key=lambda pet: (pet["arrival time"], pet["id"])
        )
        index = 0

        while index < len(animals) or self.waiting_queue or self.resting_room:
            self.remove_finished_pets()

            while index < len(animals) and animals[index]["arrival time"] <= self.time:
                self.waiting_queue.append(animals[index])
                index += 1

            entering = True

            while entering:
                entering = False

                for pet in list(self.waiting_queue):
                    if self.can_enter(pet):
                        self.add_to_room(pet)
                        self.waiting_queue.remove(pet)
                        entering = True

            self.time += 1

