def get_indirects(node, direct_orbits):
    next_node = direct_orbits[node]
    if next_node == 'COM':
        return []
    return [[next_node, direct_orbits[next_node]]] + get_indirects(next_node, direct_orbits)


def find_orbits(direct_orbits):
    orbits = []
    for node1, node2 in direct_orbits.items():
        orbits.append([node1, node2])
        orbits.extend(get_indirects(node1, direct_orbits))
    return orbits


def total_nodes(orbits):
    return [node for node, _ in orbits] + ['COM']


def total_transfers_to_node(nodes, node):
    return nodes.index(node)


def find_common_node(a, b):
    for node in a:
        if node in b:
            return node
    return None


def solver():
    with open('input.txt', 'r') as f:
        orbits = {
            line.strip().split(')')[1]: line.strip().split(')')[0]
            for line in f.readlines()
        }
        all_orbits = find_orbits(orbits)
        print('Number of orbits: ', len(all_orbits))  # 245089
        my_orbits = total_nodes(get_indirects('YOU', orbits))
        santa_orbits = total_nodes(get_indirects('SAN', orbits))
        common_node = find_common_node(my_orbits, santa_orbits)
        total = total_transfers_to_node(my_orbits, common_node) + total_transfers_to_node(santa_orbits, common_node)
        print('Total transfers:', total)


if __name__ == '__main__':
    solver()
