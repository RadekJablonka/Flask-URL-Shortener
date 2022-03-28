from datetime import datetime, timedelta
from core.models import ShortUrls
from core import app, db
from random import choice
import string
import validators
from flask import render_template, request, flash, redirect, url_for


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return "".join(
        choice(string.ascii_letters + string.digits) for _ in range(num_of_chars)
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"].replace(" ", "")
        short_id = request.form["custom_id"]
        expiration_date = request.form["expiration_date"]

        if (
            short_id
            and ShortUrls.query.filter_by(short_id=short_id).first() is not None
        ):
            flash("Please enter different Custom Short ID!")

            return redirect(url_for("index"))

        if not url or not bool(validators.url(url)):
            flash("Valid URL is required!")
            return redirect(url_for("index"))

        if len(expiration_date) > 0:
            try:
                int(expiration_date)
            except ValueError:
                flash("Please enter the expiration time in minutes")
                return redirect(url_for("index"))

        if int(expiration_date) <= 0:
            flash("Expiration time should be greater than zero")
            return redirect(url_for("index"))

        if not short_id:
            short_id = generate_short_id(8)

        expiration_in_minutes = int(expiration_date) if expiration_date else 15
        new_link = ShortUrls(
            original_url=url,
            short_id=short_id,
            created_at=datetime.now(),
            expiration_date=datetime.now() + timedelta(minutes=expiration_in_minutes),
        )
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + short_id

        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


@app.route("/<short_id>")
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link and link.expiration_date < datetime.now():
        flash(f"Custom short id {short_id} has expired")
        return redirect(url_for("index"))
    elif link:
        return redirect(link.original_url)
    else:
        return redirect(url_for("index"))
