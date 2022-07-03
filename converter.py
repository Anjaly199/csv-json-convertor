import csv
import json


# Assumptions
# 1. The csv column format for each level stays same, no matter how many level
# 2. The csv records are ordered like now , for parent-child relationship .
#    That is, all 2 level records  comes before all 3 level  come before 4 level records etc.

# a node in the tree , represent each level
class Level(dict):
  def __init__(self, label, id, link, children=None):
    super().__init__()
    self.__dict__ = self
    self.label = label
    self.id = id
    self.link = link
    self.children = list(children) if children is not None else []

  def addNode(self, obj):
    self.children.append(obj)

  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__,
                      sort_keys=True, indent=4)


def getNewNode(row, col):
  new_node = Level(row[col], row[col + 1], row[col + 2])


def addNodes(current_node, nodes, index):
  node = nodes[index]

  if index == nodes.__len__() - 1:
    current_node.children.append(node)
    return

  if current_node.children.__len__() < 1:
    current_node.children.append(nodes[index + 1])
  else:
    for child in current_node.children:
      if child.id == nodes[index].id:
        addNodes(child, nodes, index + 1)


def processRow(col_count, root, row):
  col = 1
  nodes = []
  while (col < col_count): # fetch all nodes in the row
    if len(row[col]) == 0:
      break
    nodes.append(Level(row[col], row[col + 1], row[col + 2]))
    col += 3;

  if nodes.__len__() > 0:
    addNodes(root, nodes, 1)  # insert into the tree

# read each line of csv
def readCsv():
  root = ()
  with open('/app/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    col_count = 0
    for row in csv_reader:

      col_count = row.__len__()

      # skip header
      if line_count == 0:
        line_count += 1
        continue

      if (line_count == 1):  # create root node in the tree
        root = Level(row[1], row[2], row[3])
      else:
        processRow(col_count, root, row) # for rest of the nodes, keep building the tree

      line_count += 1

    result = json.dumps(root.__dict__,indent=4)
    print(result)


readCsv()
