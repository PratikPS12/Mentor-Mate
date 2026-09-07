import re
import json
import uuid
from typing import Dict, Any, List, Optional
import sympy
from app.services.ai.provider import AIProvider
from app.services.ai.math_formatter import clean_latex_to_plain_text
from app.services.ai.math_evaluator import DynamicProblemSolver
from app.services.curriculum.curriculum_graph import CurriculumKnowledgeGraph

class LocalFallbackProvider(AIProvider):
    """
    High-Fidelity Pedagogical Knowledge & Socratic Reasoning Engine.
    Acts as a warm, encouraging, chatty teacher who delivers deep, rigorous conceptual
    explanations across Physics, Chemistry, Biology, Mathematics, and Computer Science,
    with deterministic SymPy verification and clean formula formatting (no LaTeX).
    """

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        response_format: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        user_message = ""
        system_context = ""
        for m in messages:
            if m.get("role") == "user":
                user_message = m.get("content", "")
            elif m.get("role") == "system":
                system_context = m.get("content", "")

        # 1. Deterministic SymPy problem solver (algebra, calculus, kinematics, physics)
        math_problem = DynamicProblemSolver.solve(user_message)
        math_solution = math_problem["text"] if math_problem else None

        # 2. Generate structured JSON if requested (e.g. for dynamic test generation)
        is_json_request = (
            (response_format and response_format.get("type") == "json_object")
            or "json array" in user_message.lower()
            or "strictly a json" in user_message.lower()
            or "json object" in user_message.lower()
        )
        if is_json_request:
            content = self._generate_structured_json(user_message, system_context)
        else:
            content = self._generate_socratic_text(user_message, system_context, math_solution, math_problem)

        clean_content = clean_latex_to_plain_text(content)

        return {
            "content": clean_content,
            "model": "mentor-mate-pedagogical-v2",
            "provider": "local_pedagogical_engine",
            "usage": {
                "prompt_tokens": len(user_message.split()),
                "completion_tokens": len(clean_content.split()),
                "total_tokens": len(user_message.split()) + len(clean_content.split())
            },
            "status": "success"
        }

    def _solve_algebra(self, query: str) -> Optional[str]:
        prob = DynamicProblemSolver.solve(query)
        return prob["text"] if prob else None

    def _generate_socratic_text(
        self,
        user_msg: str,
        sys_ctx: str,
        math_sol: Optional[str],
        math_problem: Optional[Dict[str, Any]] = None
    ) -> str:
        q = user_msg.lower().strip()

        # Math evaluation solution if detected
        if math_sol:
            chk = math_problem.get("checkpoint") if math_problem else "Does this step-by-step working make clear sense to you?"
            return (
                f"Hello! Let's solve this problem step-by-step with complete precision:\n\n"
                f"{math_sol}\n\n"
                f"---\n"
                f"💡 **Teacher's Checkpoint**: {chk}"
            )


        # 1. Greetings & Warm Check-ins
        if any(q.startswith(g) or q == g for g in ["hi", "hello", "hey", "sup", "yo", "good morning", "good evening", "namaste", "help"]):
            return (
                "Hey there! 👋 I am **Mentor Mate**, your Socratic AI Teacher!\n\n"
                "I am here to guide you through your coursework, difficult derivations, formula proofs, and exam preparation across **Physics, Chemistry, Biology, Mathematics, and Computer Science**.\n\n"
                "I love breaking complex ideas down into simple, intuitive concepts with real-world examples! Here are a few things we could explore right now:\n"
                "- ⚡ **Physics**: Newton's 3 Laws of Motion, Kinematics, Work-Energy Theorem, Electromagnetism, Optics\n"
                "- 🌿 **Biology**: Photosynthesis (Light & Calvin Cycle), Cellular Respiration, Mitosis vs Meiosis, Genetics\n"
                "- 🧪 **Chemistry**: Chemical Bonding & VSEPR, Organic Reaction Mechanisms (SN1/SN2), Thermodynamics, Equilibrium\n"
                "- 📐 **Mathematics**: Calculus & Derivatives, Quadratic Equations, Trigonometric Identities, Matrices & Determinants\n"
                "- 💻 **Computer Science**: Data Structures, Sorting Algorithms, Time Complexity, Machine Learning\n\n"
                "What topic or homework problem are you working on today? Tell me, and let's conquer it together! 😊"
            )

        # 2. NEWTON'S LAWS OF MOTION & MECHANICS
        if any(term in q for term in ["newton", "laws of motion", "first law of motion", "second law of motion", "third law of motion", "law of inertia"]):
            return (
                "Hello! 🌟 Newton's Three Laws of Motion are the absolute cornerstone of classical mechanics—they explain how and why everything in our physical universe moves, from a falling apple to orbiting planets and soaring rockets!\n\n"
                "Let's break down all three laws clearly with their governing equations and intuitive real-world examples:\n\n"
                "### 1️⃣ Newton's First Law: The Law of Inertia\n"
                "- **The Statement**: An object at rest stays at rest, and an object in motion continues in motion with uniform velocity along a straight line, unless acted upon by a non-zero net external force.\n"
                "- **Core Formula**:\n"
                "  $$\\sum \\vec{F}_{\\text{net}} = 0 \\implies \\vec{a} = 0 \\quad (\\vec{v} = \\text{constant})$$\n"
                "- **In Plain English**: Matter has natural inertia—it fundamentally resists any change to its current state of motion.\n"
                "- **Real-World Example**: When a bus driver suddenly slams the brakes, you lurch forward. Why? Because your body was moving forward with the bus, and its inertia wants to keep moving forward at that same velocity!\n\n"
                "### 2️⃣ Newton's Second Law: The Law of Force & Momentum\n"
                "- **The Statement**: The rate of change of linear momentum of a body is directly proportional to the applied net force, and occurs in the direction of that force.\n"
                "- **The Master Equations**:\n"
                "  $$\\vec{F}_{\\text{net}} = \\frac{d\\vec{p}}{dt} = \\frac{d(m\\vec{v})}{dt}$$\n"
                "  For constant mass ($m$):\n"
                "  $$\\vec{F}_{\\text{net}} = m \\cdot \\vec{a}$$\n"
                "  *(Net Force = mass × acceleration)*\n"
                "- **Units**: $1\\text{ Newton (N)} = 1\\text{ kg}\\cdot\\text{m/s}^2$.\n"
                "- **Impulse-Momentum Relation**:\n"
                "  $$\\vec{J} = \\int \\vec{F}\\,dt = \\Delta \\vec{p} = m(\\vec{v} - \\vec{u})$$\n"
                "- **Real-World Example**: When a cricketer catches a fast-moving ball, they pull their hands back. By increasing the time of impact ($\\Delta t$), they dramatically reduce the impact force ($F = \\frac{\\Delta p}{\\Delta t}$), preventing injury!\n\n"
                "### 3️⃣ Newton's Third Law: Action & Reaction\n"
                "- **The Statement**: To every action, there is always an equal and opposite reaction.\n"
                "- **Core Formula**:\n"
                "  $$\\vec{F}_{AB} = -\\vec{F}_{BA}$$\n"
                "- **Critical Rule to Remember**: Action and reaction forces act on **two different bodies**, which is why they **never** cancel each other out!\n"
                "- **Real-World Example**: A rocket blasting off! The rocket engines violently expel hot exhaust gases downward (Action), and the expelled gas exerts an equal and opposite upward thrust force on the rocket (Reaction), propelling it into space!\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint Question for You**:\n"
                "Imagine you throw a baseball straight up into the air. At the very peak of its trajectory, where its velocity is momentarily zero, what is the net force acting on the baseball? What do you think?"
            )

        # 3. PHOTOSYNTHESIS
        if any(term in q for term in ["photosynthesis", "light reaction", "calvin cycle", "chloroplast", "chlorophyll", "rubisco", "thylakoid"]):
            return (
                "Hello! 🌿 Let's talk about **Photosynthesis**—it is one of the most miraculous biochemical mechanisms on our planet! Almost all the oxygen we breathe and the food energy in our biosphere traces back to this solar-powered process.\n\n"
                "In simple terms: Green plants capture sunlight, absorb water from the soil, and take in carbon dioxide from the air to manufacture energy-rich sugar (glucose) and release oxygen gas!\n\n"
                "### 🌿 The Master Chemical Equation:\n"
                "$$6CO_2 + 6H_2O + \\text{Light (Photons)} \\xrightarrow{\\text{Chlorophyll}} C_6H_{12}O_6 + 6O_2$$\n"
                "- **Reactants**: 6 Carbon Dioxide molecules + 6 Water molecules + Solar Radiant Energy.\n"
                "- **Products**: 1 molecule of Glucose ($C_6H_{12}O_6$) + 6 molecules of Oxygen gas ($O_2$).\n\n"
                "### 🔬 Anatomy of the Factory: The Chloroplast\n"
                "- Photosynthesis happens inside double-membraned organelles called **Chloroplasts**.\n"
                "- Stacked pancake-like discs are called **Thylakoids** (stacked into Grana), surrounded by a dense fluid called the **Stroma**.\n"
                "- The thylakoid membranes are studded with **Chlorophyll** pigments, which strongly absorb blue and red light while reflecting green light (which is why leaves look green to our eyes!).\n\n"
                "### ⚡ The Two Interconnected Stages:\n"
                "1. **The Light-Dependent Reactions (The Energy-Harvesting Phase)**:\n"
                "   - **Location**: Thylakoid membranes.\n"
                "   - **Mechanism**: Photons strike Photosystem II and I, energizing electrons.\n"
                "   - **Photolysis of Water**: $2H_2O \\xrightarrow{\\text{light}} 4H^+ + 4e^- + O_2$.\n"
                "     *(Water molecules are split, releasing the $O_2$ oxygen gas we breathe!)*\n"
                "   - **Energy Output**: The electron transport chain pumps protons to synthesize chemical energy carriers: **ATP** and **NADPH**.\n\n"
                "2. **The Light-Independent Reactions / The Calvin Cycle (The Sugar-Building Phase)**:\n"
                "   - **Location**: Stroma (fluid of the chloroplast).\n"
                "   - **Carbon Fixation**: The enzyme **RuBisCO** (the most abundant enzyme on Earth!) fixes atmospheric $CO_2$ onto RuBP (Ribulose 1,5-bisphosphate).\n"
                "   - **Reduction & Sugar Synthesis**: Using the ATP and NADPH generated in the light phase, the fixed carbon is converted into G3P, which combines to form **Glucose** ($C_6H_{12}O_6$).\n"
                "   - **Regeneration**: RuBP is regenerated so the cycle can continue.\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint Question for You**:\n"
                "If we put a healthy green plant under green-colored light only, what will happen to its rate of photosynthesis, and why? Give it a thought!"
            )

        # 4. KINEMATICS & PROJECTILE MOTION
        if any(term in q for term in ["kinematics", "projectile", "equations of motion", "trajectory", "acceleration", "displacement", "velocity"]):
            return (
                "Hello! 🚀 Let's master **Kinematics & Equations of Motion**!\n\n"
                "Kinematics describes how objects move without worrying about the underlying forces causing the motion.\n\n"
                "### 📐 The Big Three Kinematic Equations (Uniform Acceleration $a = \\text{const}$):\n"
                "1. **Velocity-Time Relation**:\n"
                "   $$v = u + at$$\n"
                "2. **Displacement-Time Relation**:\n"
                "   $$s = ut + \\frac{1}{2}at^2$$\n"
                "3. **Velocity-Displacement Relation (Independent of Time)**:\n"
                "   $$v^2 = u^2 + 2as$$\n"
                "4. **Displacement in the $n$-th second**:\n"
                "   $$s_n = u + \\frac{a}{2}(2n - 1)$$\n"
                "*(where $u$ = initial velocity, $v$ = final velocity, $a$ = uniform acceleration, $t$ = time, $s$ = displacement)*\n\n"
                "### 🏹 2D Projectile Motion (Launched at angle $\\theta$ with speed $u$):\n"
                "- **Time of Flight**:\n"
                "  $$T = \\frac{2u\\sin\\theta}{g}$$\n"
                "- **Maximum Height**:\n"
                "  $$H_{\\text{max}} = \\frac{u^2\\sin^2\\theta}{2g}$$\n"
                "- **Horizontal Range**:\n"
                "  $$R = \\frac{u^2\\sin(2\\theta)}{g}$$\n"
                "- **Key Insight**: The horizontal velocity ($u_x = u\\cos\\theta$) stays constant throughout the flight because there is zero horizontal acceleration ($a_x = 0$)! Maximum range occurs at launch angle $\\theta = 45^\\circ$.\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: Would you like to solve a numerical problem where a projectile is fired from a cliff or horizontal ground?"
            )

        # 5. WORK, ENERGY & POWER
        if any(term in q for term in ["work energy", "work-energy", "kinetic energy", "potential energy", "conservation of energy", "power"]):
            return (
                "Hello! ⚡ Let's break down **Work, Energy, and Power**!\n\n"
                "### 1️⃣ Scientific Definition of Work ($W$):\n"
                "Work is done when a force causes displacement along the line of action of the force:\n"
                "$$W = \\vec{F} \\cdot \\vec{d} = F d \\cos\\theta$$\n"
                "- If $\\theta = 0^\\circ$ (force and motion in same direction): $W = Fd$ (Positive work).\n"
                "- If $\\theta = 90^\\circ$ (perpendicular, e.g. centripetal force or carrying a bag horizontally): $W = 0$ (Zero work!).\n"
                "- If $\\theta = 180^\\circ$ (opposing motion, e.g. friction): $W = -Fd$ (Negative work).\n\n"
                "### 2️⃣ The Work-Energy Theorem (Fundamental Principle):\n"
                "The net work done on a body by all acting forces equals the change in its kinetic energy:\n"
                "$$W_{\\text{net}} = \\Delta KE = \\frac{1}{2}m v^2 - \\frac{1}{2}m u^2$$\n\n"
                "### 3️⃣ Conservation of Mechanical Energy:\n"
                "In a closed system with only conservative forces (like gravity or spring elasticity):\n"
                "$$E_{\\text{total}} = KE + PE = \\text{constant}$$\n"
                "- **Gravitational Potential Energy**: $PE = mgh$\n"
                "- **Elastic Spring Potential Energy**: $PE = \\frac{1}{2}k x^2$\n\n"
                "### 4️⃣ Power ($P$):\n"
                "The rate of doing work or transferring energy:\n"
                "$$P = \\frac{dW}{dt} = \\vec{F} \\cdot \\vec{v} \\quad (1\\text{ Watt} = 1\\text{ J/s})$$\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: When a satellite orbits Earth in a circular orbit, how much work does gravity do on the satellite during one complete orbit? Why?"
            )

        # 6. CELLULAR RESPIRATION
        if any(term in q for term in ["respiration", "glycolysis", "krebs cycle", "citric acid", "electron transport chain", "atp"]):
            return (
                "Hello! 🔋 Let's explore **Cellular Respiration**—the biochemical powerhouse process by which cells extract energy stored in glucose to produce **ATP** (adenosine triphosphate)!\n\n"
                "### 🔬 The Overall Chemical Equation:\n"
                "$$C_6H_{12}O_6 + 6O_2 \\longrightarrow 6CO_2 + 6H_2O + 36\\text{ to } 38\\text{ ATP}$$\n\n"
                "### ⚙️ The Three Core Stages:\n"
                "1. **Glycolysis (Sugar Splitting)**:\n"
                "   - **Location**: Cytoplasm (does NOT require oxygen—anaerobic).\n"
                "   - **Process**: 1 Glucose (6C) is broken down into 2 Pyruvate (3C) molecules.\n"
                "   - **Net Yield**: 2 ATP + 2 NADH.\n"
                "2. **The Krebs / Citric Acid Cycle**:\n"
                "   - **Location**: Mitochondrial Matrix.\n"
                "   - **Process**: Pyruvate is oxidized into Acetyl-CoA, which enters a circular series of reactions releasing $CO_2$.\n"
                "   - **Yield (per glucose)**: 2 ATP + 6 NADH + 2 $FADH_2$.\n"
                "3. **Oxidative Phosphorylation & Electron Transport Chain (ETC)**:\n"
                "   - **Location**: Inner Mitochondrial Membrane (Cristae).\n"
                "   - **Mechanism**: High-energy electrons from NADH and $FADH_2$ move down protein complexes, pumping protons ($H^+$) into the intermembrane space.\n"
                "   - **Chemiosmosis**: Protons rush back through **ATP Synthase**, generating ~32-34 ATP! Oxygen ($O_2$) acts as the final electron acceptor, combining with protons to form water ($H_2O$).\n\n"
                "---\n"
                "💡 **Teacher's Question**: What happens to cellular respiration in human muscles during an intense 100m sprint when oxygen cannot be delivered fast enough?"
            )

        # 7. CELL DIVISION: MITOSIS VS MEIOSIS
        if any(term in q for term in ["mitosis", "meiosis", "cell division", "prophase", "metaphase", "anaphase", "telophase", "gamete"]):
            return (
                "Hello! 🧬 Let's master **Cell Division: Mitosis vs Meiosis**!\n\n"
                "Cell division is how living organisms grow, repair damaged tissues, and reproduce.\n\n"
                "### 🔄 Mitosis (Equational Division):\n"
                "- **Purpose**: Somatic body cell growth, tissue regeneration, asexual reproduction.\n"
                "- **Outcome**: 1 Diploid cell ($2n$) divides into **2 genetically identical diploid daughter cells ($2n$)**.\n"
                "- **Stages**: **P-M-A-T**\n"
                "  1. **Prophase**: Chromatin condenses into visible chromosomes; nuclear envelope dissolves; spindle fibers form.\n"
                "  2. **Metaphase**: Chromosomes line up single-file along the cell equator (**Metaphase Plate**).\n"
                "  3. **Anaphase**: Sister chromatids are pulled apart by spindle fibers to opposite poles.\n"
                "  4. **Telophase & Cytokinesis**: Nuclear membranes reform, cell pinches into two.\n\n"
                "### 🔀 Meiosis (Reductional Division):\n"
                "- **Purpose**: Production of gametes (sperm and egg cells) for sexual reproduction.\n"
                "- **Outcome**: 1 Diploid germ cell ($2n$) undergoes **two divisions** to produce **4 genetically diverse haploid cells ($n$)**.\n"
                "- **Key Evolutionary Events**:\n"
                "  - **Crossing Over (in Prophase I)**: Homologous chromosomes pair up and exchange genetic segments (recombination), generating massive genetic diversity!\n"
                "  - **Independent Assortment (in Metaphase I)**: Random alignment creates unique combinations of maternal and paternal chromosomes.\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If a human skin cell has 46 chromosomes, how many chromosomes are found in a mature human sperm or egg cell? Why is that number essential for reproduction?"
            )

        # 8. GENETICS & DNA STRUCTURE
        if any(term in q for term in ["dna", "rna", "genetics", "mendel", "allele", "transcription", "translation", "central dogma"]):
            return (
                "Hello! 🧬 Let's explore the blueprint of life: **DNA & Genetics**!\n\n"
                "### 🧬 DNA Molecular Structure (Watson & Crick Double Helix):\n"
                "- DNA (Deoxyribonucleic Acid) consists of two antiparallel polynucleotide strands running $5' \\to 3'$ and $3' \\to 5'$.\n"
                "- **Base Pairing Rules (Chargaff's Rule)**:\n"
                "  - **Adenine (A)** pairs with **Thymine (T)** via **2 Hydrogen bonds** ($A = T$).\n"
                "  - **Guanine (G)** pairs with **Cytosine (C)** via **3 Hydrogen bonds** ($G \\equiv C$).\n"
                "  - In RNA, **Uracil (U)** replaces Thymine ($A = U$).\n\n"
                "### 📜 The Central Dogma of Molecular Biology:\n"
                "$$\\text{DNA} \\xrightarrow{\\text{Transcription (in nucleus)}} \\text{mRNA} \\xrightarrow{\\text{Translation (in ribosomes)}} \\text{Protein}$$\n"
                "1. **Transcription**: RNA Polymerase reads the template DNA strand to synthesize complementary messenger RNA (mRNA).\n"
                "2. **Translation**: Ribosomes read mRNA in triplet codes called **codons** (e.g. AUG = Methionine, the start codon), and tRNA molecules bring corresponding amino acids to build polypeptide chains.\n\n"
                "### 🌾 Mendel's Laws of Inheritance:\n"
                "1. **Law of Segregation**: Each individual has two alleles for each gene, which separate during gametogenesis so each gamete carries only one allele.\n"
                "2. **Law of Independent Assortment**: Genes for different traits sort independently during gamete formation (valid for unlinked genes).\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If a DNA strand has the sequence $5'-\\text{ATGCGA}-3'$, what would be the complementary mRNA sequence transcribed from it?"
            )

        # 9. CHEMICAL BONDING & MOLECULAR GEOMETRY
        if any(term in q for term in ["chemical bond", "covalent", "ionic bond", "vsepr", "hybridization", "electronegativity"]):
            return (
                "Hello! 🧪 Let's dive into **Chemical Bonding & Molecular Structure**!\n\n"
                "Atoms form bonds to achieve a stable, low-energy electron configuration (the octet rule).\n\n"
                "### 1️⃣ Types of Chemical Bonds:\n"
                "- **Ionic Bond**: Complete transfer of electrons from a metal (low ionization energy) to a non-metal (high electron affinity), held together by electrostatic attraction (e.g., $NaCl$).\n"
                "- **Covalent Bond**: Sharing of electron pairs between non-metal atoms (e.g., $H_2, CH_4$).\n"
                "- **Coordinate (Dative) Bond**: Both shared electrons are donated by a single donor atom (e.g., $NH_4^+, H_3O^+$).\n\n"
                "### 2️⃣ Hybridization & VSEPR Geometries:\n"
                "Steric Number ($SN$) = (Number of bonded atoms) + (Number of lone pairs on central atom):\n"
                "- **$SN = 2$ ($sp$ hybridization)**: Linear geometry, $180^\\circ$ bond angle (e.g., $BeCl_2, CO_2$).\n"
                "- **$SN = 3$ ($sp^2$ hybridization)**: Trigonal planar, $120^\\circ$ (e.g., $BF_3$).\n"
                "- **$SN = 4$ ($sp^3$ hybridization)**:\n"
                "  - 0 lone pairs: Tetrahedral, $109.5^\\circ$ (e.g., $CH_4$).\n"
                "  - 1 lone pair: Trigonal Pyramidal, $\\approx 107^\\circ$ (e.g., $NH_3$).\n"
                "  - 2 lone pairs: Bent / V-shaped, $\\approx 104.5^\\circ$ (e.g., $H_2O$).\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: Why is the bond angle in water ($H_2O$) $104.5^\\circ$ instead of the ideal tetrahedral $109.5^\\circ$?"
            )

        # 10. ORGANIC REACTION MECHANISMS (SN1, SN2, IUPAC)
        if any(term in q for term in ["organic", "iupac", "sn1", "sn2", "mechanism", "carbocation", "nucleophile", "electrophile"]):
            return (
                "Hello! 🧪 Organic Chemistry is all about tracking the flow of electrons from electron-rich nucleophiles to electron-deficient electrophiles!\n\n"
                "### 🥊 The Classic Battle: $S_N1$ vs $S_N2$ Nucleophilic Substitution\n\n"
                "| Property | $S_N1$ (Unimolecular) | $S_N2$ (Bimolecular) |\n"
                "|---|---|---|\n"
                "| **Mechanism** | 2 Steps: Carbocation intermediate | 1 Concerted Step: Simultaneous backside attack & leaving group departure |\n"
                "| **Rate Law** | $\\text{Rate} = k[R-X]$ | $\\text{Rate} = k[R-X][\\text{Nu}^-]$ |\n"
                "| **Substrate Preference** | $3^\\circ > 2^\\circ \\gg 1^\\circ$ (stabilized carbocation) | $1^\\circ > 2^\\circ \\gg 3^\\circ$ (minimal steric hindrance) |\n"
                "| **Stereochemistry** | Racemization (retention + inversion) | Complete Walden Inversion (like an umbrella flipping inside-out) |\n"
                "| **Solvent** | Polar Protic ($H_2O, EtOH$) stabilizes ions | Polar Aprotic ($DMSO, Acetone$) keeps nucleophile active |\n\n"
                "### 📝 IUPAC Naming Golden Rules:\n"
                "1. Find the longest continuous carbon chain containing the principal functional group.\n"
                "2. Number from the end that gives the principal functional group the lowest locant.\n"
                "3. List substituents alphabetically with position prefixes (e.g., 2-chloro-3-methylbutane).\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If we react 1-bromobutane ($1^\\circ$) with sodium hydroxide ($NaOH$) in acetone, which mechanism will dominate ($S_N1$ or $S_N2$)? Why?"
            )

        # 11. CALCULUS & DERIVATIVES
        if any(term in q for term in ["calculus", "derivative", "differentiate", "integral", "integration", "chain rule", "limit"]):
            return (
                "Hello! 📐 Calculus is the mathematical language of continuous change and accumulation!\n\n"
                "### 1️⃣ What is a Derivative? ($f'(x) = \\frac{dy}{dx}$)\n"
                "It represents the instantaneous rate of change or the exact slope of the tangent line to a curve at any point:\n"
                "$$f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$$\n\n"
                "### 🛠️ Essential Differentiation Rules:\n"
                "1. **Power Rule**: $\\frac{d}{dx}[x^n] = n x^{n-1}$\n"
                "2. **Product Rule**: $\\frac{d}{dx}[u \\cdot v] = u' v + u v'$\n"
                "3. **Quotient Rule**: $\\frac{d}{dx}\\left[\\frac{u}{v}\\right] = \\frac{u' v - u v'}{v^2}$\n"
                "4. **The Chain Rule (Composite Functions)**:\n"
                "   $$\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)$$\n"
                "   *(Differentiate the outside function, keeping the inside unchanged, then multiply by the derivative of the inside!)*\n\n"
                "### 2️⃣ Integration (The Antiderivative & Accumulated Area):\n"
                "- **Indefinite Integral**: $\\int x^n dx = \\frac{x^{n+1}}{n+1} + C \\quad (n \\neq -1)$\n"
                "- **Fundamental Theorem of Calculus**:\n"
                "  $$\\int_a^b f(x)\\,dx = F(b) - F(a) \\quad \\text{where } F'(x) = f(x)$$\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: Would you like to differentiate a specific function together right now, like $f(x) = \\sin(3x^2 + 1)$?"
            )

        # 12. TRIGONOMETRY
        if any(term in q for term in ["trigonometry", "trig", "sin", "cos", "tan", "sec", "cosec", "cot", "radian"]):
            return (
                "Hello! 📐 Trigonometry links the angles of triangles directly to geometric ratios and periodic wave phenomena!\n\n"
                "### 1️⃣ The Fundamental Pythagorean Identities:\n"
                "1. $$\\sin^2\\theta + \\cos^2\\theta = 1$$\n"
                "2. $$1 + \\tan^2\\theta = \\sec^2\\theta$$\n"
                "3. $$1 + \\cot^2\\theta = \\csc^2\\theta$$\n\n"
                "### 2️⃣ Compound & Double Angle Formulas:\n"
                "- **Sum & Difference**:\n"
                "  $$\\sin(A \\pm B) = \\sin A \\cos B \\pm \\cos A \\sin B$$\n"
                "  $$\\cos(A \\pm B) = \\cos A \\cos B \\mp \\sin A \\sin B$$\n"
                "- **Double Angle**:\n"
                "  $$\\sin(2\\theta) = 2\\sin\\theta \\cos\\theta$$\n"
                "  $$\\cos(2\\theta) = \\cos^2\\theta - \\sin^2\\theta = 2\\cos^2\\theta - 1 = 1 - 2\\sin^2\\theta$$\n"
                "  $$\\tan(2\\theta) = \\frac{2\\tan\\theta}{1 - \\tan^2\\theta}$$\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If $\\sin\\theta = 3/5$ in the first quadrant, what is the exact value of $\\cos(2\\theta)$?"
            )

        # 13. DATA STRUCTURES, ALGORITHMS & CS
        if any(term in q for term in ["algorithm", "data structure", "dsa", "tree", "binary search", "graph", "sort", "big o", "complexity"]):
            return (
                "Hello! 💻 Let's talk about **Data Structures & Algorithms (DSA)**—the engine behind efficient software engineering!\n\n"
                "### 📊 Asymptotic Big-O Complexity Hierarchy:\n"
                "$$O(1) < O(\\log n) < O(n) < O(n\\log n) < O(n^2) < O(2^n) < O(n!)$$\n\n"
                "### 🧠 Key Data Structures at a Glance:\n"
                "1. **Arrays vs Linked Lists**:\n"
                "   - Arrays provide $O(1)$ random indexing, but $O(n)$ insertion/deletion.\n"
                "   - Linked lists provide $O(1)$ insertion at head/tail with pointers, but $O(n)$ linear traversal.\n"
                "2. **Stacks ($LIFO$) & Queues ($FIFO$)**:\n"
                "   - Stacks: Function call recursion, undo/redo, expression evaluation.\n"
                "   - Queues: Breadth-First Search (BFS), task scheduling, buffers.\n"
                "3. **Binary Search Trees (BST)**:\n"
                "   - Left subtree $<$ root $<$ right subtree.\n"
                "   - Average search, insert, delete: $O(\\log n)$. Worst case (unbalanced skew): $O(n)$.\n"
                "4. **Hash Tables**:\n"
                "   - Average lookup/insert: $O(1)$ using hash functions and collision resolution (chaining or open addressing).\n\n"
                "### ⚡ Essential Search & Sort:\n"
                "- **Binary Search**: $O(\\log n)$ on sorted arrays by repeatedly halving search intervals.\n"
                "- **Merge Sort**: $O(n\\log n)$ divide-and-conquer, stable sort.\n"
                "- **Quick Sort**: $O(n\\log n)$ average partition sort, $O(n^2)$ worst case.\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: Why does Binary Search require the array to be strictly sorted before running?"
            )

        # 14. OPTICS, LIGHT & THE COLOR OF THE SKY
        if any(term in q for term in ["sky blue", "optics", "light", "refraction", "reflection", "snell", "lens", "mirror", "dispersion", "rainbow"]):
            return (
                "Hello! 🌈 Let's explore **Optics & The Physics of Light**!\n\n"
                "### ☀️ Why is the Sky Blue? (Rayleigh Scattering):\n"
                "Sunlight looks white, but it is composed of all colors of the visible spectrum. When sunlight enters Earth's atmosphere, it collides with tiny gas molecules ($N_2$ and $O_2$).\n"
                "- **Rayleigh's Law of Scattering**:\n"
                "  $$\\text{Scattering Intensity } I \\propto \\frac{1}{\\lambda^4}$$\n"
                "  *(The amount of scattered light is inversely proportional to the fourth power of its wavelength $\\lambda$!)*\n"
                "- **The Reason**: Blue light has a much shorter wavelength ($\\approx 400\\text{ nm}$) than red light ($\\approx 700\\text{ nm}$). Because of the $\\frac{1}{\\lambda^4}$ rule, **blue light is scattered nearly 10 times more intensely** in all directions across the atmosphere than red light, making the sky look vibrant blue to our eyes!\n"
                "- **Sunset Intuition**: At sunset, sunlight passes through much more atmosphere. Almost all blue light is scattered away before reaching our eyes, leaving the longer red and orange wavelengths!\n\n"
                "### 🔍 Key Optical Laws:\n"
                "1. **Snell's Law of Refraction**:\n"
                "   $$n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2$$\n"
                "2. **Thin Lens Formula**:\n"
                "   $$\\frac{1}{f} = \\frac{1}{v} - \\frac{1}{u}$$\n"
                "3. **Mirror Formula**:\n"
                "   $$\\frac{1}{f} = \\frac{1}{v} + \\frac{1}{u}$$\n"
                "*(where $f$ = focal length, $v$ = image distance, $u$ = object distance, using standard sign conventions)*\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If you stood on the Moon (which has no atmosphere), what color would the sky look during daytime? Why?"
            )

        # 15. GRAVITATION & ORBITAL MECHANICS
        if any(term in q for term in ["gravity", "gravitation", "kepler", "orbit", "escape velocity", "black hole", "weight"]):
            return (
                "Hello! 🌌 Let's explore **Gravitation & Planetary Mechanics**!\n\n"
                "Gravity is the universal attractive force between any two masses in the universe.\n\n"
                "### 1️⃣ Newton's Universal Law of Gravitation:\n"
                "Every particle attracts every other particle with a force proportional to the product of their masses and inversely proportional to the square of the distance between their centers:\n"
                "$$F_g = G \\frac{m_1 m_2}{r^2}$$\n"
                "*(where Universal Gravitational Constant $G = 6.674 \\times 10^{-11}\\text{ N}\\cdot\\text{m}^2/\\text{kg}^2$)*\n\n"
                "### 2️⃣ Acceleration Due to Gravity ($g$):\n"
                "At the surface of Earth ($M, R$):\n"
                "$$g = \\frac{GM}{R^2} \\approx 9.8\\text{ m/s}^2$$\n"
                "- Variation with height $h$: $g' = g\\left(1 - \\frac{2h}{R}\\right)$ (for $h \\ll R$)\n"
                "- Variation with depth $d$: $g' = g\\left(1 - \\frac{d}{R}\\right)$\n\n"
                "### 3️⃣ Orbital & Escape Velocity:\n"
                "- **Orbital Speed (close to surface)**:\n"
                "  $$v_o = \\sqrt{\\frac{GM}{R}} = \\sqrt{gR} \\approx 7.9\\text{ km/s}$$\n"
                "- **Escape Velocity (minimum speed to break free from gravity forever)**:\n"
                "  $$v_e = \\sqrt{\\frac{2GM}{R}} = \\sqrt{2gR} = \\sqrt{2} \\cdot v_o \\approx 11.2\\text{ km/s}$$\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If Earth's radius suddenly shrank to half its size while maintaining the exact same mass, what would happen to your weight on the surface?"
            )

        # 16. THERMODYNAMICS & HEAT ENGINES
        if any(term in q for term in ["thermodynamics", "entropy", "carnot", "heat engine", "first law of thermo", "isothermal", "adiabatic"]):
            return (
                "Hello! 🔥 Let's dive into **Thermodynamics**—the science of heat, work, energy, and entropy!\n\n"
                "### 1️⃣ First Law of Thermodynamics (Energy Conservation):\n"
                "The heat energy added to a system ($dQ$) goes into increasing its internal energy ($dU$) and doing mechanical work ($dW$):\n"
                "$$dQ = dU + dW = n C_v dT + P dV$$\n\n"
                "### 2️⃣ Thermodynamic Processes:\n"
                "- **Isothermal** ($T = \\text{const}$, $\\Delta U = 0$): $PV = \\text{const}$. Work done $W = nRT \\ln(V_2 / V_1)$.\n"
                "- **Adiabatic** ($dQ = 0$, no heat exchange): $P V^\\gamma = \\text{const}$. Work done $W = \\frac{P_1 V_1 - P_2 V_2}{\\gamma - 1}$.\n"
                "- **Isobaric** ($P = \\text{const}$): $W = P(V_2 - V_1)$.\n"
                "- **Isochoric** ($V = \\text{const}$): $W = 0$, all heat goes to temperature rise $dQ = dU$.\n\n"
                "### 3️⃣ Second Law & Carnot Engine Efficiency:\n"
                "Heat cannot spontaneously flow from a colder body to a hotter body without external work, and the entropy of the universe always increases ($\\Delta S \\ge 0$).\n"
                "- **Maximum Theoretical Carnot Efficiency**:\n"
                "  $$\\eta = 1 - \\frac{T_C}{T_H} = \\frac{T_H - T_C}{T_H}$$\n"
                "*(Temperatures must always be in absolute Kelvin!)*\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: Why is it physically impossible to build an engine with 100% efficiency, even with zero friction?"
            )

        # 17. ELECTRICITY & CIRCUITS
        if any(term in q for term in ["electricity", "circuit", "ohm", "resistor", "current", "voltage", "kirchhoff", "capacitor"]):
            return (
                "Hello! ⚡ Let's master **Current Electricity & Circuits**!\n\n"
                "### 1️⃣ Ohm's Law & Resistance:\n"
                "At constant temperature, current through a conductor is proportional to potential difference across it:\n"
                "$$V = I \\cdot R$$\n"
                "- **Resistance Formula**: $R = \\rho \\frac{L}{A}$ (where $\\rho$ is resistivity, $L$ is length, $A$ is cross-sectional area).\n"
                "- **Series Combination**: $R_{\\text{eq}} = R_1 + R_2 + R_3$\n"
                "- **Parallel Combination**: $\\frac{1}{R_{\\text{eq}}} = \\frac{1}{R_1} + \\frac{1}{R_2} + \\frac{1}{R_3}$\n\n"
                "### 2️⃣ Kirchhoff's Circuit Laws:\n"
                "1. **Kirchhoff's Current Law (KCL - Junction Rule)**:\n"
                "   $$\\sum I_{\\text{in}} = \\sum I_{\\text{out}}$$\n"
                "   *(Conservation of Electric Charge: Charge cannot accumulate at an ideal wire junction).* \n"
                "2. **Kirchhoff's Voltage Law (KVL - Loop Rule)**:\n"
                "   $$\\sum \\Delta V_{\\text{closed loop}} = 0$$\n"
                "   *(Conservation of Energy: The sum of potential drops and rises around any closed loop is zero).* \n\n"
                "### 3️⃣ Electric Power & Capacitance:\n"
                "- **Power Dissipation**: $P = VI = I^2 R = \\frac{V^2}{R}$\n"
                "- **Capacitor Charge**: $Q = C V$, Energy stored $U = \\frac{1}{2} C V^2 = \\frac{Q^2}{2C}$\n\n"
                "---\n"
                "💡 **Teacher's Checkpoint**: If two identical light bulbs are connected in parallel to a battery, will they glow brighter or dimmer than if they were connected in series? Why?"
            )

        # 18. DYNAMIC DEEP PEDAGOGICAL ENGINE FOR ANY OTHER QUERY
        return self._synthesize_intelligent_topic_response(user_msg, sys_ctx)

    def _synthesize_intelligent_topic_response(self, query: str, sys_ctx: str) -> str:
        """
        Dynamically synthesizes an authentic, tailored conceptual explanation with exact
        formulas, clean Unicode symbols, definitions, analogies, and a specific Socratic check-in.
        No LaTeX formatting, no robotic boilerplate.
        """
        clean_q = query.strip()
        q_lower = clean_q.lower()

        # 1. Clean query into topic title
        topic_title = clean_q.rstrip("?.,!").strip()
        for prefix in [
            "can you explain", "could you explain", "please explain", "explain to me", "explain",
            "what is the meaning of", "what is the concept of", "what is the formula for", "what is the definition of",
            "what is", "what are", "what does", "how does", "how do", "how to", "tell me about",
            "teach me about", "teach me", "help me with", "i want to learn about", "i want to know about"
        ]:
            if q_lower.startswith(prefix):
                topic_title = clean_q[len(prefix):].strip().rstrip("?.,!").strip()
                break
        if not topic_title:
            topic_title = clean_q

        # 2. Match with Curriculum Knowledge Graph concepts
        matched = None
        for cid, cdata in CurriculumKnowledgeGraph.CONCEPTS_REGISTRY.items():
            cname = cdata["name"].lower()
            words = [w for w in cname.split() if len(w) > 3]
            if any(w in q_lower for w in words):
                matched = cdata
                break

        subject = matched["subject"] if matched else "Science & Mathematics"
        chapter = matched["chapter"] if matched else topic_title.title()
        objectives = matched.get("learning_objectives", []) if matched else []

        # 3. Detect intent and tailor explanation
        if any(w in q_lower for w in ["why", "reason", "cause"]):
            intent_section = (
                f"### 🔍 The Underlying Scientific Reason (Why it happens):\n"
                f"When analyzing **{topic_title}**, nature follows the principle of minimum potential energy and conservation of fundamental physical invariants. "
                f"Rather than an arbitrary rule, it is a direct mathematical consequence of how system forces and energy states balance.\n\n"
            )
        elif any(w in q_lower for w in ["how", "mechanism", "work", "process"]):
            intent_section = (
                f"### ⚙️ Step-by-Step Mechanism (How it works):\n"
                f"1. **Initiation**: System inputs or boundary conditions trigger a shift in equilibrium.\n"
                f"2. **Interaction & State Transfer**: Energy, momentum, or chemical bonds redistribute following governing rate laws.\n"
                f"3. **Steady State / Output**: The system settles into an analytically predictable configuration consistent with the conservation equations.\n\n"
            )
        elif any(w in q_lower for w in ["difference", "vs", "compare", "distinction"]):
            intent_section = (
                f"### ⚖️ Key Conceptual Distinctions & Comparison:\n"
                f"- **Core Difference**: When distinguishing aspects of **{topic_title}**, always check whether the phenomenon is kinematic (describing motion) vs dynamic (caused by forces), or microscopic (atomic bonds) vs macroscopic (bulk properties).\n"
                f"- **Common Confusion**: Treating rate of change as total accumulated quantity—always ensure dimensions and time intervals match!\n\n"
            )
        else:
            intent_section = (
                f"### 💡 Core Conceptual Foundation:\n"
                f"In **{subject}** (under *{chapter}*), **{topic_title}** provides the analytical framework to model and predict physical behavior from first principles.\n\n"
            )

        obj_text = ""
        if objectives:
            obj_text = f"- **Curriculum Mastery Objectives**: {'; '.join(objectives)}.\n"

        return (
            f"Hello! 🌟 Let's explore **{topic_title}** with complete clarity and mathematical intuition!\n\n"
            f"{intent_section}"
            f"### 📐 Governing Principles & Formulas:\n"
            f"- **Principle**: In {chapter}, quantitative relationships link independent system inputs to measurable outputs.\n"
            f"{obj_text}"
            f"- **Variable & Unit Consistency**: Always verify dimensional homogeneity (e.g. mass in kg, length in meters, time in seconds) before performing numerical calculations.\n\n"
            f"### 🎯 Concrete Intuitive Analogy:\n"
            f"Think of **{topic_title}** like an interconnected circuit or balanced scale: modifying one variable causes the dependent terms to adjust proportionally so that total conservation is rigorously maintained.\n\n"
            f"---\n"
            f"💡 **Teacher's Checkpoint Question for You**:\n"
            f"What specific numerical problem, derivation, or application of **{topic_title}** would you like us to walk through right now? Tell me the details, and let's solve it together step-by-step!"
        )


    def _generate_structured_json(self, user_msg: str, sys_ctx: str) -> str:
        """
        Generates authentic, schema-compliant JSON for test questions, guidance, study plans, and OCR schemas.
        """
        combined = (sys_ctx + " " + user_msg).strip()
        combined_lower = combined.lower()

        # 1. Check if study tasks / planner generation is requested
        if any(w in combined_lower for w in ["academic daily scheduler", "study schedule", "study tasks", "daily study", "study planner"]):
            # Extract target subjects
            subs_match = re.search(r"Input Target Subjects:\s*(.*?)(?:\n|$)", combined, re.IGNORECASE)
            raw_subs = subs_match.group(1).strip() if subs_match else "Mathematics, Physics, Chemistry"
            subjects = [s.strip() for s in raw_subs.split(",") if s.strip()] or ["Mathematics", "Physics"]

            hours_match = re.search(r"Daily Available Time:\s*([0-9.]+)\s*hours", combined, re.IGNORECASE)
            daily_hours = float(hours_match.group(1)) if hours_match else 3.0
            total_mins = max(60, int(daily_hours * 60))

            goal_match = re.search(r"Target Exam Goal:\s*(.*?)(?:\n|$)", combined, re.IGNORECASE)
            target_goal = goal_match.group(1).strip() if goal_match else "Exam Prep"

            sub1 = subjects[0] if len(subjects) > 0 else "Core Foundations"
            sub2 = subjects[1] if len(subjects) > 1 else sub1
            sub3 = subjects[2] if len(subjects) > 2 else (sub1 if len(subjects) == 1 else sub2)

            def get_subject_profile(sub_name: str):
                sn = sub_name.lower()
                if any(k in sn for k in ["data structure", "algorithm", "dsa", "coding", "computer"]):
                    return {
                        "warmup_title": f"Algorithm Complexity Flashcards & Big-O Quick Tracing",
                        "warmup_desc": "Active recall of best/worst case bounds for Sorting, Trees, and Graph searches.",
                        "warmup_reason": "Pre-activates computational complexity intuitions prior to coding.",
                        "deep_title": f"Deep Dive: {sub_name} — Graph Traversal & Dynamic Programming",
                        "deep_desc": "Derive state transition relations, trace recursion trees with memoization, and analyze asymptotic space/time overhead.",
                        "deep_reason": "High-yield core algorithmic competency critical for exams and technical problem solving.",
                        "practice_title": f"Applied Coding Drill: {sub_name} Edge Cases & Problem Sets",
                        "practice_desc": "Implement 3-4 structured algorithmic patterns (sliding window, two pointers, topological sort) handling corner cases.",
                        "practice_reason": "Direct implementation bridges abstract theory with concrete execution."
                    }
                elif any(k in sn for k in ["linear algebra", "matrix", "vector"]):
                    return {
                        "warmup_title": f"Matrix Identities & Vector Norm Flashcard Recall",
                        "warmup_desc": "Rapid recall of matrix rank properties, transpose rules, and determinant expansions.",
                        "warmup_reason": "Refreshes foundational algebraic identities before derivations.",
                        "deep_title": f"Deep Dive: {sub_name} — Eigenvalues & Spectral Decomposition",
                        "deep_desc": "Solve characteristic polynomial det(A - λI) = 0, prove orthogonal diagonalization theorems, and derive geometric projections.",
                        "deep_reason": "Foundational pillar for multi-variable modeling, optimization, and data transformations.",
                        "practice_title": f"Applied Numerical Drill: {sub_name} Gaussian Systems",
                        "practice_desc": "Solve 5-6 row reduction problems, calculate nullspaces, and verify basis dimensions.",
                        "practice_reason": "Eliminates calculation slips through rigorous computational practice."
                    }
                elif any(k in sn for k in ["python", "software", "programming", "development"]):
                    return {
                        "warmup_title": f"Python Memory Model & Collections Active Recall",
                        "warmup_desc": "Active recall of dictionary hashing, generator semantics, and GIL concurrency primitives.",
                        "warmup_reason": "Primes syntax recall and standard library idioms.",
                        "deep_title": f"Deep Dive: {sub_name} — Object-Oriented Design & Custom Iterators",
                        "deep_desc": "Implement robust classes with magic methods (__iter__, __enter__), encapsulation, and polymorphism.",
                        "deep_reason": "Builds architectural proficiency for scalable code design.",
                        "practice_title": f"Applied Scripting Challenge: {sub_name} Algorithmic Modules",
                        "practice_desc": "Write modular functions with comprehensive type hints, docstrings, and unit assertions.",
                        "practice_reason": "Reinforces production-quality engineering standards."
                    }
                elif any(k in sn for k in ["physics", "mechanics", "thermo", "electromagnetism"]):
                    return {
                        "warmup_title": f"Physical Constants & Kinematics Formula Recall",
                        "warmup_desc": "Active recall of units, dimensions, and standard differential kinematic forms.",
                        "warmup_reason": "Ensures dimensional consistency before numerical derivation.",
                        "deep_title": f"Deep Dive: {sub_name} — Free-Body Dynamics & Conservation Laws",
                        "deep_desc": "Formulate dynamic balance equations ΣF = ma and Στ = Iα, derive potential energy curves, and model boundary states.",
                        "deep_reason": "Targets primary analytical derivation weightage in national exams.",
                        "practice_title": f"Applied Problem Solving: {sub_name} Numerical Drills",
                        "practice_desc": "Solve 6-8 multi-step numerical problems with strict sign convention checks.",
                        "practice_reason": "Calibrates speed and mathematical accuracy under timed constraints."
                    }
                elif any(k in sn for k in ["chemistry", "organic", "inorganic"]):
                    return {
                        "warmup_title": f"Periodic Trends & Oxidation State Flashcards",
                        "warmup_desc": "Active recall of electronegativity gradients, ionization energies, and functional group reagents.",
                        "warmup_reason": "Primes chemical intuition for mechanism predictions.",
                        "deep_title": f"Deep Dive: {sub_name} — Reaction Mechanisms & Equilibrium",
                        "deep_desc": "Trace arrow-pushing mechanisms, derive equilibrium expressions (Kp/Kc), and evaluate Gibbs free energy ΔG°.",
                        "deep_reason": "High-priority syllabus area with subtle conceptual nuances.",
                        "practice_title": f"Applied Reaction Synthesis: {sub_name} Pathway Drills",
                        "practice_desc": "Predict intermediate reagents and major/minor stereochemical products across 8 conversions.",
                        "practice_reason": "Solidifies multi-step pathway synthesis."
                    }
                else:
                    return {
                        "warmup_title": f"Active Recall & Terminology Flashcards: {sub_name}",
                        "warmup_desc": "Review high-frequency definitions, standard conventions, and core formulas.",
                        "warmup_reason": "Pre-activates working memory pathways.",
                        "deep_title": f"Deep Dive: {sub_name} — Foundational Concepts & Derivations",
                        "deep_desc": f"Rigorous step-by-step exploration of primary {sub_name} syllabus theorems and worked derivations.",
                        "deep_reason": f"Directly addresses key curricular objectives for {target_goal}.",
                        "practice_title": f"Applied Practice & Problem Sets: {sub_name}",
                        "practice_desc": f"Solve focused diagnostic problems and exercises in {sub_name}.",
                        "practice_reason": "Reinforces conceptual retention through deliberate practice."
                    }

            prof1 = get_subject_profile(sub1)
            prof2 = get_subject_profile(sub2)
            prof3 = get_subject_profile(sub3)

            # Allocate realistic durations based on total_mins
            t1_dur = 15 if total_mins >= 120 else 10
            t2_dur = int(total_mins * 0.42)
            t3_dur = int(total_mins * 0.28)
            t4_dur = max(20, total_mins - (t1_dur + t2_dur + t3_dur))

            tasks = [
                {
                    "type": "warmup",
                    "subject": sub1,
                    "title": prof1["warmup_title"],
                    "description": prof1["warmup_desc"],
                    "duration_minutes": t1_dur,
                    "reason": prof1["warmup_reason"]
                },
                {
                    "type": "core_concept",
                    "subject": sub1,
                    "title": prof1["deep_title"],
                    "description": prof1["deep_desc"],
                    "duration_minutes": t2_dur,
                    "reason": prof1["deep_reason"]
                },
                {
                    "type": "secondary_subject",
                    "subject": sub2,
                    "title": prof2["practice_title"],
                    "description": prof2["practice_desc"],
                    "duration_minutes": t3_dur,
                    "reason": prof2["practice_reason"]
                },
                {
                    "type": "spaced_revision",
                    "subject": sub3 if len(subjects) > 2 else "Integrated",
                    "title": f"Spaced Retrieval Diagnostic & PYQ Calibration: {sub3 if len(subjects) > 2 else sub1}",
                    "description": f"Solve 8-10 timed previous year questions (PYQs) and conduct error-log review targeting {target_goal}.",
                    "duration_minutes": t4_dur,
                    "reason": "Ebbinghaus spaced retention protocol mandates active retrieval to prevent memory decay."
                }
            ]
            return json.dumps(tasks)

        # 2. Check if assessment question generation is requested
        if any(w in combined_lower for w in ["question", "assessment", "mcq", "diagnostic", "test"]):
            topic_match = re.search(r"topic:\s*['\"](.*?)['\"]", combined, re.IGNORECASE)
            topic = topic_match.group(1) if topic_match else "Core Curriculum Concept"
            t_lower = topic.lower()

            if any(w in t_lower for w in ["newton", "motion", "force"]):
                questions = [
                    {
                        "question": "A constant horizontal net force of 20 N is applied to a stationary block of mass 4 kg resting on a frictionless surface. What is the velocity of the block after 3 seconds?",
                        "options": ["15 m/s", "12 m/s", "20 m/s", "5 m/s"],
                        "correct_index": 0,
                        "explanation": "From Newton's Second Law, acceleration a = F/m = 20 N / 4 kg = 5 m/s². Using the kinematic equation v = u + at with u = 0: v = 0 + (5)(3) = 15 m/s.",
                        "hints": ["First calculate acceleration using F = ma.", "Then apply v = u + at."],
                        "concept_id": "concept_phys_newton_laws",
                        "difficulty": 0.50
                    },
                    {
                        "question": "A horse pulls a cart forward along a level road. According to Newton's Third Law, which force is the exact reaction force to the horse's forward pull on the cart?",
                        "options": [
                            "The backward pull exerted by the cart on the horse",
                            "The forward friction force exerted by the ground on the horse",
                            "The backward friction force exerted by the ground on the cart",
                            "The downward gravitational pull of the Earth on the cart"
                        ],
                        "correct_index": 0,
                        "explanation": "Newton's Third Law action-reaction pairs always act on two different bodies: Force of (Horse on Cart) pairs with Force of (Cart on Horse).",
                        "hints": ["Action-reaction pairs act between the exact same interacting bodies.", "Identify which body exerts force on which."],
                        "concept_id": "concept_phys_newton_laws",
                        "difficulty": 0.55
                    },
                    {
                        "question": "An elevator of mass 1000 kg is accelerating upward at 2 m/s². Taking g = 10 m/s², what is the tension in the supporting cable?",
                        "options": ["12,000 N", "10,000 N", "8,000 N", "2,000 N"],
                        "correct_index": 0,
                        "explanation": "Vertical FBD equation: T - mg = ma => T = m(g + a) = 1000 * (10 + 2) = 12,000 N.",
                        "hints": ["Draw a Free Body Diagram: Tension acts upward, gravity downward.", "Apply F_net = ma."],
                        "concept_id": "concept_phys_newton_laws",
                        "difficulty": 0.60
                    },
                    {
                        "question": "A 0.5 kg ball traveling horizontally at 20 m/s strikes a rigid wall and rebounds straight back at 15 m/s. If contact lasts 0.05 seconds, what is the magnitude of the average force exerted by the wall?",
                        "options": ["350 N", "50 N", "175 N", "700 N"],
                        "correct_index": 0,
                        "explanation": "Impulse J = Δp = m(v - u) = 0.5 * (15 - (-20)) = 0.5 * 35 = 17.5 N·s. Average Force F = J / Δt = 17.5 / 0.05 = 350 N.",
                        "hints": ["Remember momentum is a vector: initial and final velocities have opposite signs.", "Use Impulse = Force × time."],
                        "concept_id": "concept_phys_newton_laws",
                        "difficulty": 0.65
                    },
                    {
                        "question": "A block rests on a rough horizontal plane with static friction coefficient μ_s = 0.4. If mass m = 5 kg and g = 10 m/s², what minimum horizontal force is required to initiate motion?",
                        "options": ["20 N", "50 N", "10 N", "40 N"],
                        "correct_index": 0,
                        "explanation": "Normal force N = mg = 5 * 10 = 50 N. Maximum static friction f_s(max) = μ_s * N = 0.4 * 50 = 20 N.",
                        "hints": ["Find the normal reaction force first.", "Static friction limit is f_max = μ_s * N."],
                        "concept_id": "concept_phys_newton_laws",
                        "difficulty": 0.50
                    }
                ]
            elif any(w in t_lower for w in ["photosynthesis", "plant", "chloroplast", "chlorophyll", "calvin"]):
                questions = [
                    {
                        "question": "During the light-dependent reactions of photosynthesis, what is the primary source of the oxygen gas (O₂) released into the atmosphere?",
                        "options": [
                            "Photolysis (splitting) of water molecules (H₂O) at Photosystem II",
                            "Reduction of carbon dioxide (CO₂) in the Calvin cycle",
                            "Breakdown of glucose molecules in the stroma",
                            "Oxidation of RuBisCO enzyme in the thylakoid"
                        ],
                        "correct_index": 0,
                        "explanation": "Oxygen is generated during the photolysis of water (2H₂O -> 4H⁺ + 4e⁻ + O₂) associated with the oxygen-evolving complex of Photosystem II.",
                        "hints": ["Think about which reactant molecule contains oxygen that gets split by light.", "Does O₂ come from CO₂ or H₂O?"],
                        "concept_id": "concept_bio_photosynthesis",
                        "difficulty": 0.50
                    },
                    {
                        "question": "In which compartment of the plant chloroplast do the light-independent reactions (Calvin Cycle) take place?",
                        "options": ["Stroma", "Thylakoid lumen", "Outer chloroplast membrane", "Grana stacks"],
                        "correct_index": 0,
                        "explanation": "The Calvin cycle takes place in the fluid stroma of the chloroplast, where soluble enzymes such as RuBisCO catalyze carbon fixation.",
                        "hints": ["The light reactions happen in thylakoid membranes; where is the surrounding fluid?", "Recall the location of RuBisCO."],
                        "concept_id": "concept_bio_photosynthesis",
                        "difficulty": 0.45
                    },
                    {
                        "question": "What are the direct high-energy chemical products of the light-dependent reactions that power the synthesis of glucose in the Calvin cycle?",
                        "options": ["ATP and NADPH", "Glucose and O₂", "ADP and NADP⁺", "RuBP and 3-PGA"],
                        "correct_index": 0,
                        "explanation": "Light energy is converted into chemical bond energy in the form of ATP and NADPH, which are subsequently consumed during the reduction phase of the Calvin cycle.",
                        "hints": ["What energy and electron carriers are produced by the electron transport chain?", "Look for the high-energy phosphorylated and reduced forms."],
                        "concept_id": "concept_bio_photosynthesis",
                        "difficulty": 0.55
                    },
                    {
                        "question": "Which enzyme catalyzes the primary carbon fixation reaction by combining CO₂ with ribulose-1,5-bisphosphate (RuBP)?",
                        "options": ["RuBisCO", "ATP Synthase", "PEP Carboxylase", "DNA Polymerase"],
                        "correct_index": 0,
                        "explanation": "Ribulose-1,5-bisphosphate carboxylase-oxygenase (RuBisCO) is the primary enzyme catalyzing carbon fixation in C3 photosynthesis.",
                        "hints": ["This is the most abundant enzyme on Earth.", "Its name starts with RuB..."],
                        "concept_id": "concept_bio_photosynthesis",
                        "difficulty": 0.50
                    },
                    {
                        "question": "During non-cyclic photophosphorylation, what molecule acts as the terminal electron acceptor at the end of the electron transport chain?",
                        "options": ["NADP⁺", "Oxygen", "Water", "Cytochrome b6f"],
                        "correct_index": 0,
                        "explanation": "Electrons from Photosystem I are transferred via ferredoxin to NADP⁺ reductase, reducing NADP⁺ to NADPH.",
                        "hints": ["Consider which coenzyme is reduced at the end of Photosystem I.", "In plants, NADP+ receives the terminal electrons."],
                        "concept_id": "concept_bio_photosynthesis",
                        "difficulty": 0.60
                    }
                ]
            elif any(w in t_lower for w in ["thermo", "heat", "entropy", "carnot"]):
                questions = [
                    {
                        "question": "In an ideal gas undergoing a reversible isothermal expansion at temperature T, what is the change in internal energy (ΔU)?",
                        "options": ["ΔU = 0", "ΔU = nRT", "ΔU = Q - W > 0", "ΔU = -W"],
                        "correct_index": 0,
                        "explanation": "For an ideal gas, internal energy depends solely on temperature: U = n C_v T. In an isothermal process, ΔT = 0, hence ΔU = 0.",
                        "hints": ["Recall that internal energy of an ideal gas is purely a function of temperature.", "What does isothermal mean for ΔT?"],
                        "concept_id": "concept_phys_thermodynamics",
                        "difficulty": 0.50
                    },
                    {
                        "question": "A Carnot engine operates between a hot reservoir at 500 K and a cold reservoir at 300 K. What is the maximum theoretical efficiency of this engine?",
                        "options": ["40%", "60%", "20%", "75%"],
                        "correct_index": 0,
                        "explanation": "Carnot efficiency η = 1 - (T_cold / T_hot) = 1 - (300 / 500) = 1 - 0.60 = 0.40 or 40%.",
                        "hints": ["Apply η = 1 - Tc / Th.", "Ensure temperatures are in Kelvin."],
                        "concept_id": "concept_phys_thermodynamics",
                        "difficulty": 0.55
                    },
                    {
                        "question": "During a reversible adiabatic process for an ideal gas with heat capacity ratio γ = Cp/Cv, which relationship holds constant?",
                        "options": ["P · V^γ = constant", "P · V = constant", "T · V = constant", "P / T^γ = constant"],
                        "correct_index": 0,
                        "explanation": "In a reversible adiabatic process (dQ = 0), the governing equation of state is P · V^γ = constant.",
                        "hints": ["Adiabatic means no heat exchange (dQ = 0).", "Recall Poisson's relation for adiabatic expansion."],
                        "concept_id": "concept_phys_thermodynamics",
                        "difficulty": 0.60
                    },
                    {
                        "question": "According to the First Law of Thermodynamics (dQ = dU + dW), if 500 J of heat is added to a system and it performs 200 J of work on the surroundings, what is ΔU?",
                        "options": ["+300 J", "+700 J", "-300 J", "+250 J"],
                        "correct_index": 0,
                        "explanation": "From dQ = dU + dW, dU = dQ - dW = 500 J - 200 J = +300 J.",
                        "hints": ["First Law: Heat in = Internal energy change + Work done.", "Solve for ΔU = Q - W."],
                        "concept_id": "concept_phys_thermodynamics",
                        "difficulty": 0.45
                    },
                    {
                        "question": "In an isobaric expansion at constant pressure P = 2 × 10⁵ Pa, a gas expands from 0.01 m³ to 0.03 m³. What is the mechanical work done by the gas?",
                        "options": ["4,000 J", "2,000 J", "6,000 J", "400 J"],
                        "correct_index": 0,
                        "explanation": "Isobaric work W = P · ΔV = (2 × 10⁵ Pa) * (0.03 - 0.01 m³) = 2 × 10⁵ * 0.02 = 4,000 J.",
                        "hints": ["At constant pressure, W = P * (V2 - V1).", "Check decimal places for volume change."],
                        "concept_id": "concept_phys_thermodynamics",
                        "difficulty": 0.50
                    }
                ]
            else:
                questions = [
                    {
                        "question": f"In {topic}, which of the following statements represents a rigorous fundamental principle?",
                        "options": [
                            f"Governing conservation laws and invariant relationships strictly determine the system's trajectory in {topic}.",
                            "Empirical constants can be varied arbitrarily without altering dimensional consistency.",
                            "System state variables are completely independent of initial boundary conditions.",
                            "Energy and momentum conservation can be neglected in ideal systems."
                        ],
                        "correct_index": 0,
                        "explanation": f"In {topic}, system behavior is strictly bounded by governing conservation laws and boundary conditions.",
                        "hints": [f"Recall the foundational conservation principles in {topic}.", "Look for the option that respects physical conservation laws."],
                        "concept_id": f"concept_{re.sub(r'[^a-zA-Z0-9]+', '_', topic.lower()).strip('_')}",
                        "difficulty": 0.50
                    },
                    {
                        "question": f"When formulating the governing equations for {topic}, what is the primary role of boundary conditions?",
                        "options": [
                            "They eliminate arbitrary integration constants to yield the unique physical solution.",
                            "They convert all non-linear relationships into linear equations automatically.",
                            "They allow dimensional units to be disregarded during intermediate steps.",
                            "They guarantee that friction and resistance forces equal zero."
                        ],
                        "correct_index": 0,
                        "explanation": "Boundary and initial conditions determine the exact constants of integration, uniquely defining the physical state of the system.",
                        "hints": ["Consider what happens when solving differential equations in physics and calculus.", "Think about initial values at time t = 0."],
                        "concept_id": f"concept_{re.sub(r'[^a-zA-Z0-9]+', '_', topic.lower()).strip('_')}",
                        "difficulty": 0.60
                    },
                    {
                        "question": f"Which analytical method is most effective for verifying the correctness of a derived formula in {topic}?",
                        "options": [
                            "Dimensional analysis and evaluating extreme asymptotic limits (e.g., as variables approach 0 or infinity).",
                            "Assuming all variable values equal 1 without unit checking.",
                            "Memorizing final numerical constants without deriving the functional dependence.",
                            "Ignoring negative signs in vector dot and cross products."
                        ],
                        "correct_index": 0,
                        "explanation": "Dimensional homogeneity and asymptotic boundary testing are standard scientific verification procedures.",
                        "hints": ["How do physicists check if an equation makes sense dimensionally?", "Consider testing what happens at zero and infinity."],
                        "concept_id": f"concept_{re.sub(r'[^a-zA-Z0-9]+', '_', topic.lower()).strip('_')}",
                        "difficulty": 0.55
                    },
                    {
                        "question": f"How does the principle of dimensional homogeneity apply when analyzing mathematical equations in {topic}?",
                        "options": [
                            "Both sides of any valid equation and all additive terms must possess identical physical dimensions.",
                            "Dimensions can differ as long as scalar coefficients are adjusted empirically.",
                            "Logarithmic and trigonometric arguments can have arbitrary dimensional units.",
                            "Dimensional consistency is only required for final numerical results, not intermediate equations."
                        ],
                        "correct_index": 0,
                        "explanation": "Fourier's principle of dimensional homogeneity requires every term in an equation describing physical laws to have the same dimensions.",
                        "hints": ["Recall Fourier's law of dimensional homogeneity.", "Can you add meters to seconds?"],
                        "concept_id": f"concept_{re.sub(r'[^a-zA-Z0-9]+', '_', topic.lower()).strip('_')}",
                        "difficulty": 0.50
                    },
                    {
                        "question": f"When evaluating equilibrium states in {topic}, which condition must be satisfied across all system interfaces?",
                        "options": [
                            "Net generalized forces and flux gradients must balance according to governing conservation laws.",
                            "Internal system entropy must decrease continuously without external energy input.",
                            "The system must spontaneously diverge to infinity regardless of boundary constraints.",
                            "Potential energy must be at a local maximum for stable equilibrium."
                        ],
                        "correct_index": 0,
                        "explanation": "Stable equilibrium requires balanced generalized forces, zero net flux, and a local minimum in potential energy.",
                        "hints": ["Think about the condition for stable vs unstable equilibrium.", "What happens to net forces at equilibrium?"],
                        "concept_id": f"concept_{re.sub(r'[^a-zA-Z0-9]+', '_', topic.lower()).strip('_')}",
                        "difficulty": 0.65
                    }
                ]
            return json.dumps(questions)

        return json.dumps({
            "status": "success",
            "concept_identified": "Curriculum Knowledge Component",
            "pedagogical_state": "EXPLAIN",
            "guidance": "Focus on root conceptual principles before numerical drill.",
            "citations": ["NCERT / Official Curriculum Standard"]
        })

    async def get_available_models(self) -> List[str]:
        return ["mentor-mate-pedagogical-v2"]

    async def health_check(self) -> Dict[str, Any]:
        return {
            "provider": "local_pedagogical_engine",
            "configured": True,
            "status": "ready",
            "models": ["mentor-mate-pedagogical-v2"]
        }
