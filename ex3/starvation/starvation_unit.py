from ex3.vet_hospital import Hospital

class HospitalStarvation(Hospital):
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
                pet = animals[index]

                if self.room_state == "EMPTY" or self.same_group(pet):
                    self.add_to_room(pet)
                else:
                    self.waiting_queue.append(pet)

                index += 1

            new_queue = []

            for pet in self.waiting_queue:
                if self.room_state == "EMPTY" or self.same_group(pet):
                    self.add_to_room(pet)
                else:
                    new_queue.append(pet)

            self.waiting_queue = new_queue
            self.time += 1

