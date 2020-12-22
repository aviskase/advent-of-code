from .puzzle import parse, find_potentially_safe, count_potentially_safe, canonical_dangerous_list

data = '''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''.strip()


def test_potentially_safe():
    foods = parse(data)
    safe, _ = find_potentially_safe(foods)
    assert safe == {'kfcds', 'nhms', 'sbzzf', 'trh'}
    assert count_potentially_safe(foods, safe) == 5


def test_canonical():
    foods = parse(data)
    _, not_safe = find_potentially_safe(foods)
    assert canonical_dangerous_list(not_safe) == 'mxmxvkd,sqjhc,fvjkl'
