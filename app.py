from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import json
import time

app = Flask(__name__)

# Word banks with hints
words_with_hints = {
    'easy': [
        {'word': 'apple', 'hint': 'A popular fruit that keeps doctors away.'},
        {'word': 'banana', 'hint': 'A long, yellow fruit loved by monkeys.'},
        {'word': 'grape', 'hint': 'Small, round, and often made into wine.'},
        {'word': 'peach', 'hint': 'A soft fruit with fuzzy skin.'},
        {'word': 'melon', 'hint': 'A large, juicy fruit with a hard rind.'},
        {'word': 'lemon', 'hint': 'A sour yellow fruit.'},
        {'word': 'plum', 'hint': 'A small, purple or red fruit with a pit.'},
        {'word': 'kiwi', 'hint': 'A small, brown fruit with green flesh.'},
        {'word': 'mango', 'hint': 'Known as the king of fruits in India.'},
        {'word': 'pear', 'hint': 'A green fruit with a smooth texture.'},
        {'word': 'fig', 'hint': 'A small, sweet fruit often dried.'},
        {'word': 'date', 'hint': 'A sweet fruit often found in deserts.'},
        {'word': 'lime', 'hint': 'A small green fruit, often used in drinks.'},
        {'word': 'berry', 'hint': 'A small, juicy fruit often found in bunches.'}
    ],
    'medium': [
        {'word': 'strawberry', 'hint': 'A fruit often associated with summer and has seeds on the outside.'},
        {'word': 'blueberry', 'hint': 'A fruit that grows on bushes and can turn your tongue purple.'},
        {'word': 'raspberry', 'hint': 'A fruit that belongs to the rose family and has drupelets.'},
        {'word': 'pineapple', 'hint': 'A fruit with a crown and multiple eyes.'},
        {'word': 'coconut', 'hint': 'Its interior can be grated or used for milk, and it has a fibrous husk.'},
        {'word': 'papaya', 'hint': 'A tropical fruit with black seeds and orange flesh, rich in enzymes.'},
        {'word': 'passion', 'hint': 'A fruit with a wrinkled exterior when ripe and edible seeds.'},
        {'word': 'apricot', 'hint': 'A stone fruit related to plums, often dried.'},
        {'word': 'cherry', 'hint': 'A drupe fruit often used in desserts and drinks, usually red or black.'},
        {'word': 'lychee', 'hint': 'A fruit with a rough shell and translucent flesh, native to China.'},
        {'word': 'nectarine', 'hint': 'A fuzz-free relative of the peach.'},
        {'word': 'persimmon', 'hint': 'A fruit that can be astringent if not ripe.'},
        {'word': 'blackberry', 'hint': 'A fruit that is technically an aggregate of drupelets.'},
        {'word': 'mulberry', 'hint': 'A fruit that grows on trees and resembles a cluster of tiny grapes.'}
    ],
    'hard': [
        {'word': 'pomegranate', 'hint': 'A fruit whose name means "seeded apple" in Latin.'},
        {'word': 'dragonfruit', 'hint': 'A fruit from a cactus with vibrant skin and speckled flesh.'},
        {'word': 'cranberry', 'hint': 'A fruit that is often harvested by flooding fields.'},
        {'word': 'jackfruit', 'hint': 'The world’s largest tree-borne fruit, with a spiky exterior.'},
        {'word': 'tamarind', 'hint': 'A pod-like fruit used in both sweet and savory dishes, native to Africa.'},
        {'word': 'elderberry', 'hint': 'A fruit used in syrups and remedies, grows in clusters on shrubs.'},
        {'word': 'boysenberry', 'hint': 'A hybrid fruit named after a Californian farmer.'},
        {'word': 'cantaloupe', 'hint': 'A melon with a netted rind and orange flesh.'},
        {'word': 'honeydew', 'hint': 'A melon with a smooth rind and green flesh.'},
        {'word': 'gooseberry', 'hint': 'A fruit that grows on thorny bushes, often used in pies.'},
        {'word': 'rhubarb', 'hint': 'Technically a vegetable, its stalks are used in desserts.'},
        {'word': 'kumquat', 'hint': 'A citrus fruit eaten whole, peel and all.'},
        {'word': 'quince', 'hint': 'A hard fruit that turns pink when cooked.'},
        {'word': 'starfruit', 'hint': 'A fruit known for its cross-section shape.'}
    ]
}


guessed_word = []
word = ""
hint = ""
attempts = 0
message = ""
level_selected = False
leaderboard_file = 'leaderboard.json'

# Load leaderboard
def load_leaderboard():
    try:
        with open(leaderboard_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save leaderboard
def save_leaderboard(leaderboard):
    with open(leaderboard_file, 'w') as file:
        json.dump(leaderboard, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    global guessed_word, word, hint, attempts, message, level_selected

    if request.method == "POST":
        if request.form.get("action") == "play_again":
            level_selected = False
            message = ""
            return render_template("level.html")

        if not level_selected:
            level = request.form.get('level')
            if level:
                level_selected = True
                if level == 'easy':
                    attempts = 15
                elif level == 'medium':
                    attempts = 10
                else:
                    attempts = 5

                selected_word = random.choice(words_with_hints[level])
                word = selected_word['word']
                hint = selected_word['hint']
                guessed_word = ['_'] * len(word)
                message = "Choose a letter to start guessing!"
            return render_template("index.html", guessed_word=' '.join(guessed_word), attempts=attempts, message=message, hint=hint)

        letter = request.form.get('letter')
        if letter:
            letter = letter.lower()
            if letter in word:
                for i, l in enumerate(word):
                    if l == letter:
                        guessed_word[i] = letter
                message = "✅ Great guess!"
            else:
                attempts -= 1
                message = f"❌ Wrong! Attempts left: {attempts}"
        
        if '_' not in guessed_word:
            message = f"🎉 Congratulations! You found the word: {word}"
            leaderboard = load_leaderboard()
            leaderboard.append({'word': word, 'attempts_left': attempts})
            save_leaderboard(leaderboard)
        elif attempts <= 0:
            message = f"❌ You've run out of attempts! The word was: {word}"
        
        return render_template("index.html", guessed_word=' '.join(guessed_word), attempts=attempts, message=message, hint=hint)

    return render_template("level.html")

@app.route("/leaderboard")
def leaderboard():
    leaderboard = load_leaderboard()
    return render_template("leaderboard.html", leaderboard=leaderboard)

if __name__ == "__main__":
    app.run(debug=True)
