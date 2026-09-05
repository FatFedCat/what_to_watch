from random import randrange
from flask import abort, redirect, render_template, url_for
from opinions_app import app, db
from .models import Opinion
from .forms import OpinionForm


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        # Если в базе пусто - при запросе к главной странице
        # пользователь увидит ошибку 500.
        abort(500)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    # Если ошибок не возникло...
    if form.validate_on_submit():
        # ...то нужно создать новый экземпляр класса Opinion...
        opinion = Opinion(
            # ...и передать в него данные, полученные из формы.
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        # Затем добавить его в сессию работы с базой данных...
        db.session.add(opinion)
        # ...и зафиксировать изменения.
        db.session.commit()
        # Затем переадресовать пользователя на страницу добавленного мнения.
        return redirect(url_for('opinion_view', id=opinion.id))
    # Если валидация не пройдена - просто отрисовать страницу с формой.
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id):
    # Метод get() заменён на get_or_404():
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)