import csv
import json
import os


# Assumptions
# 1. The csv column format for each level stays same, no matter how many level
# 2. The csv records are ordered like now , for parent-child relationship .
#    That is, all 2 level records  comes before all 3 level  come before 4 level records etc.

# a node in the tree , represent each level
class Level(dict):
    def __init__(self, label, level_id, link, children=None):
        super().__init__()
        self.__dict__ = self
        self.label = label
        self.level_id = level_id
        self.link = link
        self.children = list(children) if children is not None else []


def add_nodes(current_node, nodes, index):
    node = nodes[index]

    if index == len(nodes) - 1:
        current_node.children.append(node)
        return

    if len(current_node.children) < 1:
        current_node.children.append(nodes[index + 1])
    else:
        for child in current_node.children:
            if child.level_id == nodes[index].level_id:
                add_nodes(child, nodes, index + 1)


def process_row(col_count, root, row):
    col = 1
    nodes = []
    while col < col_count:  # fetch all nodes in the row
        if len(row[col]) == 0:
            break
        nodes.append(Level(row[col], row[col + 1], row[col + 2]))
        col += 3

    if len(nodes) > 0:
        add_nodes(root, nodes, 1)  # insert into the tree


# read each line of csv
def read_csv(filepath):

    try:
        open(filepath)
    except OSError:
        print("cannot open")
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        # col_count = 0
        for row in csv_reader:

            col_count = len(row)
            # skip header
            if line_count == 0:
                line_count += 1
                continue

            if line_count == 1:  # create root node in the tree
                root = Level(row[1], row[2], row[3])
                # print(row[1],row[2],row[3])
            else:
                process_row(col_count, root, row)  # for rest of the nodes, keep building the tree
            line_count += 1

        result = json.dumps(dict(root), indent=4)
        print(result)


# read_csv()


def main():
    print(" the process is going to start")
    filepath = input("Please type the entire filepath with the filename : ")

    if filepath is not None and filepath.endswith(".csv"):
        read_csv(filepath)
    else:
        raise FileNotFoundError


if __name__ == "__main__":
    main()
