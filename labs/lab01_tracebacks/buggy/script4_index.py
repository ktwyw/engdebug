# Script 4: compute the change between consecutive readings. It crashes at the end of the list.
readings = [71.2, 72.0, 70.8, 73.1]

changes = []
for i in range(len(readings)):
    changes.append(readings[i + 1] - readings[i])
print(changes)
