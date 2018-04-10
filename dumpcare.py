#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, render_template_string, send_from_directory, request
import os

app = Flask(__name__, static_url_path='')

with open("flag.txt") as f:
    app.secret_key = f.readline()


@app.route('/')
def root():
    return app.send_static_file('index.html')


def goodbye(comment):
    comment = render_template_string(comment)
    return render_template("result.html", message=comment)


@app.route('/maga', methods=["POST"])
def check():
    if not request.form['name']:
        return goodbye("You didn't provide a name!")
    if not request.form['phone']:
        return goodbye("We need your phone number too!")
    print("%-18s %s" % (request.remote_addr, request.form['phone']))
    # sanitize phone number of special characters using a blacklist
    phone = request.form['phone'].translate({ord(c): None for c in '+() -'})
    # substring the first ten digits
    phone = phone[:10]
    if len(phone) < 10:
        return goodbye("Your phone numbers can't be less than 10 digits!")
    if not phone.isdigit():
        return goodbye("You've entered \"" + request.form['phone']
                       + "\" as your phone number. "
                       + "Nice try, script kiddie, but this application uses server-side verification.")
    return goodbye("Thank you! Trump is caring for you now.")


@app.route("/sauce")
def sauce():
    return send_from_directory('./', 'dump.py')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT', 7777), threaded=True)
