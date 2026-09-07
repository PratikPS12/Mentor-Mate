"""
Mentor Mate — Dynamic Curriculum & Syllabus Engine
Authentic syllabus mapping, genuine course generator, and goal-aligned question repository.
Supports: JEE, NEET, CUET, CBSE, ICSE, State Board, CET, across Classes 6 to 12 and Degree.
"""

from typing import Dict, Any, List, Optional

class CurriculumEngine:
    """
    Genuine educational curriculum and syllabus management engine.
    Maps student aim (JEE, NEET, CUET, CBSE, etc.) and class (6-12, Degree)
    to authentic syllabi, interactive study modules, and targeted diagnostic question items.
    """

    # 1. Authentic Syllabi by Goal & Subject
    SYLLABUS_REGISTRY: Dict[str, Dict[str, Any]] = {
        "JEE": {
            "name": "JEE (Main & Advanced) Engineering Track",
            "subjects": ["Physics", "Chemistry", "Math"],
            "applicable_classes": ["11", "12", "Degree"],
            "description": "Comprehensive engineering entrance curriculum covering Advanced Mechanics, Electromagnetism, Physical/Organic/Inorganic Chemistry, and Calculus & Coordinate Geometry.",
            "topics": {
                "Physics": ["Kinematics & Dynamics", "Rotational Mechanics", "Thermodynamics & Waves", "Electrostatics & Current", "Magnetic Effects & EMI", "Optics & Modern Physics"],
                "Chemistry": ["Organic Reaction Mechanisms", "Chemical Bonding & Molecular Structure", "Thermodynamics & Equilibrium", "Coordination Compounds", "Electrochemistry & Kinetics"],
                "Math": ["Differential & Integral Calculus", "Quadratic Equations & Complex Numbers", "Vectors & 3D Geometry", "Matrices & Determinants", "Coordinate Geometry & Conics"]
            }
        },
        "NEET": {
            "name": "NEET Medical Entrance Track",
            "subjects": ["Biology", "Physics", "Chemistry"],
            "applicable_classes": ["11", "12", "Degree"],
            "description": "National Eligibility cum Entrance Test curriculum emphasizing NCERT Biology (Botany & Zoology), Medical Physics applications, and Organic/Biochemical Chemistry.",
            "topics": {
                "Biology": ["Human Physiology & Organ Systems", "Genetics & Molecular Basis of Inheritance", "Cell Biology & Biomolecules", "Ecology & Environmental Biology", "Plant Physiology & Reproduction", "Biotechnology & Its Applications"],
                "Physics": ["Mechanics & Properties of Matter", "Wave Optics & Sound", "Thermal Physics", "Electrodynamics & Optics", "Atomic & Nuclear Physics"],
                "Chemistry": ["Biomolecules & Polymers", "Organic Compounds containing O & N", "Chemical Equilibrium & Solutions", "Periodic Trends & Coordination Chemistry", "Hydrocarbons"]
            }
        },
        "CUET": {
            "name": "CUET (Common University Entrance Test)",
            "subjects": ["Physics", "Chemistry", "Math", "Biology", "General Aptitude"],
            "applicable_classes": ["11", "12", "Degree"],
            "description": "National university admissions curriculum combining Class 12 NCERT domain disciplines with General Test reasoning and numerical aptitude.",
            "topics": {
                "Physics": ["Electromagnetism", "Optics", "Modern Physics", "Electronic Devices"],
                "Chemistry": ["Solid State & Solutions", "Electrochemistry", "Haloalkanes & Biomolecules"],
                "Math": ["Relations, Functions & Calculus", "Linear Programming", "Probability & Vectors"],
                "Biology": ["Reproduction & Genetics", "Biology in Human Welfare", "Ecology"],
                "General Aptitude": ["Logical & Analytical Reasoning", "Numerical Ability", "Data Interpretation"]
            }
        },
        "CBSE": {
            "name": "CBSE School & Board Curriculum",
            "subjects": ["Math", "Science", "Social Science"],
            "applicable_classes": ["6", "7", "8", "9", "10", "11", "12"],
            "description": "National standard NCERT board curriculum focusing on foundational derivations, practical application questions, and structured problem-solving.",
            "topics": {
                "Math": ["Real Numbers & Arithmetic Progressions", "Polynomials & Quadratic Equations", "Coordinate Geometry & Triangles", "Trigonometry & Surface Areas", "Statistics & Probability"],
                "Science": ["Chemical Reactions, Acids & Bases", "Life Processes & Heredity", "Light, Optics & Electricity", "Magnetic Effects & Natural Resources", "Force, Motion & Gravitation"]
            }
        },
        "ICSE": {
            "name": "ICSE / ISC Board Curriculum",
            "subjects": ["Math", "Physics", "Chemistry", "Biology"],
            "applicable_classes": ["6", "7", "8", "9", "10", "11", "12"],
            "description": "CISCE syllabus with extensive laboratory applications, conceptual breadth, and rigorous numerical practice.",
            "topics": {
                "Math": ["Commercial Mathematics & Banking", "Algebra & Matrices", "Geometry & Mensuration", "Trigonometry & Statistics"],
                "Physics": ["Force, Work, Power & Energy", "Light & Sound", "Electricity & Magnetism", "Radioactivity"],
                "Chemistry": ["Periodic Properties & Chemical Bonding", "Study of Acids, Bases & Salts", "Analytical & Organic Chemistry"],
                "Biology": ["Basic Biology & Plant Physiology", "Human Anatomy & Physiology", "Population & Pollution"]
            }
        },
        "State Board": {
            "name": "State Board Secondary & Higher Secondary",
            "subjects": ["Math", "Science"],
            "applicable_classes": ["6", "7", "8", "9", "10", "11", "12"],
            "description": "State curriculum aligned with national core syllabus guidelines with regional contextual examples and board pattern problem banks.",
            "topics": {
                "Math": ["Algebra & Linear Equations", "Geometry & Mensuration", "Arithmetic & Commercial Math"],
                "Science": ["Matter & Chemical Bonding", "Living Organisms & Life Functions", "Physical Principles of Energy & Motion"]
            }
        },
        "CET": {
            "name": "State CET Entrance Curriculum",
            "subjects": ["Physics", "Chemistry", "Math", "Biology"],
            "applicable_classes": ["11", "12", "Degree"],
            "description": "Speed-and-accuracy focused state engineering and pharmacy entrance test curriculum with intense objective practice.",
            "topics": {
                "Physics": ["Rotational Dynamics & Thermodynamics", "Electromagnetism & Wave Optics", "Semiconductors"],
                "Chemistry": ["Chemical Thermodynamics", "Solutions & Electrochemistry", "Organic Chemistry with Reaction Pathways"],
                "Math": ["Calculus, Vectors & 3D", "Trigonometric Functions & Differentiation"]
            }
        },
        "GATE": {
            "name": "GATE (Graduate Aptitude Test in Engineering)",
            "subjects": ["Computer Science", "Engineering Mathematics", "Operating Systems", "Algorithms", "Database Systems"],
            "applicable_classes": ["Degree", "Undergraduate"],
            "description": "Comprehensive graduate engineering entrance curriculum covering Advanced Algorithms, Computer Architecture, OS, DBMS, Networks, and Discrete Mathematics.",
            "topics": {
                "Computer Science": ["Algorithms & Complexity (Asymptotic, DP, Greedy)", "Data Structures (Trees, Graphs, B-Trees)", "Theory of Computation & Turing Machines", "Compiler Design & Parsing"],
                "Operating Systems": ["Process Synchronization & Semaphores", "Deadlocks & Banker's Algorithm", "Virtual Memory & Paging", "CPU Scheduling"],
                "Database Systems": ["Relational Algebra & Normalization (BCNF/3NF)", "Transactions & Serializability (ACID)", "B+ Tree Indexing"],
                "Engineering Mathematics": ["Linear Algebra & Eigenvalues", "Discrete Math & Combinatorics", "Probability & Distributions", "Graph Theory"]
            }
        },
        "Software Engineering & Placements": {
            "name": "Software Engineering & Technical Placements",
            "subjects": ["Data Structures & Algorithms", "System Design", "Database Management", "Object-Oriented Design"],
            "applicable_classes": ["Degree", "Undergraduate"],
            "description": "Industry-calibrated curriculum focusing on coding interviews, algorithmic optimization, scalable system architectures, and core computer science fundamentals.",
            "topics": {
                "Data Structures & Algorithms": ["Two Pointers & Sliding Window", "Binary Search & Divide & Conquer", "Tree & Graph Traversals (BFS/DFS)", "Dynamic Programming Patterns"],
                "System Design": ["Scalability & Load Balancing", "Caching & CDN Strategies", "Database Sharding & Replication", "Microservices & REST APIs"],
                "Database Management": ["SQL Mastery & Index Optimization", "NoSQL vs RDBMS Tradeoffs", "Transactions & Concurrency"],
                "Object-Oriented Design": ["SOLID Principles & Design Patterns", "Clean Code & Refactoring", "Low-Level Design (LLD)"]
            }
        },
        "Data Science & AI": {
            "name": "Data Science & Artificial Intelligence",
            "subjects": ["Machine Learning", "Python & Data Analysis", "Linear Algebra", "Probability & Statistics"],
            "applicable_classes": ["Degree", "Undergraduate"],
            "description": "Foundations of modern AI, statistical modeling, machine learning algorithms, deep learning architectures, and data engineering.",
            "topics": {
                "Machine Learning": ["Supervised Learning (Regression & Classification)", "Unsupervised Learning (Clustering & PCA)", "Model Evaluation & Bias-Variance Tradeoff"],
                "Probability & Statistics": ["Random Variables & Distributions", "Hypothesis Testing & p-values", "Bayesian Inference"],
                "Linear Algebra": ["Matrix Decompositions (SVD, Eigenvalues)", "Vector Spaces & Projections", "Tensors & Vector Operations"]
            }
        },
        "CAT": {
            "name": "CAT (Common Admission Test) Management Track",
            "subjects": ["Quantitative Aptitude", "Data Interpretation & Logical Reasoning", "Verbal Ability"],
            "applicable_classes": ["Degree", "Undergraduate"],
            "description": "Premier national management aptitude curriculum focusing on higher arithmetic, geometry, logical games, and analytical reading.",
            "topics": {
                "Quantitative Aptitude": ["Arithmetic (Percentages, Profit/Loss, Time/Speed/Work)", "Algebra & Functions", "Geometry & Mensuration", "Number Systems"],
                "Data Interpretation & Logical Reasoning": ["Arrangements & Puzzles", "Tables, Bar Graphs & Charts", "Binary Logic & Games"],
                "Verbal Ability": ["Reading Comprehension & Inferences", "Para-jumbles & Critical Reasoning", "Summary & Sentence Completion"]
            }
        },
        "Undergraduate": {
            "name": "Undergraduate University Engineering & Science Track",
            "subjects": ["Computer Science", "Engineering Mathematics", "Core Systems", "Quantitative Reasoning"],
            "applicable_classes": ["Degree", "Undergraduate"],
            "description": "University-level STEM curriculum spanning higher mathematics, computational fundamentals, algorithmic problem solving, and analytical engineering.",
            "topics": {
                "Computer Science": ["Data Structures & Algorithms", "Operating Systems", "Database Systems", "Computer Networks"],
                "Engineering Mathematics": ["Calculus & Differential Equations", "Linear Algebra & Matrices", "Discrete Mathematics"],
                "Core Systems": ["Digital Logic & Computer Architecture", "Signals & Information Theory", "Optimization & Numerical Methods"]
            }
        }
    }

    # 2. Authentic Question Bank mapped to Curriculum Tracks
    CURRICULUM_QUESTION_BANK: List[Dict[str, Any]] = [
        # --- JEE / High School Math ---
        {
            "id": "q_math_calculus_01",
            "concept_id": "concept_math_limits_derivatives",
            "tracks": ["JEE", "CUET", "CBSE", "ICSE", "CET"],
            "class_levels": ["11", "12", "Degree"],
            "subject": "Math",
            "topic": "Calculus",
            "difficulty": 0.45,
            "type": "multiple_choice",
            "question": "What is the derivative of f(x) = x^3 - 4x + 7 with respect to x?",
            "options": ["3x^2 - 4", "3x^2 - 4x", "x^2 - 4", "3x^2 + 7"],
            "correct_index": 0,
            "explanation": "Using the power rule d/dx[x^n] = n*x^(n-1): d/dx(x^3) = 3x^2, d/dx(-4x) = -4, and derivative of constant 7 is 0.",
            "misconception_distractors": {
                "1": {"type": "procedural_weakness", "description": "Forgot that d/dx(x) = 1, erroneously keeping x with -4."},
                "2": {"type": "power_rule_misapplication", "description": "Divided exponent instead of multiplying as coefficient."},
                "3": {"type": "constant_derivative_fallacy", "description": "Kept the constant term +7 instead of reducing to 0."}
            },
            "hints": [
                "Apply the sum and power rules of differentiation: d/dx[x^n] = n*x^(n-1).",
                "Differentiate term by term: x^3 becomes 3x^2, -4x becomes -4.",
                "The derivative of any constant value like 7 is zero."
            ],
            "source": "JEE Main / CBSE Class 12 Calculus"
        },
        {
            "id": "q_math_algebra_01",
            "concept_id": "concept_math_linear_eq",
            "tracks": ["JEE", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["6", "7", "8", "9", "10", "11", "12"],
            "subject": "Math",
            "topic": "Algebra",
            "difficulty": 0.25,
            "type": "multiple_choice",
            "question": "If 3x + 5 = 20, what is the value of x?",
            "options": ["5", "6", "4", "7"],
            "correct_index": 0,
            "explanation": "Subtract 5 from both sides: 3x = 15. Divide by 3: x = 5.",
            "misconception_distractors": {
                "1": {"type": "arithmetic_slip", "description": "Calculated 20 - 5 = 18 instead of 15."},
                "2": {"type": "subtraction_error", "description": "Subtracted incorrectly before division."},
                "3": {"type": "inversion_slip", "description": "Added 5 instead of subtracting to get 25/3."}
            },
            "hints": [
                "Isolate the variable term '3x' by subtracting 5 from both sides.",
                "3x = 20 - 5 = 15.",
                "Divide both sides by 3 to get x = 5."
            ],
            "source": "NCERT Class 8-10 Foundation"
        },
        {
            "id": "q_math_quad_01",
            "concept_id": "concept_math_quad_roots",
            "tracks": ["JEE", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["9", "10", "11", "12"],
            "subject": "Math",
            "topic": "Quadratic Equations",
            "difficulty": 0.40,
            "type": "multiple_choice",
            "question": "What are the roots of the quadratic equation x^2 - 5x + 6 = 0?",
            "options": ["x = 2, 3", "x = -2, -3", "x = 1, 6", "x = -1, -6"],
            "correct_index": 0,
            "explanation": "Factor the equation: (x - 2)(x - 3) = 0. Setting each factor to zero gives x = 2 and x = 3.",
            "misconception_distractors": {
                "1": {"type": "sign_error", "description": "Confused the factors (x-2)(x-3) with roots (-2, -3) forgetting to reverse signs."},
                "2": {"type": "factoring_fallacy", "description": "Picked factors of 6 that add to 7 instead of 5."},
                "3": {"type": "double_sign_error", "description": "Sign confusion in both constant and linear coefficients."}
            },
            "hints": [
                "Find two numbers that multiply to give +6 and add up to give -5.",
                "The numbers are -2 and -3 because (-2)*(-3)=6 and (-2)+(-3)=-5.",
                "(x - 2)(x - 3) = 0, so x = 2 or x = 3."
            ],
            "source": "NCERT Class 10 & JEE Foundation"
        },

        # --- Physics ---
        {
            "id": "q_phys_kinematics_01",
            "concept_id": "concept_phys_speed_dist",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["9", "10", "11", "12", "Degree"],
            "subject": "Physics",
            "topic": "Kinematics",
            "difficulty": 0.30,
            "type": "multiple_choice",
            "question": "A particle moves with uniform acceleration a = 4 m/s^2 from rest (u = 0). What is its velocity after 5 seconds?",
            "options": ["20 m/s", "10 m/s", "40 m/s", "25 m/s"],
            "correct_index": 0,
            "explanation": "Using the first kinematic equation v = u + at: v = 0 + (4 m/s^2)(5 s) = 20 m/s.",
            "misconception_distractors": {
                "1": {"type": "formula_confusion", "description": "Divided acceleration by time or confused with average velocity."},
                "2": {"type": "squared_time_slip", "description": "Confused velocity formula with displacement (multiplied by extra factor)."},
                "3": {"type": "calculation_error", "description": "Substituted wrong numbers into relation."}
            },
            "hints": [
                "Use the kinematic equation relating initial velocity, acceleration, and time: v = u + at.",
                "Here, initial velocity u = 0, a = 4 m/s^2, and t = 5 s.",
                "v = 0 + 4 * 5 = 20 m/s."
            ],
            "source": "NCERT Class 9 & 11 Mechanics"
        },
        {
            "id": "q_phys_gravitation_01",
            "concept_id": "concept_phys_gravitation",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["9", "10", "11", "12"],
            "subject": "Physics",
            "topic": "Gravitation",
            "difficulty": 0.50,
            "type": "multiple_choice",
            "question": "If the distance between two point masses is doubled, the gravitational attraction between them becomes:",
            "options": ["One-fourth (1/4)", "One-half (1/2)", "Double (2x)", "Four times (4x)"],
            "correct_index": 0,
            "explanation": "Newton's law of gravitation states F = G*m1*m2 / r^2. Since F is inversely proportional to r^2, doubling r multiplies F by 1/(2^2) = 1/4.",
            "misconception_distractors": {
                "1": {"type": "inverse_linear_fallacy", "description": "Assumed inverse linear relationship F ~ 1/r instead of inverse square law."},
                "2": {"type": "direct_proportion_error", "description": "Assumed force increases with distance."},
                "3": {"type": "inverse_square_direction_error", "description": "Squared the factor but applied it in direct proportion."}
            },
            "hints": [
                "Recall Newton's Law of Universal Gravitation: F = G * (m1 * m2) / r^2.",
                "The force depends inversely on the SQUARE of the distance r.",
                "If r becomes 2r, the denominator becomes (2r)^2 = 4r^2, so the force is reduced to 1/4."
            ],
            "source": "NCERT Class 9 & 11 Gravitation"
        },
        {
            "id": "q_phys_forces_01",
            "concept_id": "concept_phys_force_units",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["8", "9", "10", "11", "12"],
            "subject": "Physics",
            "topic": "Laws of Motion",
            "difficulty": 0.25,
            "type": "multiple_choice",
            "question": "What is the SI unit of force?",
            "options": ["Newton (N)", "Joule (J)", "Pascal (Pa)", "Watt (W)"],
            "correct_index": 0,
            "explanation": "Force is measured in Newtons (N) in the SI system, where 1 N = 1 kg*m/s^2.",
            "misconception_distractors": {
                "1": {"type": "unit_confusion_energy", "description": "Confused force with work/energy (Joule)."},
                "2": {"type": "unit_confusion_pressure", "description": "Confused force with pressure (Pascal)."},
                "3": {"type": "unit_confusion_power", "description": "Confused force with power (Watt)."}
            },
            "hints": [
                "Force = mass * acceleration (kg * m/s^2).",
                "Named in honor of Sir Isaac Newton.",
                "Joule is energy, Pascal is pressure, Watt is power."
            ],
            "source": "NCERT Standard Physics"
        },

        # --- Chemistry ---
        {
            "id": "q_chem_organic_01",
            "concept_id": "concept_chem_iupac",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"],
            "class_levels": ["10", "11", "12", "Degree"],
            "subject": "Chemistry",
            "topic": "Organic Chemistry",
            "difficulty": 0.35,
            "type": "multiple_choice",
            "question": "What is the correct IUPAC name for CH3-CH2-CH2-OH?",
            "options": ["Propan-1-ol", "Ethanol", "Propan-2-ol", "Butanol"],
            "correct_index": 0,
            "explanation": "The 3-carbon parent chain is propane. The -OH group is at position 1, giving Propan-1-ol.",
            "misconception_distractors": {
                "1": {"type": "carbon_count_slip", "description": "Counted 2 carbons instead of 3."},
                "2": {"type": "positional_isomer_error", "description": "Assigned -OH to central carbon (position 2)."},
                "3": {"type": "carbon_count_overestimation", "description": "Counted 4 carbons."}
            },
            "hints": [
                "Count the number of carbons in the continuous chain: CH3-CH2-CH2- has 3 carbons (root 'prop-').",
                "The -OH functional group gives suffix '-ol'.",
                "The functional group is on the first carbon, making it propan-1-ol."
            ],
            "source": "NCERT Class 10 & 11 Organic Chemistry"
        },
        {
            "id": "q_chem_bonding_01",
            "concept_id": "concept_chem_reaction_mechanisms",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "CET"],
            "class_levels": ["10", "11", "12"],
            "subject": "Chemistry",
            "topic": "Chemical Bonding",
            "difficulty": 0.40,
            "type": "multiple_choice",
            "question": "In a water molecule (H2O), what is the approximate H-O-H bond angle due to lone pair repulsion?",
            "options": ["104.5°", "109.5°", "120°", "180°"],
            "correct_index": 0,
            "explanation": "H2O has sp3 hybridization with 2 bonding pairs and 2 lone pairs. Lone pair-lone pair repulsion compresses the tetrahedral 109.5° angle down to ~104.5°.",
            "misconception_distractors": {
                "1": {"type": "ideal_geometry_fallacy", "description": "Assumed ideal tetrahedral angle without considering lone pair repulsion."},
                "2": {"type": "trigonal_planar_confusion", "description": "Confused sp3 bent with sp2 trigonal planar."},
                "3": {"type": "linear_geometry_error", "description": "Assumed linear structure like CO2."}
            },
            "hints": [
                "Oxygen in water has 2 bonding pairs with Hydrogen and 2 lone pairs.",
                "According to VSEPR theory, lone pair-lone pair repulsion is stronger than bond pair repulsion.",
                "This compresses the ideal tetrahedral angle (109.5°) to about 104.5°."
            ],
            "source": "NCERT Class 11 Chemical Bonding"
        },
        {
            "id": "q_chem_aromatic_01",
            "concept_id": "concept_chem_aromatic",
            "tracks": ["JEE", "NEET", "CUET", "CBSE", "ICSE", "CET"],
            "class_levels": ["11", "12", "Degree"],
            "subject": "Chemistry",
            "topic": "Hydrocarbons",
            "difficulty": 0.35,
            "type": "multiple_choice",
            "question": "According to Huckel's rule, a cyclic planar conjugated system is aromatic if it contains how many pi electrons?",
            "options": ["(4n + 2)", "4n", "(2n + 4)", "2n"],
            "correct_index": 0,
            "explanation": "Huckel's rule states that cyclic, planar, completely conjugated systems with (4n + 2) pi electrons (where n is an integer 0, 1, 2...) possess aromatic stability.",
            "misconception_distractors": {
                "1": {"type": "antiaromatic_confusion", "description": "Confused aromatic (4n+2) with antiaromatic (4n)."},
                "2": {"type": "formula_swap", "description": "Inverted coefficients in the formula."},
                "3": {"type": "procedural_error", "description": "Assumed any even number of pi electrons."}
            },
            "hints": [
                "Recall Huckel's rule for aromaticity: for n=1, the number of pi electrons is 4(1)+2 = 6 (like Benzene).",
                "Systems with 4n pi electrons are antiaromatic.",
                "The rule is (4n + 2) pi electrons."
            ],
            "source": "NCERT Class 11 Hydrocarbons"
        },

        # --- Biology (NEET, CUET, CBSE) ---
        {
            "id": "q_bio_cell_01",
            "concept_id": "concept_bio_cell",
            "tracks": ["NEET", "CUET", "CBSE", "ICSE", "State Board"],
            "class_levels": ["8", "9", "10", "11", "12"],
            "subject": "Biology",
            "topic": "Cell Biology",
            "difficulty": 0.25,
            "type": "multiple_choice",
            "question": "Which organelle is recognized as the 'powerhouse of the cell' for synthesizing ATP?",
            "options": ["Mitochondria", "Ribosome", "Golgi Apparatus", "Lysosome"],
            "correct_index": 0,
            "explanation": "Mitochondria produce cellular ATP through oxidative phosphorylation and the Krebs cycle, functioning as the powerhouses of eukaryotic cells.",
            "misconception_distractors": {
                "1": {"type": "organelle_role_confusion", "description": "Confused energy production with protein synthesis (Ribosome)."},
                "2": {"type": "packaging_confusion", "description": "Confused with packaging and secretion (Golgi)."},
                "3": {"type": "digestive_confusion", "description": "Confused with digestive enzymes (Lysosome)."}
            },
            "hints": [
                "This double-membraned organelle is the site of cellular respiration.",
                "It produces Adenosine Triphosphate (ATP), the energy currency of the cell.",
                "Known universally as the powerhouse of the cell: Mitochondria."
            ],
            "source": "NCERT Class 9 & 11 Cell Biology"
        },
        {
            "id": "q_bio_genetics_01",
            "concept_id": "concept_bio_genetics",
            "tracks": ["NEET", "CUET", "CBSE", "ICSE", "State Board"],
            "class_levels": ["10", "12"],
            "subject": "Biology",
            "topic": "Genetics & Evolution",
            "difficulty": 0.45,
            "type": "multiple_choice",
            "question": "In a classical Mendelian monohybrid cross between heterozygous tall pea plants (Tt x Tt), what is the phenotypic ratio of Tall to Dwarf plants?",
            "options": ["3 : 1", "1 : 2 : 1", "9 : 3 : 3 : 1", "1 : 1"],
            "correct_index": 0,
            "explanation": "The offspring genotypes are 1 TT : 2 Tt : 1 tt. Both TT and Tt express the tall phenotype, resulting in a 3:1 phenotypic ratio (3 Tall : 1 Dwarf).",
            "misconception_distractors": {
                "1": {"type": "genotypic_phenotypic_confusion", "description": "Provided the genotypic ratio (1:2:1) instead of the observable phenotypic ratio."},
                "2": {"type": "dihybrid_confusion", "description": "Confused monohybrid cross with dihybrid F2 ratio (9:3:3:1)."},
                "3": {"type": "test_cross_slip", "description": "Confused with monohybrid test cross (1:1)."}
            },
            "hints": [
                "Phenotype refers to the physical observable traits (Tall vs Dwarf).",
                "Punnett square yields: TT (Tall), Tt (Tall), Tt (Tall), tt (Dwarf).",
                "3 plants are Tall and 1 is Dwarf, giving a 3:1 phenotypic ratio."
            ],
            "source": "NCERT Class 10 & 12 Principles of Inheritance"
        },
        {
            "id": "q_bio_physiology_01",
            "concept_id": "concept_bio_cardio",
            "tracks": ["NEET", "CUET", "CBSE", "ICSE", "State Board"],
            "class_levels": ["10", "11", "12"],
            "subject": "Biology",
            "topic": "Human Physiology",
            "difficulty": 0.35,
            "type": "multiple_choice",
            "question": "Which chamber of the human heart pumps oxygenated blood into the systemic aorta to supply the entire body?",
            "options": ["Left Ventricle", "Right Ventricle", "Left Atrium", "Right Atrium"],
            "correct_index": 0,
            "explanation": "The Left Ventricle has the thickest muscular wall and pumps oxygenated blood through the aortic valve into the systemic circulation.",
            "misconception_distractors": {
                "1": {"type": "pulmonary_systemic_confusion", "description": "Right ventricle pumps deoxygenated blood to the lungs via pulmonary artery."},
                "2": {"type": "atrium_ventricle_confusion", "description": "Left atrium receives blood from pulmonary veins, does not pump to aorta."},
                "3": {"type": "complete_inversion", "description": "Right atrium receives deoxygenated blood from vena cava."}
            },
            "hints": [
                "Oxygenated blood returns from lungs to the left side of the heart.",
                "Ventricles pump blood OUT of the heart, while atria receive blood.",
                "The left ventricle pumps blood into the aorta with high pressure."
            ],
            "source": "NCERT Class 10 & 11 Body Fluids & Circulation"
        },

        # --- Undergraduate / GATE / Placement Computer Science & Mathematics ---
        {
            "id": "q_cs_dsa_01",
            "concept_id": "concept_cs_bst",
            "tracks": ["GATE", "Software Engineering & Placements", "Undergraduate", "Data Science & AI"],
            "class_levels": ["Degree", "Undergraduate"],
            "subject": "Computer Science",
            "topic": "Data Structures & Algorithms",
            "difficulty": 0.35,
            "type": "multiple_choice",
            "question": "What is the worst-case time complexity of searching for a key in a balanced Binary Search Tree (such as an AVL or Red-Black Tree) with n nodes?",
            "options": ["O(log n)", "O(n)", "O(1)", "O(n log n)"],
            "correct_index": 0,
            "explanation": "In a balanced binary search tree, the height h is strictly bounded by O(log n). Each comparison eliminates half of the remaining subtrees, yielding O(log n) worst-case search complexity.",
            "misconception_distractors": {
                "1": {"type": "unbalanced_bst_confusion", "description": "O(n) occurs in a skewed/degenerate BST, but balanced BSTs guarantee O(log n)."},
                "2": {"type": "hash_table_confusion", "description": "O(1) average lookup is characteristic of Hash Maps, not tree traversals."},
                "3": {"type": "sorting_complexity_slip", "description": "O(n log n) is typical of comparison sorting, not single-item search."}
            },
            "hints": [
                "Consider the height of a balanced tree with n nodes.",
                "At each node, we branch either left or right, halving search space.",
                "Height h = ceil(log2(n+1)), so search is O(log n)."
            ],
            "source": "GATE Computer Science / CLRS Algorithms"
        },
        {
            "id": "q_cs_os_01",
            "concept_id": "concept_cs_deadlock",
            "tracks": ["GATE", "Software Engineering & Placements", "Undergraduate"],
            "class_levels": ["Degree", "Undergraduate"],
            "subject": "Operating Systems",
            "topic": "Process Synchronization",
            "difficulty": 0.45,
            "type": "multiple_choice",
            "question": "Which of the following is NOT one of Coffman's four necessary conditions for a system deadlock to occur?",
            "options": [
                "Preemptive resource allocation",
                "Mutual exclusion",
                "Hold and wait",
                "Circular wait"
            ],
            "correct_index": 0,
            "explanation": "The four Coffman conditions are: Mutual Exclusion, Hold and Wait, NO PREEMPTION (resources cannot be forcibly taken), and Circular Wait. Preemptive resource allocation actually PREVENTS deadlock.",
            "misconception_distractors": {
                "1": {"type": "coffman_condition_inversion", "description": "Mutual exclusion is a valid necessary condition."},
                "2": {"type": "coffman_condition_inversion", "description": "Hold and wait is a valid necessary condition."},
                "3": {"type": "coffman_condition_inversion", "description": "Circular wait is a valid necessary condition."}
            },
            "hints": [
                "Deadlocks occur when resources cannot be forcibly reclaimed from a process.",
                "The actual condition is 'No Preemption'.",
                "Therefore, 'Preemptive resource allocation' is NOT a condition for deadlock."
            ],
            "source": "GATE Computer Science / Silberschatz OS"
        },
        {
            "id": "q_math_lin_alg_01",
            "concept_id": "concept_math_eigenvalues",
            "tracks": ["GATE", "Data Science & AI", "Undergraduate", "Software Engineering & Placements"],
            "class_levels": ["Degree", "Undergraduate"],
            "subject": "Engineering Mathematics",
            "topic": "Linear Algebra",
            "difficulty": 0.40,
            "type": "multiple_choice",
            "question": "For any square matrix A, the sum of all its eigenvalues is always mathematically equal to:",
            "options": ["The Trace of matrix A (sum of main diagonal elements)", "The Determinant of matrix A", "The Rank of matrix A", "The Spectral Radius"],
            "correct_index": 0,
            "explanation": "A fundamental theorem of Linear Algebra: Trace(A) = sum of eigenvalues, and Det(A) = product of eigenvalues.",
            "misconception_distractors": {
                "1": {"type": "product_sum_confusion", "description": "The product of eigenvalues equals the determinant, while the sum equals the trace."},
                "2": {"type": "rank_nullity_slip", "description": "Rank equals the number of non-zero eigenvalues for symmetric matrices, not the sum."},
                "3": {"type": "extremum_confusion", "description": "Spectral radius is the maximum absolute eigenvalue."}
            },
            "hints": [
                "Recall the relationship between the characteristic polynomial coefficients and eigenvalues.",
                "Trace(A) = a11 + a22 + ... + ann = sum(lambda_i).",
                "Determinant(A) = product(lambda_i)."
            ],
            "source": "GATE Engineering Mathematics / Gilbert Strang"
        }
    ]

    @classmethod
    def resolve_goal_key(cls, goal: str, klass: str = "10") -> str:
        g = (goal or "").strip()
        gl = g.lower()
        if g in cls.SYLLABUS_REGISTRY:
            return g
        if "gate" in gl:
            return "GATE"
        if any(k in gl for k in ["software", "placement", "dsa", "coding", "full stack"]):
            return "Software Engineering & Placements"
        if any(k in gl for k in ["data science", "ai", "machine learning", "ml", "analytics"]):
            return "Data Science & AI"
        if any(k in gl for k in ["cat", "mba", "management"]):
            return "CAT"
        if any(k in gl for k in ["degree", "undergrad", "college", "btech", "b.tech", "bsc", "b.sc", "be", "b.e."]) or klass in ["Degree", "Undergraduate"]:
            return "Undergraduate"
        if any(k in gl for k in ["jee", "engineering", "iit"]):
            return "JEE"
        if any(k in gl for k in ["neet", "medical", "mbbs"]):
            return "NEET"
        if any(k in gl for k in ["cet", "mht"]):
            return "CET"
        if any(k in gl for k in ["cuet", "university"]):
            return "CUET"
        if any(k in gl for k in ["icse", "isc"]):
            return "ICSE"
        if "state" in gl:
            return "State Board"
        if any(k in gl for k in ["10th", "tenth", "board", "cbse", "school"]):
            return "CBSE"
        return "Undergraduate" if klass in ["Degree", "Undergraduate"] else "CBSE"

    @classmethod
    def get_syllabus_for_student(cls, goal: str, klass: str) -> Dict[str, Any]:
        """Retrieves official syllabus track for student's aim and grade level."""
        goal_key = cls.resolve_goal_key(goal, klass)
        raw_syllabus = cls.SYLLABUS_REGISTRY.get(goal_key, cls.SYLLABUS_REGISTRY["CBSE"])
        
        return {
            "track": goal if goal else goal_key,
            "track_key": goal_key,
            "name": f"{goal} Personalized Track" if goal not in cls.SYLLABUS_REGISTRY else raw_syllabus["name"],
            "class_level": klass,
            "subjects": raw_syllabus["subjects"],
            "description": raw_syllabus["description"],
            "topics": raw_syllabus["topics"]
        }

    @classmethod
    def get_questions_for_student(cls, goal: str, klass: str, weak_areas: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Dynamically filters and prioritizes question items tailored strictly
        to the student's exam prep aim, grade level, and diagnostic weak areas.
        """
        target_goal = cls.resolve_goal_key(goal, klass)
        student_class = str(klass).strip() if klass else "10"
        weak_set = {w.lower().strip() for w in (weak_areas or [])}

        eligible = []
        for q in cls.CURRICULUM_QUESTION_BANK:
            # 1. Goal track match
            if target_goal not in q["tracks"] and "All" not in q["tracks"]:
                continue
            
            # 2. Class level match
            if student_class not in q["class_levels"]:
                # If exact class isn't listed, check if it's within secondary / senior range
                is_senior = student_class in ["11", "12", "Degree", "Undergraduate"]
                q_is_senior = any(c in ["11", "12", "Degree", "Undergraduate"] for c in q["class_levels"])
                if is_senior != q_is_senior:
                    continue

            eligible.append(q)

        # Fallback if specific grade subset is narrow: include general track items
        if len(eligible) < 5:
            for q in cls.CURRICULUM_QUESTION_BANK:
                if target_goal in q["tracks"] and q not in eligible:
                    eligible.append(q)

        # Sort with preference for student's known weak areas
        def sort_priority(q: Dict[str, Any]) -> int:
            q_subject = q.get("subject", "").lower()
            q_topic = q.get("topic", "").lower()
            q_concept = q.get("concept_id", "").lower()
            
            for w in weak_set:
                if w in q_subject or w in q_topic or w in q_concept:
                    return -1  # High priority
            return 0

        eligible.sort(key=sort_priority)
        return eligible

    @classmethod
    def generate_courses_for_student(cls, goal: str, klass: str, weak_areas: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Dynamically builds genuine, accredited curriculum courses aligned
        with the student's exam prep aim, grade level, and learning gaps.
        Includes embedded video lectures, comprehensive conceptual notes,
        formula sheets with variable definitions, worked examples, pitfalls,
        and official study materials.
        """
        target_goal = cls.resolve_goal_key(goal, klass)
        student_class = str(klass).strip() if klass else "10"
        weak_set = {w.lower().strip() for w in (weak_areas or [])}
        is_senior = student_class in ["11", "12"]
        is_undergrad = student_class in ["Degree", "Undergraduate"] or target_goal in ["GATE", "Software Engineering & Placements", "Data Science & AI", "Undergraduate", "CAT"]

        courses = []
        track_slug = target_goal.lower().replace(" ", "_")

        # =========================================================================
        # 0. Undergraduate / GATE / Placement / Career Engineering Track
        # =========================================================================
        if is_undergrad:
            courses.append({
                "id": f"c_{track_slug}_dsa",
                "track": target_goal,
                "title": f"{target_goal}: Data Structures & Algorithms Masterclass",
                "tag": "Computer Science",
                "hours": 12,
                "min_class": 12,
                "is_weakness_remedy": any(any(k in w for k in ["dsa", "algo", "tree", "graph", "dp", "sorting"]) for w in weak_set),
                "concept_id": "concept_cs_bst",
                "description": f"Masterclass covering asymptotic analysis, array techniques, linked structures, binary search trees, graph algorithms (BFS/DFS/Dijkstra), and dynamic programming for {target_goal}.",
                "modules": [
                    {
                        "id": f"mod_{track_slug}_dsa_1",
                        "title": "Module 1: Asymptotic Analysis & Binary Search Trees",
                        "duration": "2.0 hrs",
                        "concept_id": "concept_cs_bst",
                        "video_url": "https://www.youtube.com/embed/9Jry5-82I68",
                        "video_title": "MIT 6.006: Introduction to Algorithms & BST Operations",
                        "summary": "Big-O, Omega, and Theta notations; BST property, in-order predecessor/successor, and balanced search trees.",
                        "detailed_notes": [
                            "1. Asymptotic Hierarchy: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n). Big-O provides an asymptotic upper bound.",
                            "2. Binary Search Tree Invariant: For every node X, all keys in the left subtree are strictly less than key(X), and all keys in the right subtree are strictly greater than key(X).",
                            "3. Self-Balancing Trees: AVL and Red-Black trees maintain O(log n) height via tree rotations upon insertion/deletion."
                        ],
                        "formula_note": "BST Height: h = O(log n) for balanced trees; h = O(n) worst case for skewed trees.",
                        "formula_sheet": [
                            {
                                "name": "Master Theorem for Divide & Conquer",
                                "formula": "T(n) = a*T(n/b) + f(n)",
                                "variables": "a >= 1 (subproblems), b > 1 (division factor), f(n) = cost of combine",
                                "notes": "If f(n) = O(n^(log_b(a) - epsilon)), T(n) = Theta(n^(log_b(a)))."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Find the in-order traversal of a BST with root 10, left child 5, and right child 15.",
                                "solution_steps": [
                                    "Step 1: Traverse left subtree: 5.",
                                    "Step 2: Visit current root: 10.",
                                    "Step 3: Traverse right subtree: 15.",
                                    "Step 4: Result: 5, 10, 15 (always sorted in ascending order)."
                                ],
                                "key_insight": "In-order traversal of any valid Binary Search Tree always produces elements in strictly ascending sorted order."
                            }
                        ],
                        "pitfalls": ["Assuming search in an arbitrary binary tree is O(log n) without the BST ordering property."],
                        "study_materials": [
                            {
                                "title": "MIT OCW 6.006 Algorithms Lecture Notes",
                                "type": "University Lecture Notes",
                                "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/"
                            }
                        ],
                        "practice_question": {
                            "q": "What is the worst-case time complexity of searching in a balanced AVL tree with n elements?",
                            "options": ["O(log n)", "O(n)", "O(1)", "O(n^2)"],
                            "answer_index": 0,
                            "explanation": "AVL trees guarantee balanced height h <= 1.44 log2(n), yielding O(log n) lookup."
                        }
                    }
                ]
            })
            courses.append({
                "id": f"c_{track_slug}_os",
                "track": target_goal,
                "title": f"{target_goal}: Operating Systems & Concurrency Architecture",
                "tag": "Operating Systems",
                "hours": 10,
                "min_class": 12,
                "is_weakness_remedy": any(any(k in w for k in ["os", "operating", "deadlock", "memory", "thread", "process"]) for w in weak_set),
                "concept_id": "concept_cs_deadlock",
                "description": f"Deep dive into process lifecycle, multi-threading, CPU scheduling algorithms, virtual memory paging, and deadlock avoidance for {target_goal}.",
                "modules": [
                    {
                        "id": f"mod_{track_slug}_os_1",
                        "title": "Module 1: Concurrency, Synchronization & Deadlocks",
                        "duration": "1.8 hrs",
                        "concept_id": "concept_cs_deadlock",
                        "video_url": "https://www.youtube.com/embed/UeXh9gZJt8M",
                        "video_title": "Operating Systems: Process Synchronization & Deadlock Handling",
                        "summary": "Critical section problem, mutex locks, semaphores, and Coffman conditions for deadlocks.",
                        "detailed_notes": [
                            "1. Critical Section Requirements: Mutual Exclusion (only one process in CS), Progress (selection cannot be postponed indefinitely), Bounded Waiting (limit on times other processes enter CS).",
                            "2. Deadlock Coffman Conditions: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait. All 4 must hold simultaneously.",
                            "3. Banker's Algorithm: Resource allocation and safety algorithm that tests for safe states before allocating resources."
                        ],
                        "formula_note": "Need Matrix = Max Demand - Allocation in Banker's Algorithm.",
                        "formula_sheet": [
                            {
                                "name": "Banker's Algorithm Safety Condition",
                                "formula": "Need[i][j] = Max[i][j] - Allocation[i][j]",
                                "variables": "Max = max resource demand, Allocation = current resources assigned",
                                "notes": "A state is safe if there exists a safe sequence <P1, P2, ... Pn> where each process can finish."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "If a system has 3 processes each requiring 2 units of resource R, what is the minimum number of units of R to guarantee no deadlock?",
                                "solution_steps": [
                                    "Step 1: In worst-case allocation, each process holds 1 unit: 3 * 1 = 3 units.",
                                    "Step 2: Add 1 extra unit so at least one process gets 2 units and finishes.",
                                    "Step 3: Minimum units = 3 + 1 = 4 units."
                                ],
                                "key_insight": "Formula for deadlock-free resources: Total Resources >= sum(Max_i - 1) + 1."
                            }
                        ],
                        "pitfalls": ["Confusing Deadlock (permanent standstill) with Starvation (indefinite delay due to low priority)."],
                        "study_materials": [
                            {
                                "title": "Silberschatz Operating System Concepts (Wiley)",
                                "type": "Reference Textbook",
                                "url": "https://os-book.com/"
                            }
                        ],
                        "practice_question": {
                            "q": "Which condition prevents deadlock by forcing resources to be forcibly released?",
                            "options": ["Preemption allowed", "Mutual exclusion", "Hold and wait", "Circular wait"],
                            "answer_index": 0,
                            "explanation": "Allowing resource preemption invalidates the 'No Preemption' necessary condition, preventing deadlock."
                        }
                    }
                ]
            })
            courses.append({
                "id": f"c_{track_slug}_math",
                "track": target_goal,
                "title": f"{target_goal}: Advanced Mathematics & Quantitative Analysis",
                "tag": "Mathematics",
                "hours": 10,
                "min_class": 12,
                "is_weakness_remedy": any(any(k in w for k in ["math", "linear", "algebra", "eigen", "matrix", "probability"]) for w in weak_set),
                "concept_id": "concept_math_eigenvalues",
                "description": f"Linear algebra, matrix factorizations, probability distributions, and discrete optimization for {target_goal}.",
                "modules": [
                    {
                        "id": f"mod_{track_slug}_math_1",
                        "title": "Module 1: Linear Algebra, Eigenvalues & Matrix Factorizations",
                        "duration": "1.5 hrs",
                        "concept_id": "concept_math_eigenvalues",
                        "video_url": "https://www.youtube.com/embed/PFDu9oVAE-g",
                        "video_title": "MIT 18.06: Eigenvalues and Eigenvectors by Gilbert Strang",
                        "summary": "Characteristic equation det(A - lambda*I) = 0, trace-eigenvalue relation, and diagonalization.",
                        "detailed_notes": [
                            "1. Eigenvalue Equation: A*x = lambda*x where x is a non-zero eigenvector and lambda is the scalar eigenvalue.",
                            "2. Characteristic Polynomial: Solved via det(A - lambda*I) = 0.",
                            "3. Fundamental Properties: Trace(A) = sum(lambda_i), Det(A) = product(lambda_i)."
                        ],
                        "formula_note": "Trace(A) = sum of diagonal elements = sum of eigenvalues.",
                        "formula_sheet": [
                            {
                                "name": "Characteristic Equation",
                                "formula": "det(A - λI) = 0",
                                "variables": "A = n×n matrix, λ = eigenvalue, I = identity matrix",
                                "notes": "Roots of this polynomial are the eigenvalues of A."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Find the sum of eigenvalues of matrix A = [[2, 4], [1, 5]].",
                                "solution_steps": [
                                    "Step 1: Trace(A) is the sum of main diagonal elements: 2 + 5 = 7.",
                                    "Step 2: By theorem, sum of eigenvalues equals Trace(A).",
                                    "Step 3: Sum = 7."
                                ],
                                "key_insight": "Never waste time computing individual roots if only the sum or product of eigenvalues is asked."
                            }
                        ],
                        "pitfalls": ["Assuming eigenvectors can be zero vectors; eigenvectors are by definition non-zero."],
                        "study_materials": [
                            {
                                "title": "MIT OCW 18.06 Linear Algebra Notes",
                                "type": "University Notes",
                                "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/"
                            }
                        ],
                        "practice_question": {
                            "q": "The product of all eigenvalues of matrix A is equal to:",
                            "options": ["Determinant of A", "Trace of A", "Rank of A", "Inverse of A"],
                            "answer_index": 0,
                            "explanation": "Det(A) is identically equal to the product of its eigenvalues."
                        }
                    }
                ]
            })
            return courses

        # =========================================================================
        # 1. Physics / Physical Science Course
        # =========================================================================
        is_phys_weak = any(any(k in w for k in ["phys", "mech", "kinematics", "motion", "gravity", "gravitation", "force", "optics", "thermo", "newton", "speed", "velocity"]) for w in weak_set)
        
        phys_title = (
            f"Class {student_class} {target_goal} Physics: Mechanics, Kinematics & Field Theory"
            if is_senior else
            f"Class {student_class} {target_goal} Science: Motion, Force & Universal Gravitation"
        )
        phys_desc = (
            f"Comprehensive masterclass on one-dimensional and planar kinematics, Newton's three laws, momentum conservation, and Newtonian gravitation tailored for {target_goal} aspirants."
            if is_senior else
            f"Core foundation in velocity, acceleration, balanced forces, and universal gravity aligned with Class {student_class} {target_goal} standards."
        )

        courses.append({
            "id": f"c_{track_slug}_phys",
            "track": target_goal,
            "title": phys_title,
            "tag": "Physics",
            "hours": 8,
            "min_class": int(student_class) if student_class.isdigit() else 10,
            "is_weakness_remedy": is_phys_weak,
            "concept_id": "concept_phys_speed_dist",
            "description": phys_desc,
            "modules": [
                {
                    "id": f"mod_{track_slug}_phys_1",
                    "title": "Module 1: Kinematics & Rectilinear Motion in One Dimension",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_phys_speed_dist",
                    "video_url": "https://www.youtube.com/embed/ZM8ECpBuQYE",
                    "video_title": "Khan Academy Physics: One-Dimensional Motion & Kinematic Equations",
                    "summary": "Velocity-time relationships, uniform acceleration kinematics (v = u + at, s = ut + 0.5at^2), and graphical interpretations.",
                    "detailed_notes": [
                        "1. Fundamentals of Rectilinear Motion: Motion along a straight line is described using displacement (vector distance from origin), instantaneous velocity v = dx/dt, and acceleration a = dv/dt = d^2x/dt^2. When acceleration is uniform (constant in both magnitude and direction), velocity changes linearly with time.",
                        "2. Derivation of the Three Kinematic Equations: Starting from a = dv/dt, integrating yields v(t) = u + at. Substituting v = dx/dt and integrating again produces displacement s(t) = ut + 0.5*a*t^2. Eliminating time t between the first two yields the third fundamental relation: v^2 = u^2 + 2as.",
                        "3. Graphical Analysis of Motion: In a position-time (x-t) graph, the slope at any point equals instantaneous velocity. In a velocity-time (v-t) graph, the slope represents instantaneous acceleration, while the area under the curve bounded by the time axis directly equals displacement.",
                        "4. Free Fall Under Gravity: In vertical projectile motion without air resistance, acceleration is constant downward with magnitude g ≈ 9.8 m/s^2 (or 10 m/s^2 for quick estimations). At maximum height, instantaneous vertical velocity v = 0."
                    ],
                    "formula_note": "Kinematic Equations: 1) v = u + at, 2) s = ut + (1/2)at^2, 3) v^2 = u^2 + 2as. Valid strictly under constant acceleration.",
                    "formula_sheet": [
                        {
                            "name": "First Equation of Motion",
                            "formula": "v = u + at",
                            "variables": "v = final velocity (m/s), u = initial velocity (m/s), a = uniform acceleration (m/s²), t = time interval (s)",
                            "notes": "Linear relation between velocity and elapsed time."
                        },
                        {
                            "name": "Second Equation of Motion (Displacement)",
                            "formula": "s = ut + (1/2)at²",
                            "variables": "s = displacement (m), u = initial velocity (m/s), a = acceleration (m/s²), t = time (s)",
                            "notes": "Parabolic position-time trajectory under non-zero uniform acceleration."
                        },
                        {
                            "name": "Third Equation of Motion (Time-Independent)",
                            "formula": "v² = u² + 2as",
                            "variables": "v = final velocity, u = initial velocity, a = acceleration, s = displacement",
                            "notes": "Crucial shortcut when time 't' is neither given nor required."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "A car accelerates uniformly from rest at 3.0 m/s² for 8.0 seconds. Calculate: (a) its final velocity, and (b) total distance traversed during this interval.",
                            "solution_steps": [
                                "Step 1: Identify given quantities: Initial velocity u = 0 m/s, acceleration a = 3.0 m/s², time t = 8.0 s.",
                                "Step 2: Calculate final velocity using v = u + at => v = 0 + (3.0)(8.0) = 24.0 m/s.",
                                "Step 3: Calculate distance using s = ut + 0.5at² => s = 0*(8) + 0.5*(3.0)*(8.0)² = 0.5 * 3.0 * 64 = 96.0 meters."
                            ],
                            "key_insight": "Notice that starting from rest eliminates the 'ut' term completely, simplifying distance to 0.5*a*t²."
                        }
                    ],
                    "pitfalls": [
                        "Do NOT confuse distance (scalar total path length) with displacement (vector net change in position). If a ball is thrown up and caught, its displacement is 0, but distance traveled is 2*h.",
                        "Never apply v = u + at if acceleration is variable (e.g. a(t) = 3t). For non-uniform acceleration, calculus integration must be used.",
                        "Always assign a consistent Cartesian sign convention (e.g. upward = +y, downward = -y, so g = -9.8 m/s²)."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Physics Class 11 Chapter 3: Motion in a Straight Line",
                            "type": "Official Textbook Reference",
                            "url": "https://ncert.nic.in/textbook.php"
                        },
                        {
                            "title": "Kinematics Formula & Graphical Interpretation Cheatsheet",
                            "type": "Revision Notes",
                            "url": "https://openstax.org/books/college-physics/pages/2-introduction-to-one-dimensional-kinematics"
                        }
                    ],
                    "practice_question": {
                        "q": "A vehicle starts from rest with acceleration a = 4 m/s^2. Its velocity after 5 seconds is:",
                        "options": ["20 m/s", "10 m/s", "40 m/s", "25 m/s"],
                        "answer_index": 0,
                        "explanation": "Using v = u + at with u = 0, a = 4, and t = 5: v = 0 + (4)(5) = 20 m/s."
                    }
                },
                {
                    "id": f"mod_{track_slug}_phys_2",
                    "title": "Module 2: Universal Gravitation & Inverse Square Laws",
                    "duration": "1.8 hrs",
                    "concept_id": "concept_phys_gravitation",
                    "video_url": "https://www.youtube.com/embed/TRAbTlh70rg",
                    "video_title": "Khan Academy Physics: Newton's Law of Universal Gravitation",
                    "summary": "Newtonian universal gravitation, gravitational fields, acceleration due to gravity (g = GM/R^2), and orbital mechanics.",
                    "detailed_notes": [
                        "1. Universal Law of Gravitation: Every point mass attracts every other point mass with a force directly proportional to the product of their masses and inversely proportional to the square of the distance between their centers: F = G*(m1*m2)/r^2.",
                        "2. Gravitational Constant: G is the universal gravitational constant, with an empirical value G ≈ 6.674 × 10^-11 N·m²/kg². Unlike local gravitational acceleration g, G is invariant across the entire universe.",
                        "3. Local Surface Gravity (g): For an object of mass m on the surface of a spherical planet of mass M and radius R: F = m*g = G*(M*m)/R^2 => g = G*M / R^2. On Earth's surface, g ≈ 9.81 m/s².",
                        "4. Orbital Velocity & Satellite Motion: For a satellite in circular orbit at altitude h above radius R: Centripetal force = Gravitational force => m*v²/r = G*M*m/r² => Orbital velocity v_orbit = sqrt(G*M / r)."
                    ],
                    "formula_note": "Gravitation: F = G*(m1*m2)/r^2. Doubling distance r quarters the attraction force (inverse-square law).",
                    "formula_sheet": [
                        {
                            "name": "Newton's Universal Gravitation",
                            "formula": "F = G * (m₁ * m₂) / r²",
                            "variables": "F = gravitational force (N), G = 6.674×10⁻¹¹ N·m²/kg², m₁, m₂ = masses (kg), r = center-to-center distance (m)",
                            "notes": "Always attractive, acts along the line connecting mass centers."
                        },
                        {
                            "name": "Surface Gravitational Acceleration",
                            "formula": "g = G * M / R²",
                            "variables": "g = local acceleration (m/s²), M = mass of planet (kg), R = radius of planet (m)",
                            "notes": "Independent of the falling body's own mass."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "If the distance between two celestial bodies is doubled while both masses remain unchanged, by what factor does the mutual gravitational attraction change?",
                            "solution_steps": [
                                "Step 1: Write initial force: F₁ = G * m₁ * m₂ / r₁².",
                                "Step 2: Express new distance: r₂ = 2 * r₁.",
                                "Step 3: Substitute new distance: F₂ = G * m₁ * m₂ / (2 * r₁)² = G * m₁ * m₂ / (4 * r₁²) = (1/4) * F₁."
                            ],
                            "key_insight": "Because r is squared in the denominator, scaling distance by factor k scales force by 1/k²."
                        }
                    ],
                    "pitfalls": [
                        "Never confuse 'G' (Universal Gravitational Constant, 6.674e-11) with 'g' (local acceleration due to gravity, 9.8 m/s²).",
                        "Remember that 'r' is measured from the center of mass to center of mass, NOT from the planetary surface. Altitude h must be added: r = R_planet + h."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Physics Class 11 Chapter 8: Gravitation",
                            "type": "Official Textbook Chapter",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "If distance between two celestial bodies is doubled, gravitational force becomes:",
                        "options": ["One-fourth (1/4)", "One-half (1/2)", "Double (2x)", "Four times (4x)"],
                        "answer_index": 0,
                        "explanation": "F is proportional to 1/r^2. (2r)^2 = 4r^2 in denominator, so F becomes 1/4."
                    }
                }
            ]
        })

        # =========================================================================
        # 2. Chemistry Course
        # =========================================================================
        is_chem_weak = any(any(k in w for k in ["chem", "organic", "inorganic", "bonding", "iupac", "reaction", "aromatic", "hydrocarbon", "vsepr", "acid", "mole"]) for w in weak_set)
        
        chem_title = (
            f"Class {student_class} {target_goal} Chemistry: Molecular Structure & Organic Reaction Mechanisms"
            if is_senior else
            f"Class {student_class} {target_goal} Science: Chemical Reactions, Acids & Carbon Compounds"
        )
        chem_desc = (
            f"Systematic IUPAC nomenclature, aromaticity with Huckel's rule, electronic effects (inductive, resonance, hyperconjugation), and reaction mechanisms for {target_goal}."
            if is_senior else
            f"Mastery of chemical equations, molecular valence, naming binary compounds, and acid-base neutralization for Class {student_class}."
        )

        courses.append({
            "id": f"c_{track_slug}_chem",
            "track": target_goal,
            "title": chem_title,
            "tag": "Chemistry",
            "hours": 7,
            "min_class": int(student_class) if student_class.isdigit() else 10,
            "is_weakness_remedy": is_chem_weak,
            "concept_id": "concept_chem_iupac",
            "description": chem_desc,
            "modules": [
                {
                    "id": f"mod_{track_slug}_chem_1",
                    "title": "Module 1: IUPAC Nomenclature of Functional Organic Chains",
                    "duration": "1.4 hrs",
                    "concept_id": "concept_chem_iupac",
                    "video_url": "https://www.youtube.com/embed/cExhtwVT1v0",
                    "video_title": "Khan Academy Organic Chemistry: IUPAC Nomenclature of Functional Carbon Compounds",
                    "summary": "Naming rules, continuous carbon chains, numbering priorities for alcohols (-ol), halides, and carbonyl groups.",
                    "detailed_notes": [
                        "1. IUPAC Structural Framework: Systematic organic naming uses three components: Prefix (substituents and branches) + Root Word (length of principal carbon chain: meth-, eth-, prop-, but-, pent-, etc.) + Primary Suffix (saturation: -ane, -ene, -yne) + Secondary Suffix (principal functional group).",
                        "2. Longest Continuous Carbon Chain Rule: Identify the longest carbon sequence that contains the maximum number of principal functional groups and multiple bonds, even if it is not drawn in a horizontal straight line.",
                        "3. Lowest Locant Rule & Principal Group Priority: Number the parent chain from the terminus that assigns lowest possible numbers (locants) to: (1) Principal Functional Group > (2) Multiple Bonds (Double/Triple) > (3) Substituents/Alkyl branches.",
                        "4. Official Priority Hierarchy: Carboxylic Acid (-COOH) > Sulfonic Acid (-SO3H) > Ester (-COOR) > Acid Halide (-COX) > Amide (-CONH2) > Nitrile (-CN) > Aldehyde (-CHO) > Ketone (-CO-) > Alcohol (-OH) > Amine (-NH2) > Halogens (-F, -Cl, -Br, -I) / Nitro (-NO2)."
                    ],
                    "formula_note": "IUPAC Suffix Rules: Principal group priority determines lowest numbering on parent carbon chain.",
                    "formula_sheet": [
                        {
                            "name": "Functional Group Priority Sequence",
                            "formula": "-COOH > -SO₃H > -COOR > -CONH₂ > -CN > -CHO > -CO- > -OH > -NH₂",
                            "variables": "Determines which group receives the suffix vs which becomes a substituent prefix.",
                            "notes": "When -OH is subordinate to -COOH or -CHO, it takes prefix 'hydroxy-' instead of suffix '-ol'."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "Determine the systematic IUPAC name for CH3-CH(OH)-CH2-CH3.",
                            "solution_steps": [
                                "Step 1: Longest continuous carbon chain has 4 carbons => Root word is 'butan-'.",
                                "Step 2: Functional group is alcohol (-OH), taking secondary suffix '-ol'.",
                                "Step 3: Number from left to right to give -OH the lowest locant: C1 is CH3, C2 has -OH. (Right-to-left would give C3, which violates lowest locant rule).",
                                "Step 4: Combine: Butan-2-ol (or 2-butanol)."
                            ],
                            "key_insight": "Always check numbering in both directions to verify the lowest locant on the principal functional group."
                        }
                    ],
                    "pitfalls": [
                        "Do not assume the longest chain is always horizontal; trace around bends and branching points.",
                        "If double and triple bonds are equidistant from opposite ends, the double bond (-ene) takes lower number precedence."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Chemistry Class 11 Chapter 12: Organic Chemistry Principles & Techniques",
                            "type": "Official NCERT Chapter",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "What is the systematic IUPAC name for CH3-CH2-CH2-OH?",
                        "options": ["Propan-1-ol", "Ethanol", "Propan-2-ol", "Butanol"],
                        "answer_index": 0,
                        "explanation": "The 3-carbon parent chain is propane with -OH on carbon 1, yielding Propan-1-ol."
                    }
                },
                {
                    "id": f"mod_{track_slug}_chem_2",
                    "title": "Module 2: Aromatic Systems & Huckel's (4n+2) Criteria",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_chem_aromatic",
                    "video_url": "https://www.youtube.com/embed/oDigu9YxXUg",
                    "video_title": "Khan Academy Organic Chemistry: Aromaticity, Benzene & Hückel's (4n+2) Rule",
                    "summary": "Conditions for aromatic stability: cyclic, planar, completely conjugated ring with (4n + 2) pi electrons.",
                    "detailed_notes": [
                        "1. Four Mandatory Criteria for Aromaticity: To be classified as aromatic, a molecular system must satisfy: (a) It must be cyclic, (b) Every atom in the ring must possess an unhybridized p-orbital (completely conjugated, sp2 or sp hybridized), (c) The ring must be geometrically planar (flat), and (d) It must contain (4n + 2) delocalized pi electrons, where n is a non-negative integer (0, 1, 2, 3...).",
                        "2. Huckel's Rule vs Anti-Aromaticity: Systems that are cyclic, planar, and conjugated with 4n pi electrons (n = 1, 2, 3... -> 4, 8, 12 pi electrons) are anti-aromatic and exceptionally unstable.",
                        "3. Resonance Energy & Stability: Benzene (6 pi electrons, n = 1) exhibits approximately 150 kJ/mol (36 kcal/mol) of resonance stabilization energy, explaining why it prefers electrophilic substitution over addition."
                    ],
                    "formula_note": "Huckel's Rule: (4n + 2) pi electrons = aromatic. 4n pi electrons = antiaromatic.",
                    "formula_sheet": [
                        {
                            "name": "Huckel's Electron Count Formula",
                            "formula": "Pi Electrons = 4n + 2 (where n = 0, 1, 2, 3...)",
                            "variables": "n = 0: 2 pi e⁻, n = 1: 6 pi e⁻ (Benzene, Pyridine), n = 2: 10 pi e⁻ (Naphthalene), n = 3: 14 pi e⁻ (Anthracene)",
                            "notes": "Applies strictly to monocyclic or planar polycyclic conjugated systems."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "Evaluate whether Cyclopentadienyl anion (C5H5⁻) is aromatic, anti-aromatic, or non-aromatic.",
                            "solution_steps": [
                                "Step 1: Check ring structure: It is a 5-membered cyclic ring.",
                                "Step 2: Check conjugation: The four carbon atoms with double bonds are sp2. The carbanion carbon with lone pair is also sp2 hybridized to allow overlap.",
                                "Step 3: Count pi electrons: 2 double bonds contribute 4 pi electrons; the carbanion lone pair contributes 2 pi electrons => Total = 6 pi electrons.",
                                "Step 4: Check Huckel's formula: 4n + 2 = 6 => 4n = 4 => n = 1 (integer). It is completely planar and aromatic."
                            ],
                            "key_insight": "A lone pair on a carbanion or heteroatom (like N or O) will hybridize to sp2 if doing so enables a (4n+2) aromatic system."
                        }
                    ],
                    "pitfalls": [
                        "Do not forget to verify planarity. Cyclooctatetraene (8 pi electrons) adopts a non-planar 'tub' shape to escape anti-aromaticity, making it non-aromatic rather than anti-aromatic.",
                        "Count each double bond as 2 pi electrons; count localized lone pairs as 0 pi electrons if they reside in sp2 hybrid orbitals in the ring plane."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Chemistry Class 11 Chapter 13: Hydrocarbons & Aromatic Chemistry",
                            "type": "Official Textbook Chapter",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "Which rule defines the electron count for aromatic stability?",
                        "options": ["(4n + 2) pi electrons", "4n pi electrons", "(2n + 1) pi electrons", "2n pi electrons"],
                        "answer_index": 0,
                        "explanation": "Huckel's (4n+2) pi-electron rule distinguishes aromatic stabilization."
                    }
                }
            ]
        })

        # =========================================================================
        # 3. Biology Course (If NEET, CUET Bio, or CBSE/ICSE/State Board)
        # =========================================================================
        if target_goal in ["NEET", "CUET", "CBSE", "ICSE", "State Board"]:
            is_bio_weak = any(any(k in w for k in ["bio", "cell", "genet", "physio", "cardio", "plant", "organ", "reproduction", "dna", "ecology"]) for w in weak_set)
            
            bio_title = (
                f"Class {student_class} {target_goal} Biology: Cell Architecture & Molecular Genetics"
                if is_senior else
                f"Class {student_class} {target_goal} Science: Cell Structure, Tissues & Life Processes"
            )
            bio_desc = (
                f"Comprehensive exploration of eukaryotic organelles, energy metabolism (mitochondria/ATP), and Mendelian inheritance patterns for {target_goal} aspirants."
                if is_senior else
                f"Core foundations of plant and animal cell structures, organelle functions, and basic cellular reproduction for Class {student_class}."
            )

            courses.append({
                "id": f"c_{track_slug}_bio",
                "track": target_goal,
                "title": bio_title,
                "tag": "Biology",
                "hours": 9,
                "min_class": int(student_class) if student_class.isdigit() else 10,
                "is_weakness_remedy": is_bio_weak,
                "concept_id": "concept_bio_cell",
                "description": bio_desc,
                "modules": [
                    {
                        "id": f"mod_{track_slug}_bio_1",
                        "title": "Module 1: Cellular Architecture & Bioenergetics",
                        "duration": "1.5 hrs",
                        "concept_id": "concept_bio_cell",
                        "video_url": "https://www.youtube.com/embed/URUJD5NEXC8",
                        "video_title": "CrashCourse Biology: Cell Structure, Organelles & Membrane Transport",
                        "summary": "Mitochondrial ATP synthesis, cell membrane transport, and compartmentalized organelles in eukaryotic cells.",
                        "detailed_notes": [
                            "1. Eukaryotic vs Prokaryotic Organization: Eukaryotes feature membrane-bound organelles and a defined nucleus containing linear DNA wrapped around histone octamers. Prokaryotes (bacteria, archaea) lack membrane-bound organelles and contain a naked circular nucleoid.",
                            "2. Fluid Mosaic Model of Cell Membrane: Proposed by Singer and Nicolson (1972). Phospholipid bilayer with hydrophilic phosphate heads outward and hydrophobic fatty acid tails inward. Integral and peripheral proteins facilitate active and passive transport.",
                            "3. Mitochondria & Cellular Bioenergetics: The powerhouse of the cell. Double membrane system: smooth outer membrane and highly folded inner cristae housing the Electron Transport Chain (ETC) and ATP Synthase (F0-F1 complexes). Aerobic respiration produces 36-38 ATP per glucose molecule.",
                            "4. Endomembrane System: Coordinated system of Rough Endoplasmic Reticulum (protein synthesis with ribosomes), Smooth ER (lipid/steroid synthesis, detoxification), Golgi apparatus (post-translational protein modification and packaging), and Lysosomes (acid hydrolases for intracellular digestion)."
                        ],
                        "formula_note": "Cell Respiration: C6H12O6 + 6O2 -> 6CO2 + 6H2O + 36-38 ATP synthesized via mitochondria.",
                        "formula_sheet": [
                            {
                                "name": "Aerobic Cellular Respiration Stoichiometry",
                                "formula": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36–38 ATP",
                                "variables": "Glucose + Oxygen yields Carbon Dioxide + Water + Adenosine Triphosphate",
                                "notes": "Glycolysis (Cytoplasm: 2 ATP) → Krebs Cycle (Mitochondrial Matrix: 2 ATP) → Oxidative Phosphorylation (Inner Membrane: 32-34 ATP)."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Identify the cellular site of ATP synthase in a eukaryotic plant cell during aerobic respiration.",
                                "solution_steps": [
                                    "Step 1: Cellular respiration proceeds through glycolysis, pyruvate oxidation, citric acid cycle, and oxidative phosphorylation.",
                                    "Step 2: Oxidative phosphorylation relies on a proton gradient generated across the inner mitochondrial membrane.",
                                    "Step 3: ATP Synthase complexes (F0-F1 particles) are embedded specifically in the inner mitochondrial membrane (cristae), releasing newly synthesized ATP into the mitochondrial matrix."
                                ],
                                "key_insight": "In chloroplasts, ATP synthase is in the thylakoid membrane; in mitochondria, it is in the inner membrane cristae."
                            }
                        ],
                        "pitfalls": [
                            "Do NOT include mitochondria, chloroplasts, or peroxisomes as components of the 'endomembrane system'—their functions are not coordinated through vesicular budding from the ER.",
                            "Ribosomes are non-membrane bound organelles found in both prokaryotes (70S) and eukaryotes (80S)."
                        ],
                        "study_materials": [
                            {
                                "title": "NCERT Biology Class 11 Chapter 8: Cell — The Unit of Life",
                                "type": "Official NCERT Chapter",
                                "url": "https://ncert.nic.in/textbook.php"
                            }
                        ],
                        "practice_question": {
                            "q": "Which organelle generates ATP via oxidative phosphorylation?",
                            "options": ["Mitochondria", "Ribosome", "Golgi Body", "Lysosome"],
                            "answer_index": 0,
                            "explanation": "Mitochondria produce ATP through cellular respiration."
                        }
                    },
                    {
                        "id": f"mod_{track_slug}_bio_2",
                        "title": "Module 2: Principles of Mendelian Genetics & Inheritance",
                        "duration": "1.6 hrs",
                        "concept_id": "concept_bio_genetics",
                        "video_url": "https://www.youtube.com/embed/Mehz7tCxjSE",
                        "video_title": "Khan Academy Biology: Mendelian Genetics, Monohybrid Crosses & Punnett Squares",
                        "summary": "Monohybrid and dihybrid crosses, Law of Segregation, Law of Independent Assortment, and Punnett square probability.",
                        "detailed_notes": [
                            "1. Mendel's First Law (Law of Segregation): Alleles of a gene separate during gamete formation so that each gamete carries only one allele for each gene locus. Restored to paired state upon fertilization.",
                            "2. Mendel's Second Law (Independent Assortment): Alleles of two or more different genes sort independently into gametes, provided the genes are located on different non-homologous chromosomes or far apart on the same chromosome (independent of genetic linkage).",
                            "3. Standard Ratios: Monohybrid F2 phenotypic ratio = 3:1 (genotypic 1:2:1). Dihybrid F2 phenotypic ratio (RrYy x RrYy) = 9 Round Yellow : 3 Round Green : 3 Wrinkled Yellow : 1 Wrinkled Green (9:3:3:1)."
                        ],
                        "formula_note": "Mendelian Monohybrid Cross: F2 Phenotypic Ratio = 3 Dominant : 1 Recessive. Genotypic Ratio = 1 TT : 2 Tt : 1 tt.",
                        "formula_sheet": [
                            {
                                "name": "Mendelian Cross Ratios",
                                "formula": "Monohybrid: 3:1 (Phenotype), 1:2:1 (Genotype) | Dihybrid: 9:3:3:1",
                                "variables": "F1 Heterozygote selfing (Tt × Tt) produces 1/4 TT, 1/2 Tt, 1/4 tt.",
                                "notes": "Assumes complete dominance without lethal alleles, epistasis, or tight linkage."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "In a monohybrid cross between two heterozygous tall pea plants (Tt x Tt), what proportion of the offspring are expected to be heterozygous tall?",
                                "solution_steps": [
                                    "Step 1: Set up Punnett square: Gametes T and t from parent 1 cross with T and t from parent 2.",
                                    "Step 2: Offspring genotypes: TT (1/4), Tt (2/4), tt (1/4).",
                                    "Step 3: The heterozygous tall plants have genotype Tt, representing 2/4 = 50% = 1/2."
                                ],
                                "key_insight": "Do not confuse 'proportion of tall plants that are heterozygous' (which is 2/3) with 'proportion of all offspring' (which is 2/4 = 1/2)."
                            }
                        ],
                        "pitfalls": [
                            "Independent assortment fails if two genes are syntenic and tightly linked on the same chromosome (Morgan's Drosophila experiments).",
                            "Incomplete dominance (e.g. Snapdragon flower color) yields a 1:2:1 phenotypic ratio instead of 3:1."
                        ],
                        "study_materials": [
                            {
                                "title": "NCERT Biology Class 12 Chapter 5: Principles of Inheritance and Variation",
                                "type": "Official NCERT Chapter",
                                "url": "https://ncert.nic.in/textbook.php"
                            }
                        ],
                        "practice_question": {
                            "q": "What is the phenotypic ratio in a standard monohybrid cross (Tt x Tt)?",
                            "options": ["3 : 1", "1 : 2 : 1", "9 : 3 : 3 : 1", "1 : 1"],
                            "answer_index": 0,
                            "explanation": "3 Tall to 1 Dwarf phenotype ratio."
                        }
                    }
                ]
            })

        # =========================================================================
        # 4. Mathematics Course (If JEE, CUET Math, CBSE, ICSE, CET)
        # =========================================================================
        if target_goal in ["JEE", "CUET", "CBSE", "ICSE", "State Board", "CET"]:
            is_math_weak = any(any(k in w for k in ["math", "alg", "calc", "linear", "quad", "geometry", "derivative", "trig", "limit", "integral", "factor"]) for w in weak_set)
            
            math_title = (
                f"Class {student_class} {target_goal} Mathematics: Algebra, Polynomials & Calculus Foundations"
                if is_senior else
                f"Class {student_class} {target_goal} Mathematics: Quadratic Equations, Polynomials & Geometry"
            )
            math_desc = (
                f"Mastery of quadratic discriminant analysis, polynomial factorization, limits, and derivative applications tailored for {target_goal} preparation."
                if is_senior else
                f"Linear equations, quadratic roots, coordinate geometry, and algebraic identities aligned with Class {student_class} standards."
            )

            courses.append({
                "id": f"c_{track_slug}_math",
                "track": target_goal,
                "title": math_title,
                "tag": "Math",
                "hours": 8,
                "min_class": int(student_class) if student_class.isdigit() else 10,
                "is_weakness_remedy": is_math_weak,
                "concept_id": "concept_math_limits_derivatives",
                "description": math_desc,
                "modules": [
                    {
                        "id": f"mod_{track_slug}_math_1",
                        "title": "Module 1: Quadratic Equations, Roots & Factorization",
                        "duration": "1.4 hrs",
                        "concept_id": "concept_math_quad_roots",
                        "video_url": "https://www.youtube.com/embed/ZBalWWHYQVE",
                        "video_title": "Khan Academy Algebra: Factoring Quadratic Equations & Quadratic Formula",
                        "summary": "Solving ax^2 + bx + c = 0 via factoring and quadratic formula x = (-b +- sqrt(b^2 - 4ac))/(2a).",
                        "detailed_notes": [
                            "1. Standard Quadratic Equation Form: Any second-degree polynomial equation can be expressed as ax² + bx + c = 0, where a, b, c are real coefficients and a ≠ 0.",
                            "2. Discriminant Analysis (D = b² - 4ac): The discriminant dictates root character: (a) If D > 0, there are two distinct real roots, (b) If D = 0, there is one repeated (equal) real root at x = -b/(2a), (c) If D < 0, there are two conjugate complex roots x = (-b ± i√|D|)/(2a).",
                            "3. Vieta's Formulas for Quadratic Polynomials: For roots α and β: Sum of roots α + β = -b/a, and Product of roots α * β = c/a.",
                            "4. Method of Completing the Square: Transforming ax² + bx + c = 0 into (x + b/(2a))² = (b² - 4ac)/(4a²), which algebraically produces the universal quadratic formula."
                        ],
                        "formula_note": "Quadratic Formula: x = (-b +- sqrt(D)) / (2a), where D = b^2 - 4ac is the discriminant.",
                        "formula_sheet": [
                            {
                                "name": "Universal Quadratic Formula",
                                "formula": "x = (-b ± √(b² - 4ac)) / (2a)",
                                "variables": "a = quadratic coefficient (≠0), b = linear coefficient, c = constant term",
                                "notes": "Roots are real and rational if D is a perfect square."
                            },
                            {
                                "name": "Vieta's Relations",
                                "formula": "α + β = -b/a  |  α * β = c/a",
                                "variables": "α, β = roots of ax² + bx + c = 0",
                                "notes": "Allows reconstructing the quadratic equation: x² - (α + β)x + (αβ) = 0."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Find the roots of the equation x² - 5x + 6 = 0 using both factorization and discriminant methods.",
                                "solution_steps": [
                                    "Step 1 (Factorization): Seek two numbers whose product is 6 and sum is -5. These numbers are -2 and -3.",
                                    "Step 2: Factor: (x - 2)(x - 3) = 0 => x = 2 or x = 3.",
                                    "Step 3 (Discriminant Check): D = (-5)² - 4(1)(6) = 25 - 24 = 1. Since D > 0, roots are distinct real numbers: x = (5 ± √1)/2 = (5 ± 1)/2 => x = 3 or x = 2."
                                ],
                                "key_insight": "Factoring is faster when integer roots exist; the quadratic formula is bulletproof for non-integer or irrational roots."
                            }
                        ],
                        "pitfalls": [
                            "Never divide both sides by x in equations like x² = 5x; doing so illegally destroys the root x = 0! Instead factor as x(x - 5) = 0.",
                            "Remember the entire numerator is divided by 2a, not just the square root term."
                        ],
                        "study_materials": [
                            {
                                "title": "NCERT Mathematics Class 10 Chapter 4: Quadratic Equations",
                                "type": "Official NCERT Chapter",
                                "url": "https://ncert.nic.in/textbook.php"
                            }
                        ],
                        "practice_question": {
                            "q": "What are the roots of x^2 - 5x + 6 = 0?",
                            "options": ["x = 2, 3", "x = -2, -3", "x = 1, 6", "x = -1, -6"],
                            "answer_index": 0,
                            "explanation": "(x-2)(x-3) = 0 => x = 2 and x = 3."
                        }
                    },
                    {
                        "id": f"mod_{track_slug}_math_2",
                        "title": "Module 2: Differential Calculus, Limits & Power Rules",
                        "duration": "1.7 hrs",
                        "concept_id": "concept_math_limits_derivatives",
                        "video_url": "https://www.youtube.com/embed/WUvTyaaNkzM",
                        "video_title": "3Blue1Brown: The Essence of Calculus — Derivative Intuition & Power Rule",
                        "summary": "Limits, tangent slopes, power rule d/dx[x^n] = n*x^(n-1), product rule, and critical inflection points.",
                        "detailed_notes": [
                            "1. Limit Definition of the Derivative: The derivative represents instantaneous rate of change and geometric tangent slope: f'(x) = lim_{h->0} [f(x + h) - f(x)] / h.",
                            "2. The Power Rule: For any real exponent n: d/dx [x^n] = n * x^(n - 1). For example, d/dx [x³] = 3x².",
                            "3. Linearity of Differentiation: Derivative of a sum equals the sum of derivatives: d/dx [f(x) ± g(x)] = f'(x) ± g'(x). Constant multiple rule: d/dx [c * f(x)] = c * f'(x).",
                            "4. Product and Quotient Rules: Product Rule: d/dx [u * v] = u'v + uv'. Quotient Rule: d/dx [u / v] = (u'v - uv') / v²."
                        ],
                        "formula_note": "Power Rule: d/dx[x^n] = n*x^(n-1). Constant Rule: d/dx[c] = 0.",
                        "formula_sheet": [
                            {
                                "name": "Fundamental Power Rule",
                                "formula": "d/dx [xⁿ] = n * xⁿ⁻¹",
                                "variables": "n = any real exponent",
                                "notes": "Special cases: d/dx [x] = 1, d/dx [c] = 0 (constant), d/dx [1/x] = -1/x²."
                            },
                            {
                                "name": "Product Rule",
                                "formula": "d/dx [u * v] = u'v + uv'",
                                "variables": "u, v = differentiable functions of x",
                                "notes": "Do NOT simply multiply individual derivatives!"
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Find the derivative of the polynomial function f(x) = x³ - 4x + 7.",
                                "solution_steps": [
                                    "Step 1: Differentiate term-by-term using sum and power rules.",
                                    "Step 2: d/dx [x³] = 3 * x^(3 - 1) = 3x².",
                                    "Step 3: d/dx [-4x] = -4 * (1) = -4.",
                                    "Step 4: d/dx [7] = 0 (derivative of any constant is zero).",
                                    "Step 5: Combine: f'(x) = 3x² - 4."
                                ],
                                "key_insight": "Constant terms drop out because horizontal shifts do not alter the graph's steepness."
                            }
                        ],
                        "pitfalls": [
                            "Freshman Fallacy: d/dx [u * v] is NOT u' * v'. You must use the product rule u'v + uv'.",
                            "Remember that √x = x^(1/2), so d/dx [√x] = (1/2)x^(-1/2) = 1 / (2√x)."
                        ],
                        "study_materials": [
                            {
                                "title": "NCERT Mathematics Class 11 Chapter 13: Limits and Derivatives",
                                "type": "Official NCERT Chapter",
                                "url": "https://ncert.nic.in/textbook.php"
                            }
                        ],
                        "practice_question": {
                            "q": "What is the derivative of x^3 - 4x + 7?",
                            "options": ["3x^2 - 4", "3x^2 - 4x", "x^2 - 4", "3x^2 + 7"],
                            "answer_index": 0,
                            "explanation": "d/dx(x^3) = 3x^2, d/dx(-4x) = -4, d/dx(7) = 0."
                        }
                    }
                ]
            })

        # =========================================================================
        # 5. CUET General Aptitude Course (If CUET)
        # =========================================================================
        if target_goal == "CUET":
            courses.append({
                "id": "c_cuet_aptitude",
                "track": "CUET",
                "title": f"Class {student_class} CUET General Test: Logical Reasoning & Quantitative Aptitude",
                "tag": "General Aptitude",
                "hours": 7,
                "min_class": int(student_class) if student_class.isdigit() else 11,
                "is_weakness_remedy": False,
                "concept_id": "concept_aptitude_reasoning",
                "description": "Comprehensive prep for Section III General Test: syllogistic reasoning, numerical series, data interpretation, and percentages.",
                "modules": [
                    {
                        "id": "mod_cuet_aptitude_1",
                        "title": "Module 1: Deductive Logic, Syllogisms & Venn Representations",
                        "duration": "1.5 hrs",
                        "concept_id": "concept_aptitude_syllogism",
                        "video_url": "https://www.youtube.com/embed/3gLzHlVqJ_U",
                        "video_title": "Logical Reasoning: Syllogisms, Venn Diagrams & Statement Deductions",
                        "summary": "Mastering universal affirmative (All A are B), particular negative (Some A are not B), and non-overlapping Euler sets.",
                        "detailed_notes": [
                            "1. Deductive Validity: An argument is deductive if the conclusion follows necessarily from premises. Disregard real-world facts and evaluate only structural validity.",
                            "2. Standard Categorical Propositions: (A) Universal Affirmative: All S are P. (E) Universal Negative: No S are P. (I) Particular Affirmative: Some S are P. (O) Particular Negative: Some S are not P.",
                            "3. Venn Diagram Technique: Draw circles for each category. Shade empty regions and mark existential 'x' for positive claims. The conclusion must hold in all valid Venn diagrams."
                        ],
                        "formula_note": "Rule: If both premises are positive, negative conclusion is impossible.",
                        "formula_sheet": [
                            {
                                "name": "Categorical Syllogism Rules",
                                "formula": "Premise 1 + Premise 2 => Valid Conclusion",
                                "variables": "Major term, Minor term, Middle term",
                                "notes": "The middle term must be distributed at least once across the premises."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "Premises: 1. All cats are mammals. 2. All mammals breathe air. What conclusion is logically entailed?",
                                "solution_steps": [
                                    "Step 1: The middle term is 'mammals'.",
                                    "Step 2: Chain: Cats ⊆ Mammals ⊆ Air-breathers.",
                                    "Step 3: Conclusion: All cats breathe air."
                                ],
                                "key_insight": "Transitive subset relationships are universally valid."
                            }
                        ],
                        "pitfalls": ["Do not assume 'Some A are B' implies 'Some A are NOT B' in formal logic."],
                        "study_materials": [
                            {
                                "title": "NTA CUET General Test Section III Syllabus Guide",
                                "type": "Official Examination Guide",
                                "url": "https://exams.nta.ac.in/CUET-UG/"
                            }
                        ],
                        "practice_question": {
                            "q": "If all roses are flowers and all flowers need water, what must be true?",
                            "options": ["All roses need water", "Some roses are not flowers", "Water creates roses", "No roses need water"],
                            "answer_index": 0,
                            "explanation": "Transitive chain: Roses ⊆ Flowers ⊆ Things needing water."
                        }
                    },
                    {
                        "id": "mod_cuet_aptitude_2",
                        "title": "Module 2: Quantitative Aptitude & Data Interpretation",
                        "duration": "1.5 hrs",
                        "concept_id": "concept_aptitude_quant",
                        "video_url": "https://www.youtube.com/embed/FjL6F_0sFVo",
                        "video_title": "Quantitative Aptitude: Percentages, Ratios & Fast Mental Arithmetic",
                        "summary": "Percentage multipliers, successive percentage changes, ratio compounding, and tabular data interpretation.",
                        "detailed_notes": [
                            "1. Percentage Multipliers: An increase of r% is equivalent to multiplying by (1 + r/100). A decrease of r% multiplies by (1 - r/100).",
                            "2. Successive Percentage Change: Net change = a + b + (a*b)/100.",
                            "3. Data Interpretation Framework: Read axes, check scale (millions vs thousands), and calculate relative ratios rather than raw large numbers."
                        ],
                        "formula_note": "Successive change formula: Net % = a + b + (ab/100)%.",
                        "formula_sheet": [
                            {
                                "name": "Successive Percentage Formula",
                                "formula": "Net Change = a + b + (ab / 100)",
                                "variables": "a, b = percentage changes with respective +/- signs",
                                "notes": "For 20% increase followed by 10% decrease: 20 - 10 - (200/100) = +8%."
                            }
                        ],
                        "worked_examples": [
                            {
                                "problem": "A price is increased by 20% and then decreased by 20%. What is the net percentage change?",
                                "solution_steps": [
                                    "Step 1: a = +20, b = -20.",
                                    "Step 2: Net = 20 - 20 + (20 * -20) / 100 = 0 - 400/100 = -4%.",
                                    "Step 3: Result is a 4% decrease."
                                ],
                                "key_insight": "Equal percentage increase followed by decrease always yields a net loss of (x/10)^2 percent."
                            }
                        ],
                        "pitfalls": ["Never simply add percentages together when applied sequentially."],
                        "study_materials": [
                            {
                                "title": "SWAYAM CUET General Aptitude Module",
                                "type": "Official Course Material",
                                "url": "https://swayam.gov.in/"
                            }
                        ],
                        "practice_question": {
                            "q": "A price increases by 20% then drops by 20%. The net change is:",
                            "options": ["4% decrease", "0% change", "4% increase", "2% decrease"],
                            "answer_index": 0,
                            "explanation": "20 - 20 - (400/100) = -4%."
                        }
                    }
                ]
            })

        return courses

    @classmethod
    def get_free_external_courses(cls, goal: str, klass: str) -> List[Dict[str, Any]]:
        """
        Curates authentic, accredited, 100% free courses available online
        from top platforms (Khan Academy, MIT OCW, NPTEL/SWAYAM, DIKSHA, OpenStax).
        Strictly personalized by student's goal (NEET, JEE, CUET, CBSE, ICSE, State Board, CET)
        and grade level (secondary vs senior secondary).
        """
        target_goal = cls.resolve_goal_key(goal, klass)
        student_class = str(klass).strip() if klass else "10"
        is_senior = student_class in ["11", "12", "Degree", "Undergraduate"]

        # ---------------------------------------------------------
        # Undergraduate / GATE / Placement / Data Science Tracks
        # ---------------------------------------------------------
        if target_goal in ["GATE", "Software Engineering & Placements", "Data Science & AI", "CAT", "Undergraduate"] or student_class in ["Degree", "Undergraduate"]:
            if target_goal == "GATE":
                return [
                    {
                        "id": "ext_nptel_gate_cs",
                        "title": "NPTEL: GATE Computer Science & Information Technology",
                        "platform": "NPTEL / SWAYAM",
                        "provider": "IIT Kharagpur & IISc Bangalore",
                        "url": "https://nptel.ac.in/courses/106106131",
                        "tag": "Computer Science",
                        "track": "GATE",
                        "class_level": "Undergraduate / Degree",
                        "duration": "Comprehensive Full Syllabus Series",
                        "rating": 4.9,
                        "badge": "IIT / IISc Standard",
                        "description": "Comprehensive GATE CS series covering Theory of Computation, Algorithms, Computer Architecture, and Operating Systems with previous years' solved questions."
                    },
                    {
                        "id": "ext_mit_6006_gate",
                        "title": "MIT OCW 6.006: Introduction to Algorithms",
                        "platform": "MIT OpenCourseWare",
                        "provider": "Massachusetts Institute of Technology (MIT)",
                        "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
                        "tag": "Algorithms",
                        "track": "GATE",
                        "class_level": "Undergraduate / Degree",
                        "duration": "24 Lectures + Problem Sets & Recitations",
                        "rating": 5.0,
                        "badge": "World-Class Reference",
                        "description": "In-depth mathematical analysis of sorting, trees, hashing, shortest paths, and dynamic programming essential for high-percentile GATE problem solving."
                    },
                    {
                        "id": "ext_nptel_dbms_gate",
                        "title": "NPTEL: Database Management Systems (IIT Madras)",
                        "platform": "NPTEL / SWAYAM",
                        "provider": "IIT Madras",
                        "url": "https://nptel.ac.in/courses/106106093",
                        "tag": "Database Systems",
                        "track": "GATE",
                        "class_level": "Undergraduate / Degree",
                        "duration": "8 Weeks (40 Lectures)",
                        "rating": 4.8,
                        "badge": "IIT Madras Faculty",
                        "description": "Relational algebra, SQL, normal forms (BCNF/3NF), indexing with B+ trees, and transaction concurrency control for GATE."
                    },
                    {
                        "id": "ext_mit_1806_lin_alg",
                        "title": "MIT OCW 18.06: Linear Algebra (Prof. Gilbert Strang)",
                        "platform": "MIT OpenCourseWare",
                        "provider": "Massachusetts Institute of Technology (MIT)",
                        "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
                        "tag": "Engineering Mathematics",
                        "track": "GATE",
                        "class_level": "Undergraduate / Degree",
                        "duration": "35 Lectures + Worked Recitations",
                        "rating": 5.0,
                        "badge": "Legendary Series",
                        "description": "Vector spaces, subspaces, eigenvalues, eigenvectors, orthogonality, and singular value decomposition."
                    }
                ]
            if target_goal == "Data Science & AI":
                return [
                    {
                        "id": "ext_mit_ai_6034",
                        "title": "MIT OCW 6.034: Artificial Intelligence (Prof. Patrick Winston)",
                        "platform": "MIT OpenCourseWare",
                        "provider": "Massachusetts Institute of Technology (MIT)",
                        "url": "https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/",
                        "tag": "Machine Learning",
                        "track": "Data Science & AI",
                        "class_level": "Undergraduate / Degree",
                        "duration": "30 Lectures + Demonstrations",
                        "rating": 4.9,
                        "badge": "MIT Standard",
                        "description": "Search heuristics, neural networks, SVMs, constraint satisfaction, and rule-based expert systems."
                    },
                    {
                        "id": "ext_harvard_cs50_ai",
                        "title": "CS50's Introduction to Artificial Intelligence with Python",
                        "platform": "Harvard Online / edX",
                        "provider": "Harvard University",
                        "url": "https://cs50.harvard.edu/ai/",
                        "tag": "Python & Data Analysis",
                        "track": "Data Science & AI",
                        "class_level": "Undergraduate / Degree",
                        "duration": "7 Weeks Hands-on Projects",
                        "rating": 5.0,
                        "badge": "Harvard Certified",
                        "description": "Graph search, adversarial games (Minimax), reinforcement learning, Markov models, and natural language processing in Python."
                    },
                    {
                        "id": "ext_mit_1806_ds",
                        "title": "MIT OCW 18.06: Linear Algebra & Matrix Methods for ML",
                        "platform": "MIT OpenCourseWare",
                        "provider": "Massachusetts Institute of Technology (MIT)",
                        "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
                        "tag": "Linear Algebra",
                        "track": "Data Science & AI",
                        "class_level": "Undergraduate / Degree",
                        "duration": "35 Lectures + Worked Recitations",
                        "rating": 5.0,
                        "badge": "Core ML Foundation",
                        "description": "Fundamental matrix algebra, orthogonal projections, PCA foundations, and SVD decomposition for AI."
                    }
                ]
            if target_goal == "CAT":
                return [
                    {
                        "id": "ext_khan_quant_cat",
                        "title": "Khan Academy Advanced Quantitative Aptitude & Algebra",
                        "platform": "Khan Academy",
                        "provider": "Khan Academy",
                        "url": "https://www.khanacademy.org/math/algebra",
                        "tag": "Quantitative Aptitude",
                        "track": "CAT",
                        "class_level": "Undergraduate / Degree",
                        "duration": "Self-paced Mastery Modules",
                        "rating": 4.9,
                        "badge": "100% Free Interactive",
                        "description": "Higher arithmetic, speed math, modular arithmetic, quadratic functions, and combinatorics for CAT aspirants."
                    },
                    {
                        "id": "ext_openstax_stats_cat",
                        "title": "OpenStax Introductory Statistics & Data Interpretation",
                        "platform": "OpenStax",
                        "provider": "Rice University",
                        "url": "https://openstax.org/details/books/introductory-statistics",
                        "tag": "Data Interpretation & Logical Reasoning",
                        "track": "CAT",
                        "class_level": "Undergraduate / Degree",
                        "duration": "Complete Digital Textbook & Datasets",
                        "rating": 4.8,
                        "badge": "Peer-Reviewed Open Access",
                        "description": "Comprehensive statistical reasoning, distributions, probability tables, and data interpretation case studies."
                    }
                ]
            # Default Undergraduate / Software Engineering & Placements
            return [
                {
                    "id": "ext_harvard_cs50_core",
                    "title": "Harvard CS50: Introduction to Computer Science",
                    "platform": "Harvard Online / edX",
                    "provider": "Harvard University",
                    "url": "https://cs50.harvard.edu/x/",
                    "tag": "Computer Science",
                    "track": target_goal,
                    "class_level": "Undergraduate / Degree",
                    "duration": "11 Weeks (Self-paced)",
                    "rating": 5.0,
                    "badge": "World's Top Rated CS Course",
                    "description": "Legendary introduction to algorithmic thinking, memory management, C, Python, SQL, and full-stack software development."
                },
                {
                    "id": "ext_mit_6006_undergrad",
                    "title": "MIT OCW 6.006: Introduction to Algorithms & Data Structures",
                    "platform": "MIT OpenCourseWare",
                    "provider": "Massachusetts Institute of Technology (MIT)",
                    "url": "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/",
                    "tag": "Data Structures & Algorithms",
                    "track": target_goal,
                    "class_level": "Undergraduate / Degree",
                    "duration": "24 Lectures + Problem Sets",
                    "rating": 5.0,
                    "badge": "MIT Engineering Standard",
                    "description": "Rigorous algorithm design: asymptotic bounds, balanced binary search trees, graph algorithms, Dijkstra, Bellman-Ford, and dynamic programming."
                },
                {
                    "id": "ext_nptel_os_undergrad",
                    "title": "NPTEL: Operating Systems & System Programming (IIT Kharagpur)",
                    "platform": "NPTEL / SWAYAM",
                    "provider": "IIT Kharagpur",
                    "url": "https://nptel.ac.in/courses/106105214",
                    "tag": "Operating Systems",
                    "track": target_goal,
                    "class_level": "Undergraduate / Degree",
                    "duration": "12 Weeks (Free Online Certification)",
                    "rating": 4.8,
                    "badge": "IIT Professor Lectures",
                    "description": "Processes, threads, CPU scheduling, synchronization primitives, deadlocks, virtual memory management, and file systems."
                },
                {
                    "id": "ext_mit_1806_math",
                    "title": "MIT OCW 18.06: Linear Algebra & Matrix Calculus",
                    "platform": "MIT OpenCourseWare",
                    "provider": "Massachusetts Institute of Technology (MIT)",
                    "url": "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/",
                    "tag": "Engineering Mathematics",
                    "track": target_goal,
                    "class_level": "Undergraduate / Degree",
                    "duration": "35 Lectures + Worked Recitations",
                    "rating": 5.0,
                    "badge": "Core STEM Foundation",
                    "description": "Matrix equations, vector spaces, null space, projection, eigenvalues, and positive definite matrices."
                }
            ]

        # ---------------------------------------------------------
        # NEET Track (Medical Aspirants)
        # ---------------------------------------------------------
        if target_goal == "NEET":
            return [
                {
                    "id": "ext_khan_bio_neet",
                    "title": "Khan Academy AP & College Biology (Pre-Med & NEET Aligned)",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy",
                    "url": "https://www.khanacademy.org/science/ap-biology",
                    "tag": "Biology",
                    "track": "NEET",
                    "class_level": "Class 11-12 & Droppers",
                    "duration": "Self-paced (60+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Open Access",
                    "description": "Comprehensive interactive units covering Cellular Energetics, Molecular Genetics, Natural Selection, and Ecology with instant-feedback mastery quizzes."
                },
                {
                    "id": "ext_mit_bio_7016",
                    "title": "MIT OCW 7.016: Introductory Biology (Molecular & Cellular)",
                    "platform": "MIT OpenCourseWare",
                    "provider": "Massachusetts Institute of Technology (MIT)",
                    "url": "https://ocw.mit.edu/courses/7-016-introductory-biology-fall-2018/",
                    "tag": "Biology",
                    "track": "NEET",
                    "class_level": "Class 11-12 & Medical Entrances",
                    "duration": "36 Lectures + Exams & Recitations",
                    "rating": 4.9,
                    "badge": "World-Class University Curriculum",
                    "description": "Official MIT course taught by leading biologists. Covers biochemistry, genetics, molecular biology, recombinant DNA, and human disease mechanisms."
                },
                {
                    "id": "ext_nptel_bio_medical",
                    "title": "NPTEL Swayam: Cell Biology and Genetics for Medical Aspirants",
                    "platform": "NPTEL / SWAYAM",
                    "provider": "IIT Kanpur & Govt. of India",
                    "url": "https://nptel.ac.in/courses/102104052",
                    "tag": "Biology",
                    "track": "NEET",
                    "class_level": "Class 11-12 & Pre-Med",
                    "duration": "12 Weeks (Free Online Certification)",
                    "rating": 4.8,
                    "badge": "Govt. of India Certified",
                    "description": "Rigorous conceptual video series covering eukaryotic cell physiology, Mendelian and non-Mendelian genetic inheritance, and chromosome mechanics."
                },
                {
                    "id": "ext_diksha_neet_bio",
                    "title": "DIKSHA NCERT Class 11-12 Biology Digital Repository",
                    "platform": "DIKSHA (NCERT)",
                    "provider": "Ministry of Education, Govt. of India",
                    "url": "https://diksha.gov.in/ncert/explore",
                    "tag": "Biology",
                    "track": "NEET",
                    "class_level": "Class 11 & 12",
                    "duration": "Official Textbook Curriculum",
                    "rating": 4.8,
                    "badge": "Official NCERT Standards",
                    "description": "Official government portal offering chapter-by-chapter animated visual modules, QR-code lesson plans, and authentic NCERT line-by-line notes."
                },
                {
                    "id": "ext_khan_chem_org",
                    "title": "Khan Academy Organic Chemistry: Carbon Pathways & Mechanisms",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy",
                    "url": "https://www.khanacademy.org/science/organic-chemistry",
                    "tag": "Chemistry",
                    "track": "NEET",
                    "class_level": "Class 11-12",
                    "duration": "Self-paced (45+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Open Access",
                    "description": "Master nucleophilic substitutions (SN1/SN2), elimination, aromatic electrophilic pathways, and functional group transformations essential for NEET."
                },
                {
                    "id": "ext_openstax_bio",
                    "title": "OpenStax Biology 2e (Peer-Reviewed Complete Curriculum)",
                    "platform": "OpenStax",
                    "provider": "Rice University",
                    "url": "https://openstax.org/details/books/biology-2e",
                    "tag": "Biology",
                    "track": "NEET",
                    "class_level": "Class 11-12 & Medical",
                    "duration": "Full Textbook & Question Banks",
                    "rating": 4.9,
                    "badge": "Peer-Reviewed Open Access",
                    "description": "Complete, peer-reviewed university-grade biology textbook with high-resolution anatomical schematics, end-of-chapter problems, and interactive answers."
                }
            ]

        # ---------------------------------------------------------
        # JEE Track (Engineering Aspirants)
        # ---------------------------------------------------------
        if target_goal == "JEE":
            return [
                {
                    "id": "ext_mit_phys_801",
                    "title": "MIT OCW 8.01SC: Classical Mechanics (Prof. Walter Lewin)",
                    "platform": "MIT OpenCourseWare",
                    "provider": "Massachusetts Institute of Technology (MIT)",
                    "url": "https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/",
                    "tag": "Physics",
                    "track": "JEE",
                    "class_level": "Class 11-12 & JEE Advanced",
                    "duration": "Complete 35 Lectures + Problem Sets",
                    "rating": 5.0,
                    "badge": "Legendary MIT Series",
                    "description": "The world's most acclaimed physics lecture series. Demonstrates Newton's laws, rotational dynamics, gravitation, and harmonic oscillations from first principles."
                },
                {
                    "id": "ext_nptel_phys_eng",
                    "title": "NPTEL: Core Engineering Physics & Mechanics for JEE",
                    "platform": "NPTEL / SWAYAM",
                    "provider": "IIT Kharagpur",
                    "url": "https://nptel.ac.in/courses/115105104",
                    "tag": "Physics",
                    "track": "JEE",
                    "class_level": "Class 11-12 & JEE Main/Adv",
                    "duration": "40 Lectures + Assignments",
                    "rating": 4.8,
                    "badge": "IIT Professor Lectures",
                    "description": "Rigorous mathematical derivations of wave motion, rotational kinematics, Lagrangian formulations, and central force gravitation tailored for engineering tests."
                },
                {
                    "id": "ext_khan_calc_bc",
                    "title": "Khan Academy AP Calculus BC & Differential Equations",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy",
                    "url": "https://www.khanacademy.org/math/ap-calculus-bc",
                    "tag": "Math",
                    "track": "JEE",
                    "class_level": "Class 11-12",
                    "duration": "Self-paced (50+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Interactive",
                    "description": "Complete mastery of limits, differential calculus, integration techniques, Taylor series, and parametric vectors directly applicable to JEE Main and Advanced."
                },
                {
                    "id": "ext_mit_math_1801",
                    "title": "MIT OCW 18.01SC: Single Variable Calculus",
                    "platform": "MIT OpenCourseWare",
                    "provider": "Massachusetts Institute of Technology (MIT)",
                    "url": "https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/",
                    "tag": "Math",
                    "track": "JEE",
                    "class_level": "Class 11-12 & JEE Advanced",
                    "duration": "35 Video Lectures + Recitations",
                    "rating": 4.9,
                    "badge": "MIT Undergraduate Level",
                    "description": "Foundational course covering differentiation, optimization, Mean Value Theorem, fundamental theorem of calculus, and integration applications."
                },
                {
                    "id": "ext_nptel_math_eng",
                    "title": "NPTEL: Advanced Engineering Mathematics (IIT Roorkee)",
                    "platform": "NPTEL / SWAYAM",
                    "provider": "IIT Roorkee",
                    "url": "https://nptel.ac.in/courses/111107119",
                    "tag": "Math",
                    "track": "JEE",
                    "class_level": "Class 12 & Engineering",
                    "duration": "40 Lectures",
                    "rating": 4.7,
                    "badge": "Govt. of India Certified",
                    "description": "Deep dive into matrix algebra, eigenvalue analysis, vector calculus, and multivariable functions for aspiring engineers."
                },
                {
                    "id": "ext_openstax_univ_phys",
                    "title": "OpenStax University Physics Volume 1 (Mechanics & Waves)",
                    "platform": "OpenStax",
                    "provider": "Rice University",
                    "url": "https://openstax.org/details/books/university-physics-volume-1",
                    "tag": "Physics",
                    "track": "JEE",
                    "class_level": "Class 11-12 & JEE Main/Adv",
                    "duration": "Complete Calculus-Based Textbook",
                    "rating": 4.9,
                    "badge": "Calculus-Based STEM Standard",
                    "description": "Three-volume calculus-based physics series covering kinematics, dynamics, work, energy, rotational dynamics, momentum, and gravitation with complete solutions."
                }
            ]

        # ---------------------------------------------------------
        # CUET Track
        # ---------------------------------------------------------
        if target_goal == "CUET":
            return [
                {
                    "id": "ext_swayam_cuet",
                    "title": "SWAYAM Course Explorer: CUET UG Preparation & Domain Electives",
                    "platform": "NPTEL / SWAYAM",
                    "provider": "National Testing Agency & UGC",
                    "url": "https://swayam.gov.in/explorer",
                    "tag": "General Aptitude",
                    "track": "CUET",
                    "class_level": "Class 12 & University Entrances",
                    "duration": "Self-paced Modular Prep",
                    "rating": 4.8,
                    "badge": "Official University Portal",
                    "description": "National digital learning portal directly indexing Section I Languages, Section II Domain Subjects, and Section III General Test courses."
                },
                {
                    "id": "ext_khan_cuet_math",
                    "title": "Khan Academy College Prep Algebra & Quantitative Reasoning",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy",
                    "url": "https://www.khanacademy.org/math/algebra",
                    "tag": "Math",
                    "track": "CUET",
                    "class_level": "Class 12",
                    "duration": "Self-paced (40+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Interactive",
                    "description": "Focused problem sets across linear equations, inequalities, graphs, systems, polynomials, and rapid data interpretation techniques."
                },
                {
                    "id": "ext_diksha_cuet_ncert",
                    "title": "DIKSHA NCERT Class 12 Domain Disciplines Portal",
                    "platform": "DIKSHA (NCERT)",
                    "provider": "Ministry of Education, Govt. of India",
                    "url": "https://diksha.gov.in/ncert/explore",
                    "tag": "General Aptitude",
                    "track": "CUET",
                    "class_level": "Class 12",
                    "duration": "All Domain Subjects",
                    "rating": 4.8,
                    "badge": "Official NCERT Standards",
                    "description": "Complete NCERT Class 12 digitized curriculum modules for Science, Commerce, and Humanities domain papers in CUET UG."
                },
                {
                    "id": "ext_openstax_stats",
                    "title": "OpenStax Introductory Statistics (CUET General Test Aligned)",
                    "platform": "OpenStax",
                    "provider": "Rice University",
                    "url": "https://openstax.org/details/books/introductory-statistics",
                    "tag": "Math",
                    "track": "CUET",
                    "class_level": "Class 12 & College",
                    "duration": "Full Course Textbook & Datasets",
                    "rating": 4.8,
                    "badge": "Peer-Reviewed Open Access",
                    "description": "Master descriptive statistics, probability distributions, hypothesis testing, and regression analysis for quantitative reasoning."
                }
            ]

        # ---------------------------------------------------------
        # CBSE / ICSE / State Board — Senior Secondary (Class 11-12)
        # ---------------------------------------------------------
        if is_senior:
            return [
                {
                    "id": f"ext_diksha_{target_goal.lower().replace(' ', '_')}_senior",
                    "title": f"DIKSHA: NCERT Class 11-12 {target_goal} Digital Learning Repository",
                    "platform": "DIKSHA (NCERT)",
                    "provider": "Ministry of Education & State Boards",
                    "url": "https://diksha.gov.in/ncert/explore",
                    "tag": "Physics",
                    "track": target_goal,
                    "class_level": f"Class {student_class}",
                    "duration": "Complete Official Board Syllabus",
                    "rating": 4.9,
                    "badge": "Official Curriculum Portal",
                    "description": f"State and national board textbook-aligned interactive lessons, laboratory experiments, board derivation guides, and exemplar question solutions for {target_goal}."
                },
                {
                    "id": "ext_khan_india_senior_phys",
                    "title": "Khan Academy India: Class 11 & 12 Physics (NCERT Standards)",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy India",
                    "url": "https://www.khanacademy.org/science/in-in-class-11th-physics",
                    "tag": "Physics",
                    "track": target_goal,
                    "class_level": f"Class {student_class}",
                    "duration": "Self-paced (45+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Aligned",
                    "description": "In-depth video tutorials and step-by-step problem sets covering Kinematics, Laws of Motion, Work Energy, Waves, and Electromagnetism with Indian curriculum mapping."
                },
                {
                    "id": "ext_khan_india_senior_chem",
                    "title": "Khan Academy India: Class 11 & 12 Chemistry (NCERT Standards)",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy India",
                    "url": "https://www.khanacademy.org/science/in-in-class-11th-chemistry-india",
                    "tag": "Chemistry",
                    "track": target_goal,
                    "class_level": f"Class {student_class}",
                    "duration": "Self-paced (40+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Aligned",
                    "description": "Chemical Bonding, Equilibrium, Thermodynamics, Organic Reaction Mechanisms, and Coordination Chemistry with board exam pattern questions."
                },
                {
                    "id": "ext_khan_india_senior_math",
                    "title": "Khan Academy India: Class 11 & 12 Mathematics (NCERT Standards)",
                    "platform": "Khan Academy",
                    "provider": "Khan Academy India",
                    "url": "https://www.khanacademy.org/math/in-in-class-11th-math",
                    "tag": "Math",
                    "track": target_goal,
                    "class_level": f"Class {student_class}",
                    "duration": "Self-paced (50+ Hours)",
                    "rating": 4.9,
                    "badge": "100% Free Aligned",
                    "description": "Sets, Relations, Trigonometric Functions, Complex Numbers, Permutations, Sequences, and Calculus with Indian board exam pattern problems."
                },
                {
                    "id": "ext_openstax_college_phys",
                    "title": "OpenStax College Physics (Algebra/Trig Based Complete Course)",
                    "platform": "OpenStax",
                    "provider": "Rice University",
                    "url": "https://openstax.org/details/books/college-physics",
                    "tag": "Physics",
                    "track": target_goal,
                    "class_level": f"Class {student_class}",
                    "duration": "Complete Course & Practice Banks",
                    "rating": 4.9,
                    "badge": "Peer-Reviewed Open Access",
                    "description": "Richly illustrated conceptual physics covering mechanical equilibrium, heat transfer, electromagnetic induction, and optics without heavy calculus."
                }
            ]

        # ---------------------------------------------------------
        # CBSE / ICSE / State Board — Secondary (Class 8, 9, 10)
        # ---------------------------------------------------------
        return [
            {
                "id": f"ext_diksha_{target_goal.lower().replace(' ', '_')}_class{student_class}",
                "title": f"DIKSHA: NCERT Class {student_class} {target_goal} Science & Mathematics Portal",
                "platform": "DIKSHA (NCERT)",
                "provider": "Ministry of Education & State Boards",
                "url": "https://diksha.gov.in/ncert/explore",
                "tag": "Physics",
                "track": target_goal,
                "class_level": f"Class {student_class}",
                "duration": "Complete School Academic Year",
                "rating": 4.9,
                "badge": "Official Curriculum Portal",
                "description": f"Interactive multimedia courses directly linked to official NCERT / State Board textbooks for Class {student_class}. Includes animated experiments, chapter summaries, and sample papers."
            },
            {
                "id": f"ext_khan_india_math_class{student_class}",
                "title": f"Khan Academy India: Class {student_class} Mathematics (NCERT Aligned)",
                "platform": "Khan Academy",
                "provider": "Khan Academy India",
                "url": f"https://www.khanacademy.org/math/in-in-class-{student_class}th-math" if student_class in ["9", "10"] else "https://www.khanacademy.org/math/in-in-class-10th-math",
                "tag": "Math",
                "track": target_goal,
                "class_level": f"Class {student_class}",
                "duration": "Self-paced (50+ Hours)",
                "rating": 5.0,
                "badge": "100% Free Interactive",
                "description": f"Master quadratic equations, arithmetic progressions, coordinate geometry, trigonometry, and surface areas with gamified practice and step-by-step video hints."
            },
            {
                "id": f"ext_khan_india_phys_class{student_class}",
                "title": f"Khan Academy India: Class {student_class} Physics",
                "platform": "Khan Academy",
                "provider": "Khan Academy India",
                "url": "https://www.khanacademy.org/science/in-in-class10-physics-india",
                "tag": "Physics",
                "track": target_goal,
                "class_level": f"Class {student_class}",
                "duration": "Self-paced (40+ Hours)",
                "rating": 4.9,
                "badge": "100% Free Interactive",
                "description": "Electricity, magnetic effects of electric current, light reflection and refraction taught with intuitive conceptual demonstrations and simulations."
            },
            {
                "id": f"ext_khan_india_chem_class{student_class}",
                "title": f"Khan Academy India: Class {student_class} Chemistry",
                "platform": "Khan Academy",
                "provider": "Khan Academy India",
                "url": "https://www.khanacademy.org/science/in-in-class10-chemistry-india",
                "tag": "Chemistry",
                "track": target_goal,
                "class_level": f"Class {student_class}",
                "duration": "Self-paced (35+ Hours)",
                "rating": 4.9,
                "badge": "100% Free Interactive",
                "description": "Chemical reactions and equations, acids bases and salts, metals and non-metals, carbon and its compounds with step-by-step practice."
            },
            {
                "id": "ext_openstax_highschool_phys",
                "title": "OpenStax High School Physics (Complete Digital Course & Textbook)",
                "platform": "OpenStax",
                "provider": "Rice University",
                "url": "https://openstax.org/details/books/physics",
                "tag": "Physics",
                "track": target_goal,
                "class_level": f"Class {student_class}",
                "duration": "Self-paced Textbook & Labs",
                "rating": 4.9,
                "badge": "Peer-Reviewed Open Access",
                "description": "Engaging real-world physics explanations, motion simulations, and conceptual exercises designed specifically for high school students building strong STEM foundations."
            }
        ]


