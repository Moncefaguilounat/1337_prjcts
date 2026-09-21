
import sys

print("=== Inventory System Analysis ===")

inventory = dict()
total = 0
types = 0

for arg in sys.argv[1:]:
    key, value = arg.split(':')
    inventory[key] = int(value)

for count in inventory.values():
    total += count
    types += 1

print(f"Total items in inventory: {total}")
print(f"Unique item types: {len(inventory)}\n")

print("=== Current Inventory ===")

sum = 0
for value in inventory.values():
    sum += value
for item, count in inventory.items():
    percentage = (count / total) * 100
    print(
        f"{item}: {count} unit{'s' if count > 1 else ''} ({percentage:.1f}%)"
    )

print()
print("=== Inventory Statistics ===")

most = 0
least = 0
for item, value in inventory.items():
    if value > most:
        most = value
        m_item = item

least = most
for item, value in inventory.items():
    if value < least:
        least = value
        l_item = item

print(f"Most abundant: {m_item} ({most} unit{'s' if most > 1 else ''})")
print(f"Least abundant: {l_item} ({least} unit{'s' if least > 1 else ''})\n")

moderate = dict()
scarce = dict()

for item, count in inventory.items():
    if count >= 5:
        moderate[item] = count
    else:
        scarce[item] = count

print("=== Item Categories ===")

print("Moderate:", moderate)
print("Scarce:", scarce)

print()
print("=== Management Suggestions ===")

restock = []
for item, value in inventory.items():
    if value == least:
        restock.append(item)
print("Restock needed: ", restock)

print()
print("=== Dictionary Properties Demo ===")

keys = []
values = []
for key in inventory.keys():
    keys.append(key)
for value in inventory.values():
    values.append(value)

print("Dictionary keys: ", keys)
print("Dictionary values: ", values)

sample = "sword"
if sample in inventory:
    print(f"Sample lookup - {sample} in inventory: ",True)
else:
    print(f"Sample lookup - {sample} in inventory: ",False)
