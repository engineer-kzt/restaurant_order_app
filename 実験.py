import csv


def foodmenu_to_dict(filename):
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        new_reader = {}
        start_num = 1001  # キーの開始番号
        for i, row in enumerate(reader):
            key = start_num + i
            new_reader[key] = row
    return new_reader


x = foodmenu_to_dict("menu/food_menu.csv")
print(x)
