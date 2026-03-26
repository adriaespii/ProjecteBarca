import json
import random

teams = {
    "FC Barcelona": [
        ("M. ter Stegen", "POR", 89, 35000000, 150000),
        ("R. Araujo", "DEF", 87, 70000000, 130000),
        ("J. Koundé", "DEF", 85, 60000000, 120000),
        ("P. Cubarsí", "DEF", 81, 25000000, 30000),
        ("A. Balde", "DEF", 82, 40000000, 60000),
        ("Pedri", "MIG", 86, 80000000, 140000),
        ("F. de Jong", "MIG", 87, 75000000, 180000),
        ("Dani Olmo", "MIG", 85, 60000000, 120000),
        ("Lamine Yamal", "DEL", 86, 120000000, 80000),
        ("R. Lewandowski", "DEL", 88, 15000000, 200000),
        ("Raphinha", "DEL", 85, 50000000, 110000),
        ("Iñaki Peña", "POR", 78, 8000000, 40000),
        ("A. Christensen", "DEF", 83, 40000000, 100000),
        ("Gavi", "MIG", 84, 70000000, 100000),
        ("Fermín López", "MIG", 80, 20000000, 40000),
        ("Ferran Torres", "DEL", 82, 35000000, 90000),
        ("I. Martínez", "DEF", 82, 5000000, 60000),
        ("Casadó", "MIG", 75, 5000000, 15000),
        ("A. Fati", "DEL", 79, 15000000, 70000),
        ("Pau Víctor", "DEL", 74, 3000000, 10000)
    ],
    "Real Madrid": [
        ("T. Courtois", "POR", 90, 35000000, 250000),
        ("A. Rüdiger", "DEF", 88, 25000000, 180000),
        ("E. Militão", "DEF", 86, 70000000, 150000),
        ("D. Carvajal", "DEF", 85, 12000000, 150000),
        ("F. Mendy", "DEF", 83, 22000000, 120000),
        ("F. Valverde", "MIG", 89, 120000000, 250000),
        ("J. Bellingham", "MIG", 91, 180000000, 300000),
        ("A. Tchouaméni", "MIG", 86, 100000000, 180000),
        ("E. Camavinga", "MIG", 85, 90000000, 160000),
        ("Vini Jr.", "DEL", 91, 150000000, 350000),
        ("K. Mbappé", "DEL", 92, 180000000, 400000),
        ("Rodrygo", "DEL", 87, 100000000, 200000),
        ("Brahim Díaz", "DEL", 83, 35000000, 100000),
        ("L. Modrić", "MIG", 86, 5000000, 150000),
        ("A. Güler", "MIG", 78, 15000000, 40000),
        ("A. Lunin", "POR", 81, 16000000, 60000)
    ],
    "Manchester City": [
        ("Ederson", "POR", 88, 40000000, 180000),
        ("R. Dias", "DEF", 89, 80000000, 200000),
        ("J. Stones", "DEF", 86, 38000000, 160000),
        ("M. Akanji", "DEF", 85, 42000000, 140000),
        ("J. Gvardiol", "DEF", 86, 75000000, 180000),
        ("K. Walker", "DEF", 84, 13000000, 150000),
        ("Rodri", "MIG", 91, 110000000, 250000),
        ("K. De Bruyne", "MIG", 90, 60000000, 350000),
        ("P. Foden", "MIG", 88, 110000000, 200000),
        ("B. Silva", "MIG", 88, 80000000, 200000),
        ("M. Kovačić", "MIG", 84, 30000000, 140000),
        ("E. Haaland", "DEL", 92, 180000000, 380000),
        ("J. Doku", "DEL", 84, 65000000, 120000),
        ("J. Grealish", "DEL", 85, 60000000, 180000),
        ("R. Lewis", "DEF", 80, 35000000, 80000)
    ],
    "Arsenal": [
        ("D. Raya", "POR", 85, 30000000, 100000),
        ("W. Saliba", "DEF", 87, 80000000, 180000),
        ("Gabriel", "DEF", 86, 65000000, 150000),
        ("B. White", "DEF", 84, 55000000, 120000),
        ("O. Zinchenko", "DEF", 82, 38000000, 100000),
        ("D. Rice", "MIG", 88, 110000000, 200000),
        ("M. Ødegaard", "MIG", 88, 90000000, 200000),
        ("B. Saka", "DEL", 88, 130000000, 250000),
        ("G. Martinelli", "DEL", 85, 80000000, 150000),
        ("G. Jesus", "DEL", 84, 65000000, 180000),
        ("K. Havertz", "MIG", 85, 60000000, 160000),
        ("L. Trossard", "DEL", 84, 35000000, 120000),
        ("R. Sterling", "DEL", 83, 35000000, 180000),
        ("T. Partey", "MIG", 84, 18000000, 150000)
    ],
    "Bayern Munich": [
        ("M. Neuer", "POR", 87, 10000000, 200000),
        ("D. Upamecano", "DEF", 84, 45000000, 160000),
        ("A. Davies", "DEF", 85, 60000000, 180000),
        ("M. de Ligt", "DEF", 85, 65000000, 170000),
        ("J. Kimmich", "MIG", 88, 60000000, 230000),
        ("L. Goretzka", "MIG", 86, 40000000, 180000),
        ("J. Musiala", "MIG", 89, 130000000, 200000),
        ("S. Sané", "DEL", 86, 70000000, 190000),
        ("K. Coman", "DEL", 85, 65000000, 180000),
        ("M. Olise", "DEL", 84, 65000000, 120000),
        ("H. Kane", "DEL", 91, 110000000, 300000),
        ("S. Gnabry", "DEL", 84, 45000000, 170000),
        ("J. Palhinha", "MIG", 85, 50000000, 150000),
        ("T. Muller", "DEL", 84, 12000000, 160000)
    ],
    "PSG": [
        ("G. Donnarumma", "POR", 88, 40000000, 200000),
        ("Marquinhos", "DEF", 87, 60000000, 220000),
        ("A. Hakimi", "DEF", 85, 65000000, 180000),
        ("N. Mendes", "DEF", 84, 60000000, 150000),
        ("L. Hernández", "DEF", 84, 45000000, 160000),
        ("Vitinha", "MIG", 86, 50000000, 140000),
        ("W. Zaïre-Emery", "MIG", 84, 60000000, 100000),
        ("F. Ruiz", "MIG", 83, 30000000, 120000),
        ("O. Dembélé", "DEL", 86, 60000000, 250000),
        ("B. Barcola", "DEL", 83, 50000000, 110000),
        ("G. Ramos", "DEL", 83, 50000000, 150000),
        ("M. Asensio", "DEL", 82, 20000000, 140000)
    ],
    "Inter Milan": [
        ("Y. Sommer", "POR", 85, 5000000, 100000),
        ("A. Bastoni", "DEF", 87, 70000000, 140000),
        ("F. Dimarco", "DEF", 85, 50000000, 120000),
        ("B. Pavard", "DEF", 84, 50000000, 130000),
        ("H. Çalhanoğlu", "MIG", 86, 40000000, 150000),
        ("N. Barella", "MIG", 87, 80000000, 180000),
        ("D. Frattesi", "MIG", 83, 35000000, 100000),
        ("L. Martínez", "DEL", 89, 110000000, 200000),
        ("M. Thuram", "DEL", 84, 60000000, 140000),
        ("M. Taremi", "DEL", 82, 10000000, 100000),
        ("P. Zieliński", "MIG", 83, 20000000, 110000)
    ],
    "Liverpool": [
        ("Alisson", "POR", 89, 32000000, 220000),
        ("V. van Dijk", "DEF", 89, 32000000, 250000),
        ("T. Alexander-Arnold", "DEF", 86, 70000000, 200000),
        ("A. Robertson", "DEF", 85, 35000000, 180000),
        ("I. Konaté", "DEF", 84, 45000000, 130000),
        ("A. Mac Allister", "MIG", 86, 65000000, 160000),
        ("D. Szoboszlai", "MIG", 84, 75000000, 150000),
        ("R. Gravenberch", "MIG", 81, 35000000, 110000),
        ("M. Salah", "DEL", 89, 65000000, 350000),
        ("L. Díaz", "DEL", 85, 75000000, 150000),
        ("D. Jota", "DEL", 85, 50000000, 160000),
        ("D. Núñez", "DEL", 84, 65000000, 160000),
        ("C. Gakpo", "DEL", 83, 50000000, 140000),
        ("F. Chiesa", "DEL", 84, 35000000, 150000)
    ]
}

players = []
id_counter = 1

for team, members in teams.items():
    for name, pos, rating, price, base_salary in members:
        
        # Determine status for logic. Barcelona will be on 'team' initially
        inTeam = (team == "FC Barcelona")
        status = 'starter' if (inTeam and id_counter <= 11) else ('bench' if inTeam else 'none')
        
        player = {
            "id": id_counter,
            "name": name,
            "position": pos,
            "rating": rating,
            "price": price,
            "salary": base_salary,
            "inTeam": inTeam,
            "status": status,
            "club": team
        }
        players.append(player)
        id_counter += 1

with open('src/players.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, ensure_ascii=False, indent=4)

print("players.json generated with", len(players), "players.")
