from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm
from secret import CLIENT_TOKEN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'haoshlf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_pets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def show_homepage():
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)

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
            photo_url=photo_url,
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
