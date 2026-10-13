
import ast
import operator
import streamlit as st

st.set_page_config(
    page_title="My Calculator",
    page_icon="＋",
    layout="centered",
)

# ---------- Calculator logic ----------

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_calculate(expression):
    """Calculate arithmetic expressions without using eval()."""
    tree = ast.parse(expression, mode="eval")

    def calculate(node):
        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator")

            left = calculate(node.left)
            right = calculate(node.right)
            return op(left, right)

        if isinstance(node, ast.UnaryOp):
            op = OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError("Unsupported operator")
            return op(calculate(node.operand))

        raise ValueError("Invalid expression")

    result = calculate(tree)

    if isinstance(result, float):
        if not (-float("inf") < result < float("inf")):
            raise ValueError("Result is too large")
        if result.is_integer():
            return str(int(result))

    return str(result)

# ---------- App state ----------

if "expression" not in st.session_state:
    st.session_state.expression = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "just_calculated" not in st.session_state:
    st.session_state.just_calculated = False

if "error" not in st.session_state:
    st.session_state.error = ""

def press(key):
    current = st.session_state.expression

    if key == "C":
        st.session_state.expression = ""
        st.session_state.error = ""
        st.session_state.just_calculated = False
        return

    if key == "DEL":
        st.session_state.expression = current[:-1]
        st.session_state.error = ""
        st.session_state.just_calculated = False
        return

    if key == "=":
        if not current:
            return
        try:
            result = safe_calculate(current)
            st.session_state.history.insert(
                0, f"{current} = {result}"
            )
            st.session_state.history = st.session_state.history[:5]
            st.session_state.expression = result
            st.session_state.error = ""
            st.session_state.just_calculated = True
        except (ValueError, SyntaxError, ZeroDivisionError,
                OverflowError):
            st.session_state.error = "Invalid calculation"
        return

    if key == "%":
        # Convert the last entered number to a percentage.
        import re
        match = re.search(r"(\d+\.?\d*|\.\d+)$", current)
        if match:
            number = match.group(0)
            st.session_state.expression = (
                current[:match.start()] + f"({number}*0.01)"
            )
        st.session_state.just_calculated = False
        return

    if key in ("+", "-", "*", "/"):
        if st.session_state.just_calculated:
            st.session_state.just_calculated = False
        st.session_state.expression = current + key
        st.session_state.error = ""
        return

    if st.session_state.just_calculated:
        current = ""
        st.session_state.just_calculated = False

    st.session_state.expression = current + key
    st.session_state.error = ""

# ---------- Minimal light UI ----------

st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
        color: #202635;
    }
    .block-container {
        max-width: 430px;
        padding-top: 2rem;
    }
    h1 {
        text-align: center;
        font-size: 2rem !important;
        color: #202635;
    }
    .subtitle {
        text-align: center;
        color: #7b8496;
        margin-bottom: 1.5rem;
    }
    .display {
        background: #ffffff;
        border: 1px solid #e7eaf1;
        border-radius: 18px;
        padding: 24px 18px;
        margin: 12px 0 20px;
        min-height: 90px;
        text-align: right;
        font-size: 2.1rem;
        font-weight: 600;
        overflow-wrap: anywhere;
        color: #202635;
        box-shadow: 0 4px 18px rgba(30, 45, 80, 0.04);
    }
    div.stButton > button {
        width: 100%;
        height: 56px;
        border: 1px solid #e5e9f2;
        border-radius: 14px;
        background: #ffffff;
        color: #202635;
        font-size: 1.15rem;
        font-weight: 500;
        transition: all 0.15s ease;
    }
    div.stButton > button:hover {
        border-color: #8da8f5;
        background: #edf2ff;
        color: #355bd6;
    }
    [data-testid="stBaseButton-primary"] {
        background: #4569e8 !important;
        color: white !important;
        border: none !important;
    }
    [data-testid="stBaseButton-primary"]:hover {
        background: #3455ce !important;
    }
    section[data-testid="stSidebar"] {
        background: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

st.title("Calculator")
st.markdown(
    '<p class="subtitle">Simple calculations, beautifully done.</p>',
    unsafe_allow_html=True,
)

display = st.session_state.expression or "0"
st.markdown(
    f'<div class="display">{display}</div>',
    unsafe_allow_html=True,
)

if st.session_state.error:
    st.error(st.session_state.error)

# Each row contains four calculator buttons.
rows = [
    [("C", "secondary"), ("DEL", "secondary"),
     ("%", "secondary"), ("/", "secondary")],
    [("7", "secondary"), ("8", "secondary"),
     ("9", "secondary"), ("*", "secondary")],
    [("4", "secondary"), ("5", "secondary"),
     ("6", "secondary"), ("-", "secondary")],
    [("1", "secondary"), ("2", "secondary"),
     ("3", "secondary"), ("+", "secondary")],
    [("00", "secondary"), ("0", "secondary"),
     (".", "secondary"), ("=", "primary")],
]

labels = {
    "*": "×",
    "/": "÷",
    "-": "−",
    "DEL": "⌫",
}

for row in rows:
    columns = st.columns(4, gap="small")
    for column, (key, style) in zip(columns, row):
        with column:
            st.button(
                labels.get(key, key),
                key=f"button_{key}_{rows.index(row)}",
                type=style,
                on_click=press,
                args=(key,),
            )

with st.expander("Recent calculations"):
    if st.session_state.history:
        for item in st.session_state.history:
            st.write(item)
    else:
        st.caption("Your calculations will appear here.")