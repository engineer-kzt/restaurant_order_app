import csv


def foodorder_reading(filname):
    with open(filname, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        order_list = []
        for row in reader:
            order_list.append(row)
        return order_list


x = foodorder_reading("pasta_menue/注文履歴.csv")

print(x)


def calcu_order_history(order_list):
    calcu_result = []
    for element in order_list:
        calcu_mult = int(element["数量"]) * int(element["価格"])
        calcu_result.append(calcu_mult)
    return calcu_result


y = calcu_order_history(x)
print(y)
