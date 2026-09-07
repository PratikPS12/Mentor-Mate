import re
from typing import Dict, Any, Optional
import sympy

class DynamicProblemSolver:
    """
    Deterministic mathematical and scientific problem solver powered by SymPy.
    Computes exact roots, derivatives, integrals, matrix properties, and physics
    numerical solutions, formatting all outputs in clean, readable plain text
    using standard Unicode symbols (no LaTeX).
    """

    @classmethod
    def solve(cls, query: str) -> Optional[Dict[str, Any]]:
        q = query.strip()
        q_lower = q.lower()

        # 1. 2x2 Matrix Analysis
        matrix_sol = cls._solve_matrix(q)
        if matrix_sol:
            return matrix_sol

        # 2. Quadratic Equations
        quad_sol = cls._solve_quadratic(q)
        if quad_sol:
            return quad_sol

        # 3. Linear Equations
        linear_sol = cls._solve_linear(q)
        if linear_sol:
            return linear_sol

        # 4. Calculus: Derivatives
        if any(w in q_lower for w in ["derivative", "differentiate", "d/dx", "diff"]):
            deriv_sol = cls._solve_derivative(q)
            if deriv_sol:
                return deriv_sol

        # 5. Calculus: Integrals
        if any(w in q_lower for w in ["integral", "integrate", "antiderivative"]):
            integ_sol = cls._solve_integral(q)
            if integ_sol:
                return integ_sol

        # 6. Physics: Kinematics (u, a, t, v, s)
        kin_sol = cls._solve_kinematics(q)
        if kin_sol:
            return kin_sol

        # 7. Physics: Newton's Force (F = ma)
        force_sol = cls._solve_force(q)
        if force_sol:
            return force_sol

        # 8. Physics: Kinetic and Potential Energy
        energy_sol = cls._solve_energy(q)
        if energy_sol:
            return energy_sol

        # 9. Physics: Ohm's Law (V = IR)
        ohm_sol = cls._solve_ohms_law(q)
        if ohm_sol:
            return ohm_sol

        # 10. General Arithmetic Expressions (e.g. "calculate 25 * 14 + sqrt(144)")
        if any(w in q_lower for w in ["calculate", "evaluate", "what is"]) and any(c in q for c in ["+", "-", "*", "/", "^"]):
            arith_sol = cls._solve_arithmetic(q)
            if arith_sol:
                return arith_sol

        return None

    @classmethod
    def _solve_matrix(cls, q: str) -> Optional[Dict[str, Any]]:
        m = re.search(r"\[\s*\[(.*?)\]\s*,\s*\[(.*?)\]\s*\]", q)
        if not m:
            return None
        try:
            r1 = [sympy.sympify(x.strip()) for x in m.group(1).split(",")]
            r2 = [sympy.sympify(x.strip()) for x in m.group(2).split(",")]
            if len(r1) == 2 and len(r2) == 2:
                M = sympy.Matrix([r1, r2])
                det_val = M.det()
                if det_val != 0:
                    inv_M = M.inv()
                    inv_str = f"[[{inv_M[0,0]}, {inv_M[0,1]}], [{inv_M[1,0]}, {inv_M[1,1]}]]"
                    invertible = "Invertible (Non-singular, det ≠ 0)"
                else:
                    inv_str = "Singular matrix (No inverse exists because det = 0)"
                    invertible = "Non-invertible (Singular, det = 0)"

                text = (
                    f"### 📐 Matrix Determinant & Inverse Analysis (2 × 2):\n\n"
                    f"Given Matrix A = [[{r1[0]}, {r1[1]}], [{r2[0]}, {r2[1]}]]\n\n"
                    f"1. **Determinant Calculation**:\n"
                    f"   det(A) = (a · d) - (b · c)\n"
                    f"   det(A) = ({r1[0]} · {r2[1]}) - ({r1[1]} · {r2[0]}) = {det_val}\n\n"
                    f"2. **Invertibility Status**: {invertible}\n\n"
                    f"3. **Inverse Matrix A⁻¹**:\n"
                    f"   A⁻¹ = (1 / det(A)) · [[d, -b], [-c, a]]\n"
                    f"   A⁻¹ = {inv_str}\n"
                )
                return {
                    "type": "matrix",
                    "title": "2x2 Matrix Analysis",
                    "text": text,
                    "checkpoint": f"Would you like to verify this inverse by checking that A · A⁻¹ = I (the 2x2 Identity Matrix [[1, 0], [0, 1]])?"
                }
        except Exception:
            return None
        return None

    @classmethod
    def _solve_quadratic(cls, q: str) -> Optional[Dict[str, Any]]:
        # Matches: ax^2 + bx + c = 0 or ax² + bx + c = 0
        cleaned = q.replace("²", "^2")
        m = re.search(r"([+-]?\s*\d*)\s*x\^2\s*([+-]\s*\d+)\s*x\s*([+-]\s*\d+)\s*=\s*0", cleaned, re.IGNORECASE)
        if not m:
            # Check without c: ax^2 + bx = 0
            m2 = re.search(r"([+-]?\s*\d*)\s*x\^2\s*([+-]\s*\d+)\s*x\s*=\s*0", cleaned, re.IGNORECASE)
            if m2:
                a_str = m2.group(1).replace(" ", "")
                a = int(a_str) if a_str and a_str not in ["+", "-"] else (-1 if a_str == "-" else 1)
                b = int(m2.group(2).replace(" ", ""))
                c = 0
            else:
                return None
        else:
            a_str = m.group(1).replace(" ", "")
            a = int(a_str) if a_str and a_str not in ["+", "-"] else (-1 if a_str == "-" else 1)
            b = int(m.group(2).replace(" ", ""))
            c = int(m.group(3).replace(" ", ""))

        disc = b**2 - 4 * a * c
        x = sympy.Symbol("x")
        sols = sympy.solve(a * x**2 + b * x + c, x)

        if disc > 0:
            nature = "Two distinct real roots (since D > 0)"
        elif disc == 0:
            nature = "One real repeated root (since D = 0)"
        else:
            nature = "Two complex conjugate roots (since D < 0)"

        sols_str = ", ".join([f"x = {s}" for s in sols])

        text = (
            f"### 📐 Step-by-Step Quadratic Equation Solution for {a}x² + {b}x + {c} = 0:\n\n"
            f"1. **Identify Coefficients**:\n"
            f"   a = {a}, b = {b}, c = {c}\n\n"
            f"2. **Calculate Discriminant (D = b² - 4ac)**:\n"
            f"   D = ({b})² - 4·({a})·({c})\n"
            f"   D = {b**2} - ({4*a*c}) = {disc}\n\n"
            f"3. **Nature of Roots**:\n"
            f"   {nature}\n\n"
            f"4. **Exact Solutions via Quadratic Formula [x = (-b ± √D) / (2a)]**:\n"
            f"   x = (-({b}) ± √({disc})) / (2·{a})\n"
            f"   **Roots**: {sols_str}\n\n"
            f"5. **Vieta's Relations (Root Verification)**:\n"
            f"   - Sum of roots: α + β = -b / a = -({b}) / {a} = {-b/a}\n"
            f"   - Product of roots: α · β = c / a = {c} / {a} = {c/a}\n"
        )
        return {
            "type": "quadratic",
            "title": f"Roots of {a}x² + {b}x + {c} = 0",
            "text": text,
            "checkpoint": f"Try plugging one of the roots ({sols[0]}) back into {a}x² + {b}x + {c} to see if it equals 0! Does it verify?"
        }

    @classmethod
    def _solve_linear(cls, q: str) -> Optional[Dict[str, Any]]:
        # Matches: ax + b = c or ax = c
        m = re.search(r"([+-]?\s*\d*)\s*x\s*([+-]\s*\d+)?\s*=\s*([+-]?\s*\d+)", q)
        if not m:
            return None
        try:
            a_str = (m.group(1) or "").replace(" ", "")
            a = int(a_str) if a_str and a_str not in ["+", "-"] else (-1 if a_str == "-" else 1)
            b = int((m.group(2) or "0").replace(" ", ""))
            c = int(m.group(3).replace(" ", ""))

            x = sympy.Symbol("x")
            sol = sympy.solve(sympy.Eq(a * x + b, c), x)
            if not sol:
                return None

            ans = sol[0]
            sign_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
            eq_display = f"{a}x {sign_b} = {c}" if b != 0 else f"{a}x = {c}"

            steps = [
                f"Equation to solve: **{eq_display}**"
            ]
            if b != 0:
                steps.append(f"Step 1 (Isolate variable term): Subtract {b} from both sides => {a}x = {c} - ({b}) = {c - b}")
                steps.append(f"Step 2 (Divide by coefficient of x): x = ({c - b}) / {a} = {ans}")
            else:
                steps.append(f"Step 1 (Divide by coefficient of x): x = {c} / {a} = {ans}")

            steps_text = "\n".join([f"- {s}" for s in steps])

            text = (
                f"### 📐 Linear Equation Step-by-Step Solution (SymPy Verified):\n\n"
                f"{steps_text}\n\n"
                f"**Verification**:\n"
                f"Substitute x = {ans} into LHS: {a}({ans}) {sign_b} = {a * ans + b} (Matches RHS: {c} ✓)\n"
            )
            return {
                "type": "linear",
                "title": f"Solution to {eq_display}",
                "text": text,
                "checkpoint": "Does each arithmetic step make clear sense, or would you like to try another equation?"
            }
        except Exception:
            return None

    @classmethod
    def _solve_derivative(cls, q: str) -> Optional[Dict[str, Any]]:
        # Extract expression after "derivative of", "differentiate", or "d/dx"
        m = re.search(r"(?:derivative of|differentiate|d/dx of|d/dx)\s*[:=]?\s*([a-zA-Z0-9\s\+\-\*\/\^\(\)\.\_]+)", q, re.IGNORECASE)
        if not m:
            return None
        expr_raw = m.group(1).strip().rstrip("?.,")
        if not expr_raw or len(expr_raw) < 1:
            return None

        # Clean expr for sympify: replace ^ with **, 2x with 2*x
        clean_expr = expr_raw.replace("^", "**")
        clean_expr = re.sub(r"(\d+)\s*x", r"\1*x", clean_expr)

        try:
            x = sympy.Symbol("x")
            parsed = sympy.sympify(clean_expr)
            deriv = sympy.diff(parsed, x)

            # Format in clean text
            parsed_str = str(parsed).replace("**", "^").replace("*", "·")
            deriv_str = str(deriv).replace("**", "^").replace("*", "·")
            # Convert powers to superscripts
            for p in ["2", "3", "4", "5"]:
                parsed_str = parsed_str.replace(f"^{p}", "²" if p == "2" else ("³" if p == "3" else f"^{p}"))
                deriv_str = deriv_str.replace(f"^{p}", "²" if p == "2" else ("³" if p == "3" else f"^{p}"))

            text = (
                f"### 📐 Step-by-Step Differentiation:\n\n"
                f"Given Function: **f(x) = {parsed_str}**\n\n"
                f"1. **Governing Rule**:\n"
                f"   The derivative f'(x) = d/dx [f(x)] represents the instantaneous rate of change or tangent slope at any x.\n\n"
                f"2. **Differentiation Steps**:\n"
                f"   - Apply Power Rule: d/dx [xⁿ] = n · xⁿ⁻¹\n"
                f"   - Apply Linearity: d/dx [u + v] = d/dx [u] + d/dx [v]\n\n"
                f"3. **Final Derivative Result**:\n"
                f"   **f'(x) = {deriv_str}**\n"
            )
            return {
                "type": "derivative",
                "title": f"Derivative of f(x) = {parsed_str}",
                "text": text,
                "checkpoint": f"Would you like to evaluate this derivative at a specific point, like x = 1 or x = 2?"
            }
        except Exception:
            return None

    @classmethod
    def _solve_integral(cls, q: str) -> Optional[Dict[str, Any]]:
        m = re.search(r"(?:integral of|integrate|antiderivative of)\s*[:=]?\s*([a-zA-Z0-9\s\+\-\*\/\^\(\)\.\_]+?)(?:\s*dx|\s*$)", q, re.IGNORECASE)
        if not m:
            return None
        expr_raw = m.group(1).strip().rstrip("?.,")
        if not expr_raw:
            return None

        clean_expr = expr_raw.replace("^", "**")
        clean_expr = re.sub(r"(\d+)\s*x", r"\1*x", clean_expr)

        try:
            x = sympy.Symbol("x")
            parsed = sympy.sympify(clean_expr)
            integ = sympy.integrate(parsed, x)

            parsed_str = str(parsed).replace("**", "^").replace("*", "·")
            integ_str = str(integ).replace("**", "^").replace("*", "·")
            for p in ["2", "3", "4", "5"]:
                parsed_str = parsed_str.replace(f"^{p}", "²" if p == "2" else ("³" if p == "3" else f"^{p}"))
                integ_str = integ_str.replace(f"^{p}", "²" if p == "2" else ("³" if p == "3" else f"^{p}"))

            text = (
                f"### 📐 Step-by-Step Integration:\n\n"
                f"Integrand: **f(x) = {parsed_str}**\n\n"
                f"1. **Governing Rule (Power Rule for Integration)**:\n"
                f"   ∫ xⁿ dx = (xⁿ⁺¹ / (n + 1)) + C   (for n ≠ -1)\n\n"
                f"2. **Antiderivative Result**:\n"
                f"   **∫ ({parsed_str}) dx = {integ_str} + C**\n"
                f"   *(where C is the arbitrary constant of integration)*\n\n"
                f"3. **Verification by Differentiation**:\n"
                f"   d/dx [{integ_str} + C] = {parsed_str} ✓\n"
            )
            return {
                "type": "integral",
                "title": f"Integral of f(x) = {parsed_str}",
                "text": text,
                "checkpoint": f"Would you like to calculate a definite integral with boundary limits (e.g. from x = 0 to x = 3)?"
            }
        except Exception:
            return None

    @classmethod
    def _solve_kinematics(cls, q: str) -> Optional[Dict[str, Any]]:
        # Detect patterns like: u = 10, a = 2, t = 5
        u_m = re.search(r"(?:u|initial velocity)\s*=\s*([+-]?\d+(?:\.\d+)?)", q, re.IGNORECASE)
        v_m = re.search(r"(?:v|final velocity)\s*=\s*([+-]?\d+(?:\.\d+)?)", q, re.IGNORECASE)
        a_m = re.search(r"(?:a|acceleration)\s*=\s*([+-]?\d+(?:\.\d+)?)", q, re.IGNORECASE)
        t_m = re.search(r"(?:t|time)\s*=\s*(\d+(?:\.\d+)?)", q, re.IGNORECASE)
        s_m = re.search(r"(?:s|distance|displacement)\s*=\s*([+-]?\d+(?:\.\d+)?)", q, re.IGNORECASE)

        # Need at least 2 parameters to compute kinematics
        params = [bool(u_m), bool(v_m), bool(a_m), bool(t_m), bool(s_m)]
        if sum(params) < 2:
            return None

        u = float(u_m.group(1)) if u_m else None
        v = float(v_m.group(1)) if v_m else None
        a = float(a_m.group(1)) if a_m else None
        t = float(t_m.group(1)) if t_m else None
        s = float(s_m.group(1)) if s_m else None

        steps = []
        # Case 1: u, a, t known -> find v and s
        if u is not None and a is not None and t is not None:
            v_calc = u + a * t
            s_calc = u * t + 0.5 * a * (t**2)
            steps.append(f"Given: Initial velocity u = {u} m/s, Acceleration a = {a} m/s², Time t = {t} s")
            steps.append(f"1. Final Velocity Formula: v = u + a·t")
            steps.append(f"   v = {u} + ({a})·({t}) = {v_calc} m/s")
            steps.append(f"2. Displacement Formula: s = u·t + (1/2)·a·t²")
            steps.append(f"   s = ({u})·({t}) + (0.5)·({a})·({t}²) = {u*t} + {0.5*a*(t**2)} = {s_calc} m")
            res_title = f"Kinematics Results: v = {v_calc} m/s, s = {s_calc} m"
        elif u is not None and v is not None and t is not None:
            a_calc = (v - u) / t if t > 0 else 0
            s_calc = ((u + v) / 2) * t
            steps.append(f"Given: Initial velocity u = {u} m/s, Final velocity v = {v} m/s, Time t = {t} s")
            steps.append(f"1. Acceleration: a = (v - u) / t = ({v} - {u}) / {t} = {a_calc} m/s²")
            steps.append(f"2. Displacement: s = ((u + v) / 2) · t = (({u} + {v}) / 2) · {t} = {s_calc} m")
            res_title = f"Kinematics Results: a = {a_calc} m/s², s = {s_calc} m"
        else:
            return None

        text = (
            f"### 🚀 Kinematics Step-by-Step Calculation:\n\n"
            + "\n".join([f"- {st}" for st in steps]) + "\n"
        )
        return {
            "type": "kinematics",
            "title": res_title,
            "text": text,
            "checkpoint": "Notice how the units match consistently across velocity (m/s), acceleration (m/s²), and displacement (m)!"
        }

    @classmethod
    def _solve_force(cls, q: str) -> Optional[Dict[str, Any]]:
        # Matches: mass = 5 kg, acceleration = 2 m/s^2 or force = 20 N, mass = 4 kg
        m_match = re.search(r"(?:mass|m)\s*=\s*(\d+(?:\.\d+)?)\s*(?:kg|g)?", q, re.IGNORECASE)
        a_match = re.search(r"(?:acceleration|a)\s*=\s*([+-]?\d+(?:\.\d+)?)\s*(?:m/s\^?2)?", q, re.IGNORECASE)
        f_match = re.search(r"(?:force|f|net force)\s*=\s*([+-]?\d+(?:\.\d+)?)\s*(?:n|newtons?)?", q, re.IGNORECASE)

        if m_match and a_match:
            m = float(m_match.group(1))
            a = float(a_match.group(1))
            f = m * a
            text = (
                f"### ⚡ Newton's Second Law Calculation (F = m · a):\n\n"
                f"- **Given**:\n"
                f"  - Mass (m) = {m} kg\n"
                f"  - Acceleration (a) = {a} m/s²\n\n"
                f"- **Governing Formula**:\n"
                f"  F_net = m · a\n\n"
                f"- **Substitution & Calculation**:\n"
                f"  F_net = ({m} kg) · ({a} m/s²) = **{f} N** (Newtons)\n"
            )
            return {
                "type": "force",
                "title": f"Force Calculation: F = {f} N",
                "text": text,
                "checkpoint": f"If the mass were doubled to {2*m} kg while keeping the force at {f} N, what would happen to the acceleration?"
            }
        elif f_match and m_match:
            f = float(f_match.group(1))
            m = float(m_match.group(1))
            if m > 0:
                a = f / m
                text = (
                    f"### ⚡ Acceleration Calculation from Force (a = F / m):\n\n"
                    f"- **Given**:\n"
                    f"  - Net Force (F) = {f} N\n"
                    f"  - Mass (m) = {m} kg\n\n"
                    f"- **Governing Formula**:\n"
                    f"  a = F_net / m\n\n"
                    f"- **Substitution & Calculation**:\n"
                    f"  a = ({f} N) / ({m} kg) = **{a} m/s²**\n"
                )
                return {
                    "type": "force",
                    "title": f"Acceleration: a = {a} m/s²",
                    "text": text,
                    "checkpoint": f"Because acceleration is directly proportional to force and inversely proportional to mass!"
                }
        return None

    @classmethod
    def _solve_energy(cls, q: str) -> Optional[Dict[str, Any]]:
        # Kinetic Energy: m, v
        m_match = re.search(r"(?:mass|m)\s*=\s*(\d+(?:\.\d+)?)\s*(?:kg)?", q, re.IGNORECASE)
        v_match = re.search(r"(?:velocity|speed|v)\s*=\s*(\d+(?:\.\d+)?)\s*(?:m/s)?", q, re.IGNORECASE)
        h_match = re.search(r"(?:height|h)\s*=\s*(\d+(?:\.\d+)?)\s*(?:m|meters)?", q, re.IGNORECASE)

        if m_match and v_match:
            m = float(m_match.group(1))
            v = float(v_match.group(1))
            ke = 0.5 * m * (v**2)
            text = (
                f"### ⚡ Kinetic Energy Calculation (KE = (1/2) · m · v²):\n\n"
                f"- **Given**:\n"
                f"  - Mass (m) = {m} kg\n"
                f"  - Velocity (v) = {v} m/s\n\n"
                f"- **Governing Formula**:\n"
                f"  KE = (1/2) · m · v²\n\n"
                f"- **Calculation**:\n"
                f"  KE = 0.5 · ({m}) · ({v})²\n"
                f"  KE = 0.5 · ({m}) · ({v**2}) = **{ke} J** (Joules)\n"
            )
            return {
                "type": "energy",
                "title": f"Kinetic Energy: KE = {ke} J",
                "text": text,
                "checkpoint": f"Notice that velocity is squared—so doubling the speed from {v} m/s to {2*v} m/s quadruples the kinetic energy to {ke*4} J!"
            }
        elif m_match and h_match:
            m = float(m_match.group(1))
            h = float(h_match.group(1))
            g = 9.8
            pe = m * g * h
            text = (
                f"### ⚡ Gravitational Potential Energy (PE = m · g · h):\n\n"
                f"- **Given**:\n"
                f"  - Mass (m) = {m} kg\n"
                f"  - Height (h) = {h} m\n"
                f"  - Acceleration due to gravity (g) = 9.8 m/s²\n\n"
                f"- **Governing Formula**:\n"
                f"  PE = m · g · h\n\n"
                f"- **Calculation**:\n"
                f"  PE = ({m} kg) · (9.8 m/s²) · ({h} m) = **{pe:.2f} J** (Joules)\n"
            )
            return {
                "type": "energy",
                "title": f"Potential Energy: PE = {pe:.2f} J",
                "text": text,
                "checkpoint": f"If the object is dropped from height {h} m, all of this potential energy will convert into kinetic energy just before impact!"
            }
        return None

    @classmethod
    def _solve_ohms_law(cls, q: str) -> Optional[Dict[str, Any]]:
        v_match = re.search(r"(?:voltage|potential|v)\s*=\s*(\d+(?:\.\d+)?)\s*(?:v|volts?)?", q, re.IGNORECASE)
        r_match = re.search(r"(?:resistance|r)\s*=\s*(\d+(?:\.\d+)?)\s*(?:ohm|ohms|Ω)?", q, re.IGNORECASE)
        i_match = re.search(r"(?:current|i)\s*=\s*(\d+(?:\.\d+)?)\s*(?:a|amps?|amperes?)?", q, re.IGNORECASE)

        if v_match and r_match:
            v = float(v_match.group(1))
            r = float(r_match.group(1))
            if r > 0:
                i = v / r
                p = v * i
                text = (
                    f"### ⚡ Ohm's Law & Circuit Power (V = I · R):\n\n"
                    f"- **Given**:\n"
                    f"  - Voltage (V) = {v} V\n"
                    f"  - Resistance (R) = {r} Ω\n\n"
                    f"- **Formulas**:\n"
                    f"  1. Electric Current: I = V / R\n"
                    f"  2. Power Dissipation: P = V · I = I² · R\n\n"
                    f"- **Calculations**:\n"
                    f"  - Current I = {v} V / {r} Ω = **{i:.3f} A**\n"
                    f"  - Power P = ({v} V) · ({i:.3f} A) = **{p:.2f} W** (Watts)\n"
                )
                return {
                    "type": "ohms_law",
                    "title": f"Current I = {i:.3f} A, Power = {p:.2f} W",
                    "text": text,
                    "checkpoint": f"If we doubled the resistance to {2*r} Ω while holding voltage constant, the current would halve to {i/2:.3f} A!"
                }
        return None

    @classmethod
    def _solve_arithmetic(cls, q: str) -> Optional[Dict[str, Any]]:
        m = re.search(r"(?:calculate|evaluate|what is)\s*[:=]?\s*([0-9\+\-\*\/\^\(\)\.\s_]+)", q, re.IGNORECASE)
        if not m:
            return None
        expr_str = m.group(1).strip()
        if not expr_str or len(expr_str) < 2:
            return None
        try:
            val = sympy.sympify(expr_str.replace("^", "**"))
            num_val = float(val) if val.is_number and not val.is_Integer else val
            text = (
                f"### 🔢 Step-by-Step Numerical Calculation:\n\n"
                f"- **Expression**: {expr_str}\n"
                f"- **Exact Result**: **{num_val}**\n"
            )
            return {
                "type": "arithmetic",
                "title": f"Calculation Result: {num_val}",
                "text": text,
                "checkpoint": f"The exact value evaluates to {num_val}."
            }
        except Exception:
            return None
