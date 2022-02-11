from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
            created_by = current_user
        )
        db.session.add(new_store)
        db.session.commit()

        flash('Success! New Store Added')
        return redirect(url_for('main.store_detail', store_id = new_store))
    else: 
        return render_template('new_store.html', form = form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()


    if form.validate_on_submit():
        new_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data, 
            photo_url = form.photo_url.data,
            store_id = form.store.data.id,
            created_by = current_user

        )
        db.session.add(new_item)
        db.session.commit()
        flash('Success! New Item Added')
        return redirect(url_for('main.item_detail', item_id = new_item))
    else:
        return render_template('new_item.html', form = form)


@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm()

    if form.validate_on_submit():
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()
        

        flash('Success! Store Updated')
        store = GroceryStore.query.get(store_id)
        return redirect(url_for('main.store_detail',  store_id = store, store = store))
    else: 

    # TODO: Send the form to the template and use it to render the form fields
        store = GroceryStore.query.get(store_id)
        print("form not submitted")
        return render_template('store_detail.html', store = store, form = form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm()
    if form.validate_on_submit():
        form.populate_obj(item)
        # db.session.add(item)
        db.session.commit()
        flash('Success! Item Updated')
        return redirect(url_for('main.item_detail', item_id = item))
    else:
    # TODO: Send the form to the template and use it to render the form fields
        item = GroceryItem.query.get(item_id)
        return render_template('item_detail.html', item=item, form = form)

