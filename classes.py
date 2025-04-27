import json

class Person:
    def __init__(self, name, password, tz, phone, numGame, numWin, words):
        self.name = name
        self.password = password
        self.tz = tz
        self.phone = phone
        self.numGame = numGame
        self.numWin = numWin
        self.words = set(words)  # כך לא יוצגו מילים כפולות

    def to_dict(self):
        return {
            "name": self.name,
            "password": self.password,
            "tz": self.tz,
            "phone": self.phone,
            "numGame": self.numGame,
            "numWin": self.numWin,
            "words": list(self.words)  # המרת הסט לרשימה
        }

def save_to_json(persons, users):
    with open(users, 'w', encoding='utf-8') as json_file:
        json.dump([person.to_dict() for person in persons], json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    persons = []

    person1 = Person("Nechami", "123", "111111111", "050-1111111", "0", "0", [])
    person2 = Person("Yael", "456", "222222222", "050-2222222", "0", "0", [])
    person3 = Person("Nomi", "789", "333333333", "050-3333333", "0", "0", [])

    persons.append(person1)
    persons.append(person2)
    persons.append(person3)

    # Save to JSON
    save_to_json(persons, 'users.json')
