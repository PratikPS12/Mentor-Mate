from typing import Dict, Any, List, Optional
from app.core.database import db_manager
from app.services.curriculum.curriculum_engine import CurriculumEngine

class RecommendationService:
    """
    Evidence-driven resource and course recommendation engine.
    Multi-objective ranking based on student mastery gaps, curriculum alignment, and prerequisite fit.
    """

    # Static foundational accredited courses
    COURSES_CATALOG = [
        {
            "id": "c_org_review",
            "track": "All",
            "title": "Organic Chemistry Rapid Review",
            "tag": "Chemistry",
            "hours": 6,
            "min_class": 11,
            "concept_id": "concept_chem_reaction_mechanisms",
            "description": "Comprehensive sprint across IUPAC naming, aromatic systems, and nucleophilic substitution mechanisms for JEE/NEET/Boards.",
            "modules": [
                {
                    "id": "mod_org_1",
                    "title": "Module 1: IUPAC Nomenclature & Functional Groups",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_chem_iupac",
                    "video_url": "https://www.youtube.com/embed/cExhtwVT1v0",
                    "video_title": "Khan Academy Organic Chemistry: IUPAC Nomenclature of Functional Carbon Compounds",
                    "summary": "Mastering the longest chain rule, principal functional group priority (alcohols, aldehydes, carboxylic acids), and suffix rules.",
                    "detailed_notes": [
                        "1. IUPAC Naming Architecture: Every systematic name consists of: Prefix (substituent branches) + Root Word (longest continuous carbon chain: meth-, eth-, prop-, but-, pent-) + Primary Suffix (saturation: -ane, -ene, -yne) + Secondary Suffix (principal functional group: -oic acid, -al, -one, -ol, -amine).",
                        "2. Priority Hierarchy: -COOH > -SO3H > -COOR > -CONH2 > -CN > -CHO > -CO- > -OH > -NH2. The highest priority functional group determines the principal suffix and the numbering direction.",
                        "3. Lowest Locants: Number the parent chain from the end that gives the principal group the lowest possible number. When multiple substituents exist, list them alphabetically in the prefix."
                    ],
                    "formula_note": "Rule: Suffix priority: -COOH > -SO3H > -COOR > -CONH2 > -CN > -CHO > -CO- > -OH > -NH2.",
                    "formula_sheet": [
                        {
                            "name": "IUPAC Functional Group Priority Sequence",
                            "formula": "-COOH > -SO₃H > -COOR > -CONH₂ > -CN > -CHO > -CO- > -OH > -NH₂",
                            "variables": "Determines suffix assignment vs prefix substituent designation.",
                            "notes": "Alkyl groups and halogens are always treated as substituent prefixes."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "Name the compound CH3-CH2-OH using systematic IUPAC rules.",
                            "solution_steps": [
                                "Step 1: Longest carbon chain contains 2 carbons -> root word 'eth-'.",
                                "Step 2: Carbon-carbon single bonds -> primary suffix '-an-'.",
                                "Step 3: Principal group is alcohol (-OH) -> secondary suffix '-ol'.",
                                "Step 4: Combine: Ethanol."
                            ],
                            "key_insight": "Position locant '1' is omitted for ethanol since -OH can only be at position 1 on a 2-carbon chain."
                        }
                    ],
                    "pitfalls": [
                        "Do NOT assume the longest continuous chain is always horizontal.",
                        "Never forget to alphabetize prefixes (e.g. ethyl precedes methyl regardless of numerical locant)."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Chemistry Class 11 Chapter 12: Organic Chemistry Basics",
                            "type": "Official Textbook Reference",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "What is the systematic IUPAC name for CH3-CH2-OH?",
                        "options": ["Ethanol", "Methanol", "Ethane", "Dimethylether"],
                        "answer_index": 0,
                        "explanation": "2-carbon parent chain is ethane. Suffix '-ol' denotes the primary alcohol group, giving ethanol."
                    }
                },
                {
                    "id": "mod_org_2",
                    "title": "Module 2: Aromaticity, Benzene & Resonance Stabilization",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_chem_aromatic",
                    "video_url": "https://www.youtube.com/embed/oDigu9YxXUg",
                    "video_title": "Khan Academy Organic Chemistry: Aromatic Compounds & Hückel's (4n+2) Rule",
                    "summary": "Huckel's (4n+2) pi-electron rule, planar cyclic conjugated systems, electrophilic aromatic substitution, and ortho/para directors.",
                    "detailed_notes": [
                        "1. Criteria for Aromaticity: To be aromatic, a molecule must be: (a) Cyclic, (b) Planar, (c) Completely conjugated around the ring with sp2/sp hybridized atoms, and (d) Contain (4n + 2) pi electrons.",
                        "2. Anti-Aromaticity: Planar, cyclic, fully conjugated systems with 4n pi electrons (4, 8, 12) are anti-aromatic and exceptionally unstable.",
                        "3. Benzene Resonance: Benzene (6 pi electrons, n=1) possesses ~150 kJ/mol of resonance energy, favoring electrophilic substitution over addition."
                    ],
                    "formula_note": "Huckel's Rule: Cyclic, planar, completely conjugated system with (4n + 2) pi electrons is aromatic.",
                    "formula_sheet": [
                        {
                            "name": "Hückel's (4n+2) Formula",
                            "formula": "Pi Electrons = 4n + 2 (n = 0, 1, 2, 3...)",
                            "variables": "n = 0 (2 pi e⁻), n = 1 (6 pi e⁻: Benzene), n = 2 (10 pi e⁻: Naphthalene)",
                            "notes": "Applies strictly to planar, cyclic, completely conjugated systems."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "Is Benzene (C6H6) aromatic?",
                            "solution_steps": [
                                "Step 1: Benzene is a 6-membered planar ring.",
                                "Step 2: All 6 carbons are sp2 hybridized, providing a continuous p-orbital ring.",
                                "Step 3: 3 double bonds provide 6 pi electrons. 4n + 2 = 6 => n = 1 (integer).",
                                "Step 4: Conclusion: Benzene is aromatic."
                            ],
                            "key_insight": "The high resonance stabilization energy makes benzene resistant to typical alkene addition reactions."
                        }
                    ],
                    "pitfalls": [
                        "Non-planar rings (like cyclooctatetraene in tub conformation) are non-aromatic, NOT anti-aromatic."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Chemistry Class 11 Chapter 13: Aromatic Hydrocarbons",
                            "type": "Official Textbook Reference",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "Benzene (C6H6) is classified as:",
                        "options": ["Alkane", "Alkene", "Aromatic", "Cycloalkane"],
                        "answer_index": 2,
                        "explanation": "Benzene has a planar cyclic ring with 6 delocalized pi electrons (n=1), making it aromatic."
                    }
                },
                {
                    "id": "mod_org_3",
                    "title": "Module 3: Nucleophilic Substitution Mechanisms (SN1 vs SN2)",
                    "duration": "1.8 hrs",
                    "concept_id": "concept_chem_reaction_mechanisms",
                    "video_url": "https://www.youtube.com/embed/wCspf85eQQo",
                    "video_title": "Khan Academy Organic Chemistry: Nucleophilic Substitution Mechanisms (SN1 vs SN2)",
                    "summary": "Stepwise unimolecular SN1 with planar carbocation intermediate vs concerted bimolecular SN2 with Walden inversion.",
                    "detailed_notes": [
                        "1. SN1 Mechanism: Two-step unimolecular substitution. Step 1 is the slow rate-determining loss of leaving group to form a planar carbocation. Step 2 is nucleophilic attack from either face, producing racemization. Rate = k[Substrate]. Favored by tertiary substrates and polar protic solvents.",
                        "2. SN2 Mechanism: One-step concerted bimolecular substitution. Backside nucleophilic attack causes simultaneous departure of the leaving group, resulting in 100% Walden inversion of stereochemistry. Rate = k[Substrate][Nucleophile]. Favored by primary/methyl substrates and polar aprotic solvents."
                    ],
                    "formula_note": "SN1: Rate = k[R-X] (forms carbocation). SN2: Rate = k[R-X][Nu-] (concerted backside attack with inversion).",
                    "formula_sheet": [
                        {
                            "name": "SN1 vs SN2 Kinetics & Substrate Preference",
                            "formula": "SN1: 3° > 2° >> 1° (Carbocation stability) | SN2: Methyl > 1° > 2° >> 3° (Steric hindrance)",
                            "variables": "3°: tertiary, 2°: secondary, 1°: primary alkyl halides",
                            "notes": "SN1 favored in polar protic solvents (H2O, EtOH); SN2 in polar aprotic (Acetone, DMSO, DMF)."
                        }
                    ],
                    "worked_examples": [
                        {
                            "problem": "Which substrate undergoes fastest substitution via SN2 mechanism: 1-bromobutane or 2-bromo-2-methylpropane?",
                            "solution_steps": [
                                "Step 1: Identify substrate degrees: 1-bromobutane is primary (1°); 2-bromo-2-methylpropane is tertiary (3°).",
                                "Step 2: SN2 rate depends inversely on steric congestion around the alpha carbon.",
                                "Step 3: Primary halide allows unhindered backside nucleophilic attack. Therefore, 1-bromobutane is much faster."
                            ],
                            "key_insight": "Tertiary substrates are virtually inert to SN2 due to severe steric crowding."
                        }
                    ],
                    "pitfalls": [
                        "Do not use polar protic solvents for SN2 as they hydrogen-bond and deactivate the nucleophile."
                    ],
                    "study_materials": [
                        {
                            "title": "NCERT Chemistry Class 12 Chapter 10: Haloalkanes and Haloarenes",
                            "type": "Official Textbook Reference",
                            "url": "https://ncert.nic.in/textbook.php"
                        }
                    ],
                    "practice_question": {
                        "q": "The SN1 nucleophilic substitution reaction typically proceeds via which intermediate?",
                        "options": ["Carbocation", "Free Radical", "Carbanion", "Concerted Transition State"],
                        "answer_index": 0,
                        "explanation": "SN1 proceeds through a 2-step mechanism forming a planar sp2 carbocation intermediate."
                    }
                }
            ]
        },
        {
            "id": "c_alg_sprint",
            "track": "All",
            "title": "Algebra Mastery Sprint",
            "tag": "Math",
            "hours": 4,
            "min_class": 9,
            "concept_id": "concept_math_quad_roots",
            "description": "High-yield sprint on linear systems, quadratic roots, difference of squares, and polynomial factorization.",
            "modules": [
                {
                    "id": "mod_alg_1",
                    "title": "Module 1: Linear Equations & Transposition Rules",
                    "duration": "1.0 hr",
                    "concept_id": "concept_math_linear_eq",
                    "video_url": "https://www.youtube.com/embed/bAerID24QJ8",
                    "video_title": "Khan Academy Algebra: Solving Multi-Step Linear Equations",
                    "summary": "Solving ax + b = c with variable isolation and consistent inverse operations on both sides.",
                    "detailed_notes": [
                        "1. Balancing Principles: Whatever operation is applied to the LHS must be identically applied to the RHS.",
                        "2. Inverse Operations: Addition inverses subtraction; multiplication inverses division."
                    ],
                    "formula_note": "Principle of balance: Any operation applied to the LHS must be identically applied to the RHS.",
                    "practice_question": {
                        "q": "If 2x + 3 = 11, what is the value of x?",
                        "options": ["3", "4", "5", "7"],
                        "answer_index": 1,
                        "explanation": "2x = 11 - 3 = 8 => x = 4."
                    }
                },
                {
                    "id": "mod_alg_2",
                    "title": "Module 2: Standard Algebraic Identities & Expansions",
                    "duration": "1.2 hrs",
                    "concept_id": "concept_math_algebraic_identities",
                    "video_url": "https://www.youtube.com/embed/p1OqM3kFvJ4",
                    "video_title": "Khan Academy Algebra: Standard Polynomial Expansions & Identities",
                    "summary": "Expansion of (a+b)^2, (a-b)^2, a^2-b^2, and avoiding the freshman exponent distribution fallacy.",
                    "detailed_notes": [
                        "1. Standard Binomial Expansions: (a+b)² = a² + 2ab + b²; (a-b)² = a² - 2ab + b².",
                        "2. Difference of Squares: a² - b² = (a - b)(a + b)."
                    ],
                    "formula_note": "(a + b)^2 = a^2 + 2ab + b^2. Notice the cross-term 2ab.",
                    "practice_question": {
                        "q": "What is the standard expansion of (a + b)^2?",
                        "options": ["a^2 + b^2", "a^2 + b^2 + 2ab", "2a + 2b", "a^2 + 2ab"],
                        "answer_index": 1,
                        "explanation": "(a+b)(a+b) = a^2 + ab + ba + b^2 = a^2 + 2ab + b^2."
                    }
                },
                {
                    "id": "mod_alg_3",
                    "title": "Module 3: Quadratic Roots & Factorization",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_math_quad_roots",
                    "video_url": "https://www.youtube.com/embed/ZBalWWHYQVE",
                    "video_title": "Khan Academy Algebra: Factoring Quadratic Equations & Finding Roots",
                    "summary": "Factorization by splitting middle terms and quadratic discriminant analysis (D = b^2 - 4ac).",
                    "detailed_notes": [
                        "1. Discriminant Analysis: D = b² - 4ac. Real roots exist if D >= 0.",
                        "2. Quadratic Formula: x = (-b ± √D) / (2a)."
                    ],
                    "formula_note": "Roots: x = (-b +- sqrt(b^2 - 4ac)) / (2a). Real roots exist if D >= 0.",
                    "practice_question": {
                        "q": "The roots of the equation x^2 - 9 = 0 are:",
                        "options": ["+-2", "+-3", "+-9", "3 only"],
                        "answer_index": 1,
                        "explanation": "x^2 = 9 => x = +-3."
                    }
                }
            ]
        },
        {
            "id": "c_phys_mech",
            "track": "All",
            "title": "Physics Mechanics Core",
            "tag": "Physics",
            "hours": 5,
            "min_class": 9,
            "concept_id": "concept_phys_speed_dist",
            "description": "Foundational mechanics: Newton's laws of motion, speed-distance-acceleration graphs, and universal gravitation.",
            "modules": [
                {
                    "id": "mod_phys_1",
                    "title": "Module 1: Kinematics (v = u + at, s = ut + 0.5at^2)",
                    "duration": "1.2 hrs",
                    "concept_id": "concept_phys_speed_dist",
                    "video_url": "https://www.youtube.com/embed/ZM8ECpBuQYE",
                    "video_title": "CrashCourse Physics: Motion in a Straight Line (1D Kinematics)",
                    "summary": "Uniform and non-uniform acceleration, vector velocity vs scalar speed, and instantaneous rates of change.",
                    "detailed_notes": [
                        "1. Velocity vs Speed: Velocity is vector displacement over time; speed is scalar distance over time.",
                        "2. Kinematic Equations: v = u + at; s = ut + 0.5at²; v² = u² + 2as."
                    ],
                    "formula_note": "Kinematics: v = u + at | s = ut + 0.5*a*t^2 | v^2 = u^2 + 2as.",
                    "practice_question": {
                        "q": "If a car accelerates from rest at 2 m/s^2 for 5 seconds, what is its final speed?",
                        "options": ["7 m/s", "10 m/s", "20 m/s", "25 m/s"],
                        "answer_index": 1,
                        "explanation": "v = u + at = 0 + (2)(5) = 10 m/s."
                    }
                },
                {
                    "id": "mod_phys_2",
                    "title": "Module 2: Newton's Laws & Force Units",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_phys_force_units",
                    "video_url": "https://www.youtube.com/embed/kKKM8Y-u7ds",
                    "video_title": "CrashCourse Physics: Newton's Laws of Motion & Forces",
                    "summary": "First law of inertia, second law (F = ma = dp/dt), third law of action-reaction, and free-body force diagrams.",
                    "detailed_notes": [
                        "1. Newton's First Law: An object remains at rest or in uniform straight-line motion unless acted upon by a net external force.",
                        "2. Newton's Second Law: F_net = m * a.",
                        "3. Newton's Third Law: For every action force, there is an equal and opposite reaction force."
                    ],
                    "formula_note": "Newton's Second Law: F_net = m * a. 1 Newton = 1 kg * m/s^2.",
                    "practice_question": {
                        "q": "What is the SI unit of force?",
                        "options": ["Newton (N)", "Joule (J)", "Pascal (Pa)", "Watt (W)"],
                        "answer_index": 0,
                        "explanation": "Force is measured in Newtons (N) in SI."
                    }
                },
                {
                    "id": "mod_phys_3",
                    "title": "Module 3: Universal Gravitation",
                    "duration": "1.3 hrs",
                    "concept_id": "concept_phys_gravitation",
                    "video_url": "https://www.youtube.com/embed/TRAbTlh70rg",
                    "video_title": "Khan Academy Physics: Universal Law of Gravitation",
                    "summary": "Inverse-square gravitational attraction, planetary motion, acceleration due to gravity g, and orbital mechanics.",
                    "detailed_notes": [
                        "1. Universal Gravitation: F = G*(m1*m2)/r².",
                        "2. Inverse Square Law: Doubling r quarters the gravitational force."
                    ],
                    "formula_note": "Newton's Gravitation: F = G*(m1*m2)/r^2. G = 6.674 x 10^-11 N m^2 / kg^2.",
                    "practice_question": {
                        "q": "If distance between two masses is doubled, the gravitational force becomes:",
                        "options": ["One-fourth (1/4)", "One-half (1/2)", "Double (2x)", "Four times (4x)"],
                        "answer_index": 0,
                        "explanation": "Inverse square law: (2)^2 in denominator gives 1/4 of original force."
                    }
                }
            ]
        },
        {
            "id": "c_bio_foundations",
            "track": "All",
            "title": "Biological Systems & Genetics",
            "tag": "Biology",
            "hours": 6,
            "min_class": 9,
            "concept_id": "concept_bio_cell",
            "description": "Essential cell biology, eukaryotic organelle physiology, genetics, and cardiovascular transport systems.",
            "modules": [
                {
                    "id": "mod_bio_1",
                    "title": "Module 1: Cellular Organelles & Bioenergetics",
                    "duration": "1.5 hrs",
                    "concept_id": "concept_bio_cell",
                    "video_url": "https://www.youtube.com/embed/URUJD5NEXC8",
                    "video_title": "CrashCourse Biology: Animal Cells, Organelles & Membrane Systems",
                    "summary": "Mitochondria, ribosomes, endoplasmic reticulum, cellular respiration, and ATP synthesis pathways.",
                    "detailed_notes": [
                        "1. Eukaryotic Cells: Compartmentalized membrane-bound organelles with distinct biochemical microenvironments.",
                        "2. Mitochondria: Sites of cellular respiration, producing ATP via the electron transport chain."
                    ],
                    "formula_note": "Aerobic respiration produces ~36-38 ATP per glucose molecule via Krebs cycle and oxidative phosphorylation.",
                    "practice_question": {
                        "q": "Which organelle is recognized as the 'powerhouse of the cell'?",
                        "options": ["Mitochondria", "Ribosome", "Golgi Apparatus", "Lysosome"],
                        "answer_index": 0,
                        "explanation": "Mitochondria generate the majority of cellular ATP."
                    }
                },
                {
                    "id": "mod_bio_2",
                    "title": "Module 2: Mendelian Genetics & Inheritance",
                    "duration": "1.8 hrs",
                    "concept_id": "concept_bio_genetics",
                    "video_url": "https://www.youtube.com/embed/Mehz7tCxjSE",
                    "video_title": "Khan Academy Biology: Mendelian Genetics, Punnett Squares & Monohybrid Crosses",
                    "summary": "Dominant vs recessive alleles, monohybrid crosses (3:1 phenotypic ratio), dihybrid crosses (9:3:3:1), and chromosome segregation.",
                    "detailed_notes": [
                        "1. Law of Segregation: Two alleles for a gene separate during gamete formation.",
                        "2. Monohybrid cross (Tt x Tt) produces 3:1 phenotypic ratio and 1:2:1 genotypic ratio."
                    ],
                    "formula_note": "Monohybrid cross (Tt x Tt): 1 TT : 2 Tt : 1 tt genotypic ratio; 3 Tall : 1 Dwarf phenotypic ratio.",
                    "practice_question": {
                        "q": "In a cross between Tt and Tt, what is the expected phenotypic ratio?",
                        "options": ["3:1", "1:2:1", "9:3:3:1", "1:1"],
                        "answer_index": 0,
                        "explanation": "Phenotypic ratio of monohybrid cross is 3:1."
                    }
                }
            ]
        }
    ]

    @classmethod
    async def get_catalog_for_user(cls, student_id: str, track_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Dynamically constructs the accredited course catalog for the student's
        exact aim, grade level, and curriculum track.
        """
        profile_col = db_manager.get_collection("student_profiles")
        profile = await profile_col.find_one({"student_id": student_id})
        goal = (profile.get("goal") or "CBSE") if profile else "CBSE"
        klass = str(profile.get("klass") or "10") if profile else "10"
        weak_areas = profile.get("weak_areas", []) if profile else []

        target_track = track_filter if (track_filter and track_filter != "All") else goal
        
        # 1. Primary: Generate courses strictly aligned to this student's track & class
        generated = CurriculumEngine.generate_courses_for_student(target_track, klass, weak_areas)
        all_courses_map: Dict[str, Dict[str, Any]] = {}
        for c in generated:
            all_courses_map[c["id"]] = c

        # 2. If 'All' is chosen, also include student's primary aim courses
        if track_filter == "All" and target_track != goal:
            for c in CurriculumEngine.generate_courses_for_student(goal, klass, weak_areas):
                if c["id"] not in all_courses_map:
                    all_courses_map[c["id"]] = c

        # 3. Fallback to base catalog (include track matches and universal 'All' courses)
        for c in cls.COURSES_CATALOG:
            c_track = c.get("track", "All")
            if (track_filter == "All" or c_track == "All" or c_track.upper() == target_track.upper()):
                if c["id"] not in all_courses_map:
                    all_courses_map[c["id"]] = c

        # 4. Integrate student-uploaded study materials as custom personalized course modules
        materials_col = db_manager.get_collection("study_materials")
        student_materials = await materials_col.find({"student_id": student_id})
        for sm in student_materials:
            analysis = sm.get("analysis")
            if not isinstance(analysis, dict):
                analysis = {
                    "summary": f"Personalized learning module from your uploaded notes.",
                    "key_concepts": [sm.get("title", "Notes")],
                    "key_formulas": [],
                    "course_module": {}
                }
            cm = analysis.get("course_module") or {}
            if not isinstance(cm, dict):
                cm = {}
            mat_id = sm.get("id") or sm.get("material_id") or "doc"
            mat_course_id = f"custom_notes_{mat_id}"
            mat_title = f"{sm.get('title', 'Lecture Notes')} (Personalized Course)"
            mat_course = {
                "id": mat_course_id,
                "title": mat_title,
                "track": goal,
                "tag": sm.get("subject", "General"),
                "hours": max(1, round(analysis.get("estimated_study_minutes", 60) / 60)),
                "description": analysis.get("summary", f"Personalized learning module generated from your uploaded {sm.get('subject')} notes via AI OCR."),
                "concept_id": f"concept_custom_{sm.get('subject', 'notes').lower()}",
                "reason": "Directly adapted from your personal study notes with AI OCR",
                "fit_score": 99.0,
                "is_weakness_remedy": True,
                "modules": [
                    {
                        "id": f"mod_custom_{mat_id}",
                        "title": cm.get("title", f"Module: {sm.get('title')}"),
                        "duration": cm.get("duration", "1.0 hr"),
                        "concept_id": f"concept_custom_{sm.get('subject', 'notes').lower()}",
                        "summary": analysis.get("summary", ""),
                        "formula_note": cm.get("formula_note") or (", ".join(analysis.get("key_formulas", [])[:2]) if analysis.get("key_formulas") else "Formulas extracted via OCR"),
                        "detailed_notes": cm.get("detailed_notes") or analysis.get("key_concepts", []),
                        "pitfalls": cm.get("pitfalls", ["Always verify foundational definitions before applying formulas."]),
                        "formula_sheet": [
                            {"name": f"Formula {i+1}", "formula": f, "variables": "Governing Rule", "notes": "Extracted from your notes"}
                            for i, f in enumerate(analysis.get("key_formulas", []))
                        ],
                        "practice_question": (
                            {
                                "q": analysis["generated_questions"][0]["question"],
                                "options": analysis["generated_questions"][0]["options"],
                                "answer_index": analysis["generated_questions"][0]["correct_index"],
                                "explanation": analysis["generated_questions"][0]["explanation"]
                            }
                            if analysis.get("generated_questions") else None
                        )
                    }
                ]
            }
            if mat_course_id not in all_courses_map:
                all_courses_map[mat_course_id] = mat_course

        return list(all_courses_map.values())

    @classmethod
    async def get_free_courses_for_user(cls, student_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves authentic, accredited 100% free courses available online
        strictly calibrated to the student's exam prep goal and class level.
        """
        profile_col = db_manager.get_collection("student_profiles")
        profile = await profile_col.find_one({"student_id": student_id}) if student_id else None
        goal = (profile.get("goal") or "CBSE") if profile else "CBSE"
        klass = str(profile.get("klass") or "10") if profile else "10"
        return CurriculumEngine.get_free_external_courses(goal, klass)

    @classmethod
    async def get_course_for_user(cls, course_id: str, student_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieves course detail accurately calibrated to the student's exact
        class level and exam goal. Supports fuzzy resolution for enrolled titles
        and enrolled_X index references.
        """
        profile = None
        goal = "CBSE"
        klass = "10"
        weak_areas = []

        if student_id:
            profile_col = db_manager.get_collection("student_profiles")
            profile = await profile_col.find_one({"student_id": student_id})
            if profile:
                goal = profile.get("goal") or "CBSE"
                klass = str(profile.get("klass") or "10")
                weak_areas = profile.get("weak_areas", [])

        student_courses = CurriculumEngine.generate_courses_for_student(goal, klass, weak_areas)
        clean_id = (course_id or "").strip().lower()

        # 1. Direct ID or Title match in student's calibrated courses
        for c in student_courses:
            if c["id"].lower() == clean_id or c["title"].lower() == clean_id:
                return c

        # 1b. Check student uploaded study materials
        if student_id:
            materials_col = db_manager.get_collection("study_materials")
            mats = await materials_col.find({"student_id": student_id})
            for sm in mats:
                mat_id = sm.get("id") or sm.get("material_id") or ""
                mat_title = f"{sm.get('title', '')} (Personalized Course)".lower()
                sm_title = (sm.get("title") or "").lower()
                if clean_id in [f"custom_notes_{mat_id}".lower(), mat_id.lower(), sm_title, mat_title] or (sm_title and sm_title in clean_id):
                    analysis = sm.get("analysis", {})
                    cm = analysis.get("course_module") or {}
                    return {
                        "id": f"custom_notes_{mat_id}",
                        "title": f"{sm.get('title', 'Lecture Notes')} (Personalized Course)",
                        "track": goal,
                        "tag": sm.get("subject", "General"),
                        "hours": max(1, round(analysis.get("estimated_study_minutes", 60) / 60)),
                        "description": analysis.get("summary", ""),
                        "concept_id": f"concept_custom_{sm.get('subject', 'notes').lower()}",
                        "modules": [
                            {
                                "id": f"mod_custom_{mat_id}",
                                "title": cm.get("title", f"Module: {sm.get('title')}"),
                                "duration": cm.get("duration", "1.0 hr"),
                                "concept_id": f"concept_custom_{sm.get('subject', 'notes').lower()}",
                                "summary": analysis.get("summary", ""),
                                "formula_note": cm.get("formula_note") or (", ".join(analysis.get("key_formulas", [])[:2]) if analysis.get("key_formulas") else "Extracted formulas"),
                                "detailed_notes": cm.get("detailed_notes") or analysis.get("key_concepts", []),
                                "pitfalls": cm.get("pitfalls", ["Verify formulas before numerical application."]),
                                "formula_sheet": [
                                    {"name": f"Formula {i+1}", "formula": f, "variables": "Governing Rule", "notes": "Extracted from your notes"}
                                    for i, f in enumerate(analysis.get("key_formulas", []))
                                ],
                                "practice_question": (
                                    {
                                        "q": analysis["generated_questions"][0]["question"],
                                        "options": analysis["generated_questions"][0]["options"],
                                        "answer_index": analysis["generated_questions"][0]["correct_index"],
                                        "explanation": analysis["generated_questions"][0]["explanation"]
                                    }
                                    if analysis.get("generated_questions") else None
                                )
                            }
                        ]
                    }

        # 2. Check base catalog by ID or Title
        for c in cls.COURSES_CATALOG:
            if c["id"].lower() == clean_id or c["title"].lower() == clean_id:
                return c

        # 3. Handle enrolled_X index pointers from enrolled courses list
        if profile and clean_id.startswith("enrolled_"):
            try:
                idx = int(clean_id.replace("enrolled_", ""))
                enrolled_titles = profile.get("enrolled_courses", [])
                if 0 <= idx < len(enrolled_titles):
                    enrolled_target = enrolled_titles[idx].strip().lower()
                    # 3a. Check student's own generated courses and base catalog
                    for c in student_courses:
                        if c["title"].lower() == enrolled_target or enrolled_target in c["title"].lower() or c["title"].lower() in enrolled_target:
                            return c
                    for c in cls.COURSES_CATALOG:
                        if c["title"].lower() == enrolled_target or enrolled_target in c["title"].lower() or c["title"].lower() in enrolled_target:
                            return c

                    # 3b. Search across all goals and grades
                    for g in ["State Board", "NEET", "CBSE", "ICSE", "CUET", "JEE", "CET"]:
                        for k in ["10", "11", "12", "9", "8"]:
                            for c in CurriculumEngine.generate_courses_for_student(g, k):
                                if c["title"].lower() == enrolled_target or enrolled_target in c["title"].lower() or c["title"].lower() in enrolled_target:
                                    return c

                    # 3c. Keyword matching by subject (bio, chem, phys, math)
                    for g in ["NEET", "State Board", "CBSE", "JEE"]:
                        for c in CurriculumEngine.generate_courses_for_student(g, klass):
                            tag = c.get("tag", "").lower()
                            if tag == "biology" and any(k in enrolled_target for k in ["bio", "cell", "genet", "life"]):
                                return c
                            if tag == "chemistry" and any(k in enrolled_target for k in ["chem", "organic", "iupac"]):
                                return c
                            if tag == "math" and any(k in enrolled_target for k in ["math", "algebra", "calculus", "quad"]):
                                return c
                            if tag == "physics" and any(k in enrolled_target for k in ["phys", "motion", "force", "gravity"]):
                                return c
            except Exception:
                pass

        # 4. Partial substring or keyword matching across student courses
        for c in student_courses:
            c_title = c["title"].lower()
            c_tag = c.get("tag", "").lower()
            if clean_id in c_title or c_title in clean_id or (c_tag and c_tag in clean_id):
                return c

        # 5. Search across all curricula goals and grades
        return cls.get_course_by_id(course_id)

    @classmethod
    def get_course_by_id(cls, course_id: str) -> Optional[Dict[str, Any]]:
        clean_id = (course_id or "").strip().lower()

        # 1. Search in curriculum generated courses across all goals
        for goal in ["JEE", "NEET", "CUET", "CBSE", "ICSE", "State Board", "CET"]:
            for klass in ["11", "12", "10", "9", "8"]:
                for c in CurriculumEngine.generate_courses_for_student(goal, klass):
                    if c["id"].lower() == clean_id or c["title"].lower() == clean_id or clean_id in c["title"].lower() or c["title"].lower() in clean_id:
                        return c

        # 2. Search in base catalog
        for c in cls.COURSES_CATALOG:
            if c["id"].lower() == clean_id or c["title"].lower() == clean_id or clean_id in c["title"].lower() or c["title"].lower() in clean_id:
                return c

        # 3. Subject-keyword fallback across all generated courses
        for goal in ["NEET", "State Board", "CBSE", "JEE"]:
            for c in CurriculumEngine.generate_courses_for_student(goal, "10"):
                tag = c.get("tag", "").lower()
                if tag == "biology" and any(k in clean_id for k in ["bio", "cell", "genet"]):
                    return c
                if tag == "chemistry" and any(k in clean_id for k in ["chem", "organic"]):
                    return c
                if tag == "math" and any(k in clean_id for k in ["math", "algebra", "calc"]):
                    return c
                if tag == "physics" and any(k in clean_id for k in ["phys", "motion", "force"]):
                    return c

        return None

    @classmethod
    async def get_personalized_recommendations(cls, student_id: str) -> List[Dict[str, Any]]:
        profile_col = db_manager.get_collection("student_profiles")
        mastery_col = db_manager.get_collection("mastery_states")

        profile = await profile_col.find_one({"student_id": student_id})
        goal = (profile.get("goal") or "CBSE") if profile else "CBSE"
        klass = str(profile.get("klass") or "10") if profile else "10"
        weak_areas = [w.lower() for w in (profile.get("weak_areas", []) if profile else [])]

        mastery_records = await mastery_col.find({"student_id": student_id})
        concept_mastery_map = {m["concept_id"]: m.get("mastery", 0.5) for m in mastery_records}

        # Retrieve all candidate courses for this student
        candidates = await cls.get_catalog_for_user(student_id)

        ranked_items = []
        for c in candidates:
            score = 0.0
            reasons = []

            # Track match bonus
            if c["track"].upper() == goal.upper() or c["track"] == "All":
                score += 35.0
                reasons.append(f"Official {goal} Curriculum Alignment")

            # Weakness matching bonus
            tag_lower = c["tag"].lower()
            title_lower = c["title"].lower()
            for w in weak_areas:
                if w in tag_lower or w in title_lower or c.get("is_weakness_remedy"):
                    score += 50.0
                    reasons.append(f"🎯 Directly Remediates Diagnosed Weak Area: {w.capitalize()}")
                    break

            # Mastery gap bonus
            concept_id = c.get("concept_id")
            if concept_id in concept_mastery_map:
                m_val = concept_mastery_map[concept_id]
                if m_val < 0.60:
                    gap_score = (1.0 - m_val) * 40.0
                    score += gap_score
                    reasons.append(f"BKT Concept Mastery is currently low ({int(m_val*100)}%)")

            if not reasons:
                reasons.append(f"Foundational Module for Class {klass}")
                score += 15.0

            ranked_items.append({
                "id": c["id"],
                "title": c["title"],
                "track": c["track"],
                "tag": c["tag"],
                "hours": c["hours"],
                "reason": " • ".join(reasons),
                "concept_id": c.get("concept_id"),
                "fit_score": round(score, 1),
                "modules_count": len(c.get("modules", [])),
                "is_weakness_remedy": c.get("is_weakness_remedy", False)
            })

        ranked_items.sort(key=lambda x: x["fit_score"], reverse=True)
        return ranked_items[:8]
