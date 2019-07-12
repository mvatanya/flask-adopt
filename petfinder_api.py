from secret import CLIENT_TOKEN
import requests

class PetFinder():

    @classmethod
    def get_random_pets(cls):
        resp = requests.get(
            "https://api.petfinder.com/v2/animals",
            params={"sort": "random", "status": "adoptable", "limit": 10},
            headers={'Authorization': f"Bearer {CLIENT_TOKEN}"}
        )
        return resp.json()

    @classmethod
    def get_search_results(cls, age, species, name):
        params = {"sort": "recent", "status": "adoptable", "limit": 10}

        if age:
            params['age'] = age
        if species:
            params['species'] = species
        if name:
            params['name'] = name

        resp = requests.get(
            "https://api.petfinder.com/v2/animals",
            params=params,
            headers={'Authorization': f"Bearer {CLIENT_TOKEN}"}
        )

        return resp.json()


# print(resp.json())

