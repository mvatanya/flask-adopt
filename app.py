from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm, SearchPetFinderForm
from petfinder_api import PetFinder

app = Flask(__name__)
app.config['SECRET_KEY'] = 'haoshlf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_pets' #location where the database is
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app) #this is to connect app.py to the location that line9 tell where database is
db.create_all()

# panang = Pet(name='Panang', species='Dog', photo_url='https://lh3.googleusercontent.com/LuzElISBGNY97YOthkFubM9s1_2C-DpYZsUudUpKUTLR90AKWyQeLwObWeO8WB8nja2YCJiZLoj_ildHlCeXd1xBmiMactT4pqp-eVIWsBELC3aMw156qxB4owuAakkPfJvtKEdhGtxVT9jiKwg_d5oozGlctBRsscBNfkLOtcX4OAxBzCjn4QkyU2o5ce304QCZ4rcXvKn9IHgQxgx8fDBSfSgo6BjgBoA1aYaGwf-sG9UouhE6mkq0r4geZtygI9z0RAtMXiIdIjcyHS0Id4Px_ZyV5UGjeyPyHAxdZoUFcqI4DcMfxFEY36xAvKC0tWNAtfCZ0CzCOURjcem-GJ4ydPD3uMC0xqGnjdEkZJPxmygnGmY6p2WuaP4mh3skyPQrv1TrHlF8oJPk2yHJHjaiUY5LI60-R8I9_qIkJxENQyb7Fqy3uHlMx1RdMjWc7-zBrhYyK3PSPd2QLwb_WiKpQnfqYUV7Iz9KGNtFiArlupktMIJAsxrhgKcCb99gpyIuZenmQiJTaCS9_jhfzAjNm5iiTymCjysprKmWSxlmRQx5OstVYvy8Jru-YV-MsUQaydvx6IvYTncHP30pwg3FzIoRgCZZy0wu9fSDBHaZIVLfiAdphw5cWdC9KE9_nHAqV_MzMt5ifG-1Tsh6uQOG7ajzpeY=w319-h367-no', age=1)
# db.session.add(panang)
# db.session.commit()

@app.route('/')
def show_homepage():
    pets_finder_list = PetFinder.get_random_pets()['animals']
   
    pets = Pet.query.all()
    pet_finder_pets = []

    for pet in pets_finder_list:
        try:
            photo_url = pet['photos'][0]['small']
        except IndexError:
            photo_url = None

        obj = {
            'name': pet['name'],
            'age': pet['age'],
            'photo_url': photo_url,
            'species': pet['species']
        }
        pet_finder_pets.append(obj)

    return render_template('homepage.html', pets=pets, pet_finder_pets=pet_finder_pets)

@app.route('/pets/new', methods=['GET', 'POST'])
def add_pet_form():
    """all fields besides photo and notes are required 
    
    allowed species are Dog, Cat, Porcupine. On sucess redirects to homepage"""

    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url or None,
            age=age,
            notes=notes
        )

        db.session.add(pet)
        db.session.commit()

        flash(f'{name} has been put up for adoptions :D')

        return redirect("/")

    else:
        return render_template('forms/pet_add_form.html', form=form)


@app.route('/pets/<pet_id>', methods=["GET", "POST"])
def show_pet_details(pet_id):
    """Shows pet details and allows some of them to be edited
    (notes, photo and availability can be edited)
    """

    pet = Pet.query.get_or_404(pet_id)

    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()

        flash(f'{pet.name} has been updated :D')
        return redirect(f'/')

    else:
        return render_template('pet_details.html', pet=pet, form=form)

@app.route('/search', methods=['GET'])
def search_pet():

    form = SearchPetFinderForm()
    if form.validate_on_submit():
        pet_finder_list = PetFinder.get_search_results(
            species=form.species.data, 
            age=form.age.data,
            name=form.name.data,
            )
        pets_finder_list = PetFinder.get_random_pets()['animals']
   
        pet_finder_pets = []

        for pet in pets_finder_list:
            try:
                photo_url = pet['photos'][0]['small']
            except IndexError:
                photo_url = None

            obj = {
                'name': pet['name'],
                'age': pet['age'],
                'photo_url': photo_url,
                'species': pet['species']
            }
        pet_finder_pets.append(obj)
        return render_template('search_results.html', pets=pet_finder_list)
    else:
        return render_template('forms/search_form.html', form=form)