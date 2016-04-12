import hashlib
import os
import string

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
)

app = Flask(__name__)
app.config.from_pyfile('config.py')
if 'VERSUSHORSE_CONFIG' in os.environ:
    app.config.from_envvar('VERSUSHORSE_CONFIG')


def shaify(text):
    h = hashlib.sha256()
    h.update(text)
    # Probably an easier way to turn this into an int, but this works.
    return int(h.hexdigest(), 16)


def shawin(first, second):
    first_hash = shaify(first.lower())
    second_hash = shaify(second.lower())
    combined_hash = shaify("%s%s" % (first, second))
    first_diff = abs(first_hash - combined_hash)
    second_diff = abs(second_hash - combined_hash)
    if first_diff < second_diff:
        return first
    # No check for equal because not much more likely than a collision
    return second


def sanitize(subdomain):
    valid_characters = string.ascii_letters + string.digits + '-'
    clean = ''.join(ch for ch in subdomain if ch in valid_characters)
    clean = clean.strip("-")
    return clean


def is_sbvp(text):
    text = text.lower()
    return "stealth" in text and "bomb" in text


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/", subdomain="<attacker>")
def results(attacker):
    if session.get('flavor'):
        attacker = session['flavor']
        del session['flavor']
    victor = shawin(attacker, 'horse')
    if is_sbvp(attacker):
        return render_template("sbvp.html")
    elif attacker == 'www':
        # DNS and/or my browser is misbehaving and directing raw versus.horse
        # to www.versus.horse - sadly we will never know who wins in a fight
        # between www and a horse.
        return render_template("index.html")
    else:
        return render_template("fight.html", attacker=attacker, victor=victor)


@app.route("/api/compare/<attacker>", defaults={'attackee': 'horse'},
           methods=['GET', 'POST'])
@app.route("/api/compare/<attacker>/<attackee>", methods=['GET', 'POST'])
def api_compare(attacker, attackee):

    winner = shawin(attacker, attackee)
    result = {
        'attacker': attacker,
        'attackee': attackee,
        'verdict': winner,
    }
    return jsonify(result)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/fight", methods=['GET', 'POST'])
def fight():
    attacker = request.values['attacker']
    if not attacker:
        attacker = 'nothing'
    server = app.config['SERVER_NAME']
    session['flavor'] = attacker
    return redirect("http://%s.%s" % (sanitize(attacker), server))
