from functions import find_matching_formulas, formula_to_string
import streamlit as st

#タイトル
st.set_page_config(page_title="分子式計算機", page_icon="🧪", layout="wide")
st.markdown("""
    <style>
        .element-label {
            font-weight: bold;
            font-size: 2.0rem;
            margin-top: 0.3rem;
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #FF0000;'>分子式計算機</h2>", unsafe_allow_html=True)

# ヘッダー：Exact Massと許容誤差を入力
st.markdown("### Exact Massと許容誤差を入力")
exact_mass = st.number_input("Exact Massを入力:", step=0.00001, format="%.5f")
tolerance = st.number_input("許容誤差を入力:", min_value=0.0, step=0.00001, format="%.5f")

# 基本の元素 (C, H, O, N, Na)
st.markdown("### 原子の最小値と最大値を設定:")
min_atoms = {}
max_atoms = {}

basic_elements = ['C', 'H', 'O', 'N', 'S', 'Na']

for element in basic_elements:
    with st.container():
        col1, col2, col3 = st.columns([1, 8, 8])
        col1.markdown(f"<div class='element-label'>{element}</div>", unsafe_allow_html=True)
        min_atoms[element] = col2.number_input(f"{element}の最小値", min_value=0, step=1, value=0, key=f"min_{element}")
        max_atoms[element] = col3.number_input(f"{element}の最大値", min_value=0, step=1, value=0, key=f"max_{element}")


# 追加の元素 (ユーザー選択)
additional_elements = {
    'P': 'P',
    'B': 'B',
    'K': 'K',
    'Si': 'Si',
    'F': 'F',
    'Cl': 'Cl',
    'Br': 'Br',
    'I': 'I',
    'Li': 'Li',
    'Mg': 'Mg',
    'Al': 'Al',
    'Ca': 'Ca',
    'Sc': 'Sc',
    'Ti': 'Ti',
    'V': 'V',
    'Cr': 'Cr',
    'Mn': 'Mn',
    'Fe': 'Fe',
    'Co': 'Co',
    'Ni': 'Ni',
    'Cu': 'Cu',
    'Zn': 'Zn',
    'Se': 'Se',
    'Rb': 'Rb',
    'Sr': 'Sr',
    'Rb': 'Rb',
    'Rh': 'Rh',
    'Pd': 'Pd',
    'Ag': 'Ag',
    'Sn': 'Sn',
    'Cs': 'Cs',
    'Os': 'Os',
    'Ir': 'Ir',
    'Pt': 'Pt',
    'Au': 'Au',
    'Pb': 'Pb'
}

selected_elements = st.sidebar.multiselect("追加する原子を選択:", list(additional_elements.keys()))
for element in selected_elements:
    st.sidebar.write(f"**{element}**")
    min_atoms[element] = st.sidebar.number_input(f"{element}の最小値", min_value=0, step=1, value=0, key=f"min_{element}")
    max_atoms[element] = st.sidebar.number_input(f"{element}の最大値", min_value=0, step=1, value=1, key=f"max_{element}")
    
# 結果の表示
st.markdown("""
    <style>
        .stButton>button {
            padding: 0.3rem 0.8rem;
            font-size: 0.85rem;
            border: 2px solid #4CAF50;  /* 枠線の色 */
            color: #FFFFFF;  /* 文字色 */
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);  /* 影をつける */
        }
    </style>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)    
if st.button("分子式を計算する"):
    with st.spinner("計算中..."):
        matching_formulas = find_matching_formulas(exact_mass, tolerance, min_atoms, max_atoms)
    
    if matching_formulas:
        
        matching_formulas.sort(key=lambda x: abs(x[1] - exact_mass))
        st.write("** 分子式 | Exact Mass | 誤差**")
        
        for i, (formula, mass) in enumerate(matching_formulas):
            formula_str = formula_to_string(formula)
            error = abs(mass - exact_mass)
            if i == 0:
                st.markdown(f"<h4 style='color: red;'>{formula_str} | Mass: {mass:.6f} | 誤差: {error:.6f}</h4>", unsafe_allow_html=True)
            elif i == 1:
                st.markdown(f"<h4 style='color: blue;'>{formula_str} | Mass: {mass:.6f} | 誤差: {error:.6f}</h4>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h4>{formula_str} | Mass: {mass:.6f} | 誤差: {error:.6f}</h4>", unsafe_allow_html=True)

    else:
        st.warning("一致する分子式が見つかりませんでした。")