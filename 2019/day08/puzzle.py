from pprint import pprint
def flatten(a):
    return [item for sublist in a for item in sublist]


def num_of_x(layer, x=0):
    flat_layer = flatten(layer)
    return flat_layer.count(x)


def find_with_smallest_zeros(layers):
    return min(layers, key=num_of_x)


def combine_layers(layers, width, height):
    image = []
    pixel = -1
    for h in range(height):
        image.append([])
        for w in range(width):
            for l in layers:
                pixel = l[h][w]
                if pixel == 1 or pixel == 0:
                    break
            image[h].append(pixel)
    return image


def convert_to_layers(raw_data, width, height):
    layer_size = width * height
    num_of_layers = len(raw_data) // layer_size
    raw_data = iter(raw_data)
    layers = []
    for l in range(num_of_layers):
        layers.append([])
        for h in range(height):
            layers[l].append([])
            for w in range(width):
                layers[l][h].append(int(next(raw_data)))
    return layers


def solver():
    with open('input.txt', 'r') as f:
        raw_data = f.readline()
        layers = convert_to_layers(raw_data, 25, 6)
        layer = find_with_smallest_zeros(layers)
        print('Result: ', num_of_x(layer, 1) * num_of_x(layer, 2))
        image = combine_layers(layers, 25, 6)
        pprint(image)


if __name__ == '__main__':
    solver()
