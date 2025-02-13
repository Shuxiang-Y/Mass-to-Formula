from itertools import product

#基本的に最も同位体比が多いものを採用、同じぐらいの同位体比のものが2つある場合、小さいほうを採用
ELEMENT_MASSES = {
    'C': 12.000000,
    'H': 1.007825,
    'Li': 7.016003,
    'B': 11.009305,
    'O': 15.994915,
    'N': 14.003074,
    'F': 18.998403,
    'Na': 22.989769,
    'Mg': 23.985041,
    'Al': 26.981538,
    'S': 31.972071,
    'P': 30.973762,
    'Si': 27.976926,
    'Cl': 34.968852,
    'K': 38.963706,
    'Ca': 39.962590,
    'Sc': 44.955908,
    'Ti': 47.947942,
    'V': 50.943957,
    'Cr': 51.940506,
    'Mn': 54.938043,
    'Fe': 55.934936,
    'Co': 58.933194,
    'Ni': 57.935342,
    'Cu': 62.929597,
    'Zn': 63.929142,
    'Se': 79.916521,
    'Br': 78.918337,
    'Rb': 84.911789,
    'Sr': 87.905612,
    'Rb': 101.904344,
    'Rh': 102.905498,
    'Pd': 105.903480,
    'Ag': 106.905091,
    'Sn': 119.902201,
    'I': 126.904471,
    'Cs': 132.905451,
    'Os': 191.961477,
    'Ir': 192.962921,
    'Pt': 193.962680,
    'Au': 196.966568,
    'Pb': 207.976652
}

def generate_formulas(max_atoms):
    """
    個別に最大原子数を設定して、可能な分子式を生成する。
    max_atoms: 各元素の最大原子数を持つ辞書 (例: {'C': 10, 'H': 20, 'O': 5, 'N': 5})
    """
    elements = list(max_atoms.keys())
    ranges = [range(max_atoms[element] + 1) for element in elements]
    for combo in product(*ranges):
        if sum(combo) == 0:  # 全ての原子数が0の場合を除外
            continue
        yield {elements[i]: combo[i] for i in range(len(elements))}

def calculate_exact_mass(formula):
    """
    分子式から正確質量を計算する。
    formula: 分子式を表す辞書 (例: {'C': 6, 'H': 12, 'O': 6})
    """
    return sum(ELEMENT_MASSES[element] * count for element, count in formula.items())

def find_matching_formulas(exact_mass, tolerance, max_atoms):
    """
    与えられた正確質量に一致する分子式の候補を探す。
    exact_mass: 測定された正確質量
    tolerance: 許容誤差 (例: 0.01)
    max_atoms: 各元素の最大原子数を持つ辞書 (例: {'C': 10, 'H': 20, 'O': 5, 'N': 5})
    """
    matching_formulas = []
    for formula in generate_formulas(max_atoms):
        mass = calculate_exact_mass(formula)
        if abs(mass - exact_mass) <= tolerance:
            matching_formulas.append((formula, mass))
    return matching_formulas

def formula_to_string(formula):
    """
    辞書形式の分子式を通常の化学式文字列に変換する。
    例: {'C': 5, 'H': 10, 'O': 1} -> 'C5H10O'
    """
    return ''.join(f"{element}{count if count > 1 else ''}" for element, count in formula.items() if count > 0)

max_atoms = {'C': 30, 'H': 40, 'O': 5, 'Si': 1, 'Na' : 1}  # 各元素の最大原子数
exact_mass = 471.1962  # 測定された正確質量
tolerance = 0.001    # 許容誤差

matching_formulas = find_matching_formulas(exact_mass, tolerance, max_atoms)

for formula, mass in matching_formulas:
    formula_str = formula_to_string(formula)
    print(f"Formula: {formula_str}, Mass: {mass:.6f}")