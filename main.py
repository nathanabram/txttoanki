import genanki
import random
import things
import os

from cached_property import cached_property
from genanki import Model
from genanki import Note
from genanki import Deck
from genanki import Package


model_id = random.randrange(1 << 30, 1 << 31)


CSS = """.card {
 font-family: arial;
 font-size: 20px;
 text-align: center;
 color: black;
 background-color: white;
}
.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
}
"""

MY_CLOZE_MODEL = genanki.Model(
    998877661,
    'My Cloze Model',
    fields=[
        {'name': 'Text'},
        {'name': 'Extra'},
    ],
    templates=[{
        'name': 'My Cloze Card',
        'qfmt': '{{cloze:Text}}',
        'afmt': '{{cloze:Text}}<br>{{Extra}}',
    }, ],
    css=CSS,
    model_type=Model.CLOZE)


# Function to allow for generation of notes with simplified cloze tag syntax.
def cloze_replace(string):
    string = string.replace("{{", "{{cloze:")
    i = 1
    if "{{" in string:
        while True:
            if "cloze:" in string:
                string = string.replace("cloze:", f"c{i}::", 1)
                i += 1
            else:
                break
    else:
        string += "{{c1::.}}"
    return string


autocomplete_clozes = True

notes_to_add = []


f = open('/Users/nathank/Library/Mobile Documents/com~apple~CloudDocs/Notes/Flashcards.txt', 'r+')


list_of_notes = f.readlines()


for note in list_of_notes:
    note_text = cloze_replace(note)
    note_extra = ""
    anki_note = genanki.Note(
        model=MY_CLOZE_MODEL,
        fields=[note_text, note_extra]
    )
    notes_to_add.append(anki_note)

anki_deck = genanki.Deck(model_id, "Staging")
anki_package = genanki.Package(anki_deck)


for note in notes_to_add:
    anki_deck.add_note(note)


# Save the deck to a file
anki_package.write_to_file("staging_deck.apkg")
os.system(f"cd ~/Library/Mobile\ Documents/com~apple~CloudDocs/Notes; cat Flashcards.txt >> notes_added_to_anki.txt")
f.truncate(0)
f.close()

print("Created deck with {} flashcards".format(len(anki_deck.notes)))
