test_sentences = {
    "irrelevant": "Pouet Pouet, camembert ! ",
    "purchase": "Acheter",
    "find-restaurant": "Trouver un restaurant",
    "find-hotel": "Trouver un hotel",
    "find-around-me": "Trouver le plus proche",
    "find-flight": "Trouver un avion",
    "find-train": "Trouver un train",
    "provide-showtimes": "Veux la météo"
}

test_dataset = [
    {"intent": "irrelevant", "sentence": "L Esclavagisme moderne"},
    {"intent": "purchase", "sentence": "Acheter"},
    {"intent": "find-hotel", "sentence": "Trouver un hotel"},
    {"intent": "find-restaurant", "sentence": "Trouver un restaurant"},
    {"intent": "find-around-me", "sentence": "Trouver autour de moi"},
    {"intent": "find-flight", "sentence": "Trouver un avion"},
    {"intent": "find-train", "sentence": "Trouver un train"},
    {"intent": "provide-showtimes", "sentence": "Vouloir la météo"},
    {"intent": "irrelevant", "sentence": "Dictateur"},
    {"intent": "irrelevant", "sentence": "Master >> Main"}
]

all_labels = sorted([
    "irrelevant",
    "purchase",
    "find-restaurant",
    "find-hotel",
    "find-around-me",
    "find-flight",
    "find-train",
    "provide-showtimes"
])
