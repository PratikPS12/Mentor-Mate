import re
from typing import Optional, Tuple

def extract_balanced_braces(s: str, start_idx: int) -> Tuple[Optional[str], int]:
    """
    Extracts content within balanced curly braces starting at start_idx.
    Returns (content, end_index) or (None, start_idx) if not found.
    """
    if start_idx >= len(s) or s[start_idx] != "{":
        return None, start_idx
    depth = 0
    content = []
    for i in range(start_idx, len(s)):
        if s[i] == "{":
            depth += 1
            if depth > 1:
                content.append("{")
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return "".join(content), i + 1
            else:
                content.append("}")
        else:
            content.append(s[i])
    return None, start_idx

def clean_latex_to_plain_text(text: str) -> str:
    """
    Transforms LaTeX math markup, symbols, and formatting into clean,
    human-readable plain text with proper Unicode mathematical symbols,
    superscripts, subscripts, and formulas. No LaTeX tags or backslashes remain.
    """
    if not text:
        return ""

    s = text

    # 1. Convert \frac{numerator}{denominator} with balanced braces
    while r"\frac" in s:
        idx = s.find(r"\frac")
        after_frac = idx + len(r"\frac")
        while after_frac < len(s) and s[after_frac].isspace():
            after_frac += 1
        num, next_idx = extract_balanced_braces(s, after_frac)
        if num is None:
            # Check for simple \frac 1 2 pattern
            m = re.match(r"\\frac\s*([a-zA-Z0-9])\s*([a-zA-Z0-9])", s[idx:])
            if m:
                s = s[:idx] + f"({m.group(1)} / {m.group(2)})" + s[idx + m.end():]
                continue
            break
        while next_idx < len(s) and s[next_idx].isspace():
            next_idx += 1
        den, end_idx = extract_balanced_braces(s, next_idx)
        if den is None:
            break

        cleaned_num = clean_latex_to_plain_text(num).strip()
        cleaned_den = clean_latex_to_plain_text(den).strip()
        # If num has spaces or operators (+, -, ±), wrap in parentheses
        if any(op in cleaned_num for op in ["+", "-", "±", "·", "*", " "]):
            num_str = f"({cleaned_num})"
        else:
            num_str = cleaned_num
        if any(op in cleaned_den for op in ["+", "-", "±", "·", "*", " "]):
            den_str = f"({cleaned_den})"
        else:
            den_str = cleaned_den
        s = s[:idx] + f"({num_str} / {den_str})" + s[end_idx:]


    # 2. Square roots and cube roots with balanced braces
    while r"\sqrt[3]" in s:
        idx = s.find(r"\sqrt[3]")
        after = idx + len(r"\sqrt[3]")
        while after < len(s) and s[after].isspace():
            after += 1
        rad, end_idx = extract_balanced_braces(s, after)
        if rad is not None:
            s = s[:idx] + f"∛({clean_latex_to_plain_text(rad).strip()})" + s[end_idx:]
        else:
            break

    while r"\sqrt" in s:
        idx = s.find(r"\sqrt")
        after = idx + len(r"\sqrt")
        while after < len(s) and s[after].isspace():
            after += 1
        rad, end_idx = extract_balanced_braces(s, after)
        if rad is not None:
            s = s[:idx] + f"√({clean_latex_to_plain_text(rad).strip()})" + s[end_idx:]
        else:
            # Check simple \sqrt x
            m = re.match(r"\\sqrt\s*([a-zA-Z0-9])", s[idx:])
            if m:
                s = s[:idx] + f"√({m.group(1)})" + s[idx + m.end():]
                continue
            break

    # 3. Vector formatting: \vec{F} -> F
    while r"\vec" in s:
        idx = s.find(r"\vec")
        after = idx + len(r"\vec")
        while after < len(s) and s[after].isspace():
            after += 1
        vec_content, end_idx = extract_balanced_braces(s, after)
        if vec_content is not None:
            s = s[:idx] + clean_latex_to_plain_text(vec_content).strip() + s[end_idx:]
        else:
            m = re.match(r"\\vec\s*([a-zA-Z])", s[idx:])
            if m:
                s = s[:idx] + m.group(1) + s[idx + m.end():]
                continue
            break

    # 4. Strip \text{...}, \mathrm{...}, \mathbf{...}, \mathit{...}, \operatorname{...}
    for cmd in [r"\text", r"\mathrm", r"\mathbf", r"\mathit", r"\textbf", r"\textit", r"\operatorname"]:
        while cmd in s:
            idx = s.find(cmd)
            after = idx + len(cmd)
            while after < len(s) and s[after].isspace():
                after += 1
            content, end_idx = extract_balanced_braces(s, after)
            if content is not None:
                s = s[:idx] + content + s[end_idx:]
            else:
                break

    # 5. Greek and mathematical symbols & operators
    symbol_replacements = [
        (r"\\alpha", "α"), (r"\\beta", "β"), (r"\\gamma", "γ"), (r"\\theta", "θ"),
        (r"\\lambda", "λ"), (r"\\mu", "μ"), (r"\\pi", "π"), (r"\\sigma", "σ"),
        (r"\\omega", "ω"), (r"\\rho", "ρ"), (r"\\eta", "η"), (r"\\phi", "φ"),
        (r"\\psi", "ψ"), (r"\\delta", "δ"), (r"\\epsilon", "ε"), (r"\\tau", "τ"),
        (r"\\Delta", "Δ"), (r"\\Omega", "Ω"), (r"\\Theta", "Θ"), (r"\\Lambda", "Λ"),
        (r"\\Sigma", "Σ"), (r"\\Phi", "Φ"), (r"\\Psi", "Ψ"),
        (r"\\sum", "∑"), (r"\\prod", "∏"), (r"\\int", "∫"), (r"\\oint", "∮"),
        (r"\\infty", "∞"), (r"\\approx", "≈"), (r"\\sim", "~"), (r"\\neq", "≠"),
        (r"\\ne\b", "≠"), (r"\\leq", "≤"), (r"\\le\b", "≤"), (r"\\geq", "≥"),
        (r"\\ge\b", "≥"), (r"\\pm", "±"), (r"\\mp", "∓"), (r"\\cdot", " · "),
        (r"\\times", " × "), (r"\\div", " ÷ "), (r"\\circ", "°"),
        (r"\\implies", " => "), (r"\\iff", " <=> "),
        (r"\\xrightarrow\{([^{}]+)\}", r" --(\1)--> "),
        (r"\\longrightarrow", " --> "), (r"\\to", " → "), (r"\\rightarrow", " → "),
        (r"\\leftarrow", " ← "), (r"\\leftrightarrow", " ↔ "), (r"\\propto", " ∝ "),
        (r"\\partial", "∂"), (r"\\nabla", "∇"),
        (r"\\equiv", " ≡ "), (r"\\ll\b", " << "), (r"\\gg\b", " >> "),
        (r"\\in\b", " ∈ "), (r"\\notin\b", " ∉ "), (r"\\subset\b", " ⊂ "),
        (r"\\cup\b", " ∪ "), (r"\\cap\b", " ∩ "),
        (r"\\sin", "sin"), (r"\\cos", "cos"), (r"\\tan", "tan"),
        (r"\\sec", "sec"), (r"\\csc", "csc"), (r"\\cot", "cot"),
        (r"\\arcsin", "arcsin"), (r"\\arccos", "arccos"), (r"\\arctan", "arctan"),
        (r"\\ln", "ln"), (r"\\log", "log"), (r"\\exp", "exp"),
        (r"\\lim_\{([^}]+)\}", r"lim(\1)"), (r"\\lim", "lim"),
        (r"\\quad", " "), (r"\\qquad", "  "),
        (r"\\left\(", "("), (r"\\right\)", ")"),
        (r"\\left\[", "["), (r"\\right\]", "]"),
        (r"\\left\\{", "{"), (r"\\right\\}", "}"),
        (r"\\left\|", "|"), (r"\\right\|", "|"),
        (r"\\left", ""), (r"\\right", ""),
        (r"\\,", " "), (r"\\;", " "), (r"\\!", ""), (r"\\:", " "),
    ]

    for pattern, rep in symbol_replacements:
        s = re.sub(pattern, rep, s)

    # 6. Superscripts
    sup_map = {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴",
        "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹",
        "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾",
        "n": "ⁿ", "i": "ⁱ"
    }
    def replace_sup(match):
        inner = match.group(1) or match.group(2)
        return "".join(sup_map.get(c, "^" + c) for c in inner)

    s = re.sub(r"\^\{([0-9\+\-ni]+)\}|\^([0-9\+\-ni])\b", replace_sup, s)
    s = re.sub(r"\^\\circ|\^\{°\}", "°", s)

    # 7. Subscripts for chemical formulas and variables
    sub_map = {
        "0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄",
        "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉",
        "+": "₊", "-": "₋", "a": "ₐ", "e": "ₑ", "o": "ₒ",
        "x": "ₓ", "i": "ᵢ", "j": "ⱼ"
    }
    def replace_sub(match):
        inner = match.group(1) or match.group(2)
        return "".join(sub_map.get(c, "_" + c) for c in inner)

    # Subscripts with braces _{...} or _digit
    s = re.sub(r"_\{([0-9\+\-aeoxij]+)\}|_([0-9\+\-aeoxij])", replace_sub, s)
    # Generic word subscript _{net} -> _net
    s = re.sub(r"_\{([^{}]+)\}", r"_\1", s)


    # 8. Strip $$ ... $$ and $ ... $
    s = re.sub(r"\$\$([^\$]+)\$\$", r"\1", s)
    s = re.sub(r"\$([^\$]+)\$", r"\1", s)

    # 9. Clean up any remaining backslashes before words and braces
    s = re.sub(r"\\([a-zA-Z]+)", r"\1", s)
    s = s.replace(r"\{", "{").replace(r"\}", "}")

    # 10. Clean up extra spaces
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r" \n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)

    return s.strip()
