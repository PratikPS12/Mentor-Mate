from typing import Dict, Any, List, Optional, Set
from collections import deque

class CurriculumKnowledgeGraph:
    """
    Curriculum Knowledge Graph & Prerequisite Directed Acyclic Graph (DAG).
    Connects concepts across classes (8-12) and boards/goals (CBSE, ICSE, State Board, JEE, NEET, CUET).
    Enables root-cause diagnosis of prerequisite deficits.
    """

    CONCEPTS_REGISTRY: Dict[str, Dict[str, Any]] = {
        # Mathematics Graph
        "math_linear_eq": {
            "id": "math_linear_eq",
            "name": "Linear Equations & Single Variable Algebra",
            "subject": "Mathematics",
            "chapter": "Algebra Foundations",
            "grade": "8-9",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.3,
            "prerequisites": [],
            "learning_objectives": ["Isolate unknown variables", "Preserve equation invariants"]
        },
        "math_poly_factor": {
            "id": "math_poly_factor",
            "name": "Polynomial Factorization & Identities",
            "subject": "Mathematics",
            "chapter": "Polynomials",
            "grade": "9-10",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.45,
            "prerequisites": ["math_linear_eq"],
            "learning_objectives": ["Factorize quadratics by splitting middle term", "Apply algebraic identities"]
        },
        "concept_math_quad_roots": {
            "id": "concept_math_quad_roots",
            "name": "Roots of Quadratic Equations & Discriminant Analysis",
            "subject": "Mathematics",
            "chapter": "Quadratic Equations",
            "grade": "10-11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.6,
            "prerequisites": ["math_poly_factor"],
            "learning_objectives": ["Apply quadratic formula", "Analyze discriminant b^2 - 4ac for real/complex roots"]
        },
        "math_functions_limits": {
            "id": "math_functions_limits",
            "name": "Functions, Domain-Range, and Intuitive Limits",
            "subject": "Mathematics",
            "chapter": "Calculus Foundations",
            "grade": "11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.7,
            "prerequisites": ["concept_math_quad_roots"],
            "learning_objectives": ["Evaluate function limits", "Handle indeterminate forms"]
        },
        "math_differential_calc": {
            "id": "math_differential_calc",
            "name": "Differentiation, Chain Rule & Rate of Change",
            "subject": "Mathematics",
            "chapter": "Differential Calculus",
            "grade": "11-12",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.85,
            "prerequisites": ["math_functions_limits"],
            "learning_objectives": ["Apply chain, product, and quotient rules", "Compute tangents and extrema"]
        },
        "math_matrices_determinants": {
            "id": "math_matrices_determinants",
            "name": "Matrices, Determinants & Linear Systems",
            "subject": "Mathematics",
            "chapter": "Linear Algebra & Matrices",
            "grade": "11-12",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "CUET"],
            "difficulty": 0.65,
            "prerequisites": ["math_linear_eq"],
            "learning_objectives": ["Matrix multiplication & inversion", "Evaluate 2x2 and 3x3 determinants", "Solve linear systems via Cramer's rule"]
        },

        # Physics Graph
        "phys_vectors": {
            "id": "phys_vectors",
            "name": "Vectors & Coordinate Resolution",
            "subject": "Physics",
            "chapter": "Mathematical Tools",
            "grade": "11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.4,
            "prerequisites": [],
            "learning_objectives": ["Vector addition and scalar product", "Resolving vectors into orthogonal components"]
        },
        "phys_kinematics_1d": {
            "id": "phys_kinematics_1d",
            "name": "Kinematics & Equations of Uniform Acceleration",
            "subject": "Physics",
            "chapter": "Motion in a Straight Line",
            "grade": "9-11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.5,
            "prerequisites": ["phys_vectors"],
            "learning_objectives": ["Apply v = u + at, s = ut + 0.5at^2", "Interpret displacement-time graphs"]
        },
        "concept_phys_force_units": {
            "id": "concept_phys_force_units",
            "name": "Newton's Laws of Motion & Free Body Dynamics",
            "subject": "Physics",
            "chapter": "Laws of Motion",
            "grade": "9-11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.65,
            "prerequisites": ["phys_kinematics_1d"],
            "learning_objectives": ["Draw free-body diagrams", "Solve multi-body connected systems"]
        },
        "phys_rotational_dynamics": {
            "id": "phys_rotational_dynamics",
            "name": "Rotational Motion, Torque & Moment of Inertia",
            "subject": "Physics",
            "chapter": "System of Particles & Rotational Motion",
            "grade": "11",
            "goals": ["CBSE", "JEE", "NEET"],
            "difficulty": 0.9,
            "prerequisites": ["concept_phys_force_units", "phys_vectors"],
            "learning_objectives": ["Calculate torque tau = r x F", "Apply conservation of angular momentum"]
        },

        # Chemistry Graph
        "chem_atomic_structure": {
            "id": "chem_atomic_structure",
            "name": "Bohr Model, Quantum Numbers & Electronic Configuration",
            "subject": "Chemistry",
            "chapter": "Structure of Atom",
            "grade": "9-11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.45,
            "prerequisites": [],
            "learning_objectives": ["Write electronic configurations", "Understand valence orbitals"]
        },
        "chem_chemical_bonding": {
            "id": "chem_chemical_bonding",
            "name": "Covalent Bonding, VSEPR & Hybridization",
            "subject": "Chemistry",
            "chapter": "Chemical Bonding",
            "grade": "10-11",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.6,
            "prerequisites": ["chem_atomic_structure"],
            "learning_objectives": ["Predict molecular geometry", "Determine sp/sp2/sp3 hybridization"]
        },
        "concept_chem_iupac": {
            "id": "concept_chem_iupac",
            "name": "IUPAC Nomenclature & Organic Reaction Mechanisms",
            "subject": "Chemistry",
            "chapter": "Organic Chemistry Fundamentals",
            "grade": "10-12",
            "goals": ["CBSE", "ICSE", "State Board", "JEE", "NEET"],
            "difficulty": 0.75,
            "prerequisites": ["chem_chemical_bonding"],
            "learning_objectives": ["Systematic IUPAC naming", "Differentiate SN1 vs SN2 nucleophilic mechanisms"]
        },

        # Biology Graph
        "concept_bio_cell": {
            "id": "concept_bio_cell",
            "name": "Cellular Structure, Organelles & Membrane Transport",
            "subject": "Biology",
            "chapter": "Cell: The Unit of Life",
            "grade": "9-11",
            "goals": ["CBSE", "ICSE", "State Board", "NEET", "CUET"],
            "difficulty": 0.5,
            "prerequisites": [],
            "learning_objectives": ["Identify organelle functions", "Understand active vs passive transport"]
        },
        "bio_genetics_mendel": {
            "id": "bio_genetics_mendel",
            "name": "Mendelian Genetics, Linkage & Chromosomal Inheritance",
            "subject": "Biology",
            "chapter": "Principles of Inheritance",
            "grade": "10-12",
            "goals": ["CBSE", "ICSE", "State Board", "NEET", "CUET"],
            "difficulty": 0.8,
            "prerequisites": ["concept_bio_cell"],
            "learning_objectives": ["Calculate monohybrid & dihybrid ratios", "Identify autosomal vs sex-linked conditions"]
        }
    }

    @classmethod
    def get_concept(cls, concept_id: str) -> Optional[Dict[str, Any]]:
        return cls.CONCEPTS_REGISTRY.get(concept_id)

    @classmethod
    def get_all_prerequisites(cls, concept_id: str) -> List[str]:
        """
        Traverses DAG backwards to find all direct and indirect prerequisites.
        """
        prereqs: Set[str] = set()
        queue = deque([concept_id])
        visited: Set[str] = set()

        while queue:
            curr = queue.popleft()
            if curr in visited:
                continue
            visited.add(curr)

            concept = cls.CONCEPTS_REGISTRY.get(curr)
            if concept:
                for p in concept.get("prerequisites", []):
                    prereqs.add(p)
                    queue.append(p)

        return list(prereqs)

    @classmethod
    def diagnose_root_cause(
        cls,
        failed_concept_id: str,
        student_masteries: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Inspects prerequisite chain. If an earlier prerequisite has mastery < 0.60,
        classifies error as 'prerequisite_gap' pointing to the foundational concept.
        """
        prereqs = cls.get_all_prerequisites(failed_concept_id)
        for p_id in prereqs:
            mastery = student_masteries.get(p_id, 0.5)
            if mastery < 0.60:
                p_concept = cls.CONCEPTS_REGISTRY.get(p_id)
                return {
                    "error_type": "prerequisite_gap",
                    "root_concept_id": p_id,
                    "root_concept_name": p_concept["name"] if p_concept else p_id,
                    "root_mastery": mastery,
                    "explanation": f"Struggle in '{cls.CONCEPTS_REGISTRY.get(failed_concept_id, {}).get('name')}' is rooted in unmastered prerequisite: '{p_concept['name'] if p_concept else p_id}'."
                }

        target_concept = cls.CONCEPTS_REGISTRY.get(failed_concept_id)
        return {
            "error_type": "knowledge_gap",
            "root_concept_id": failed_concept_id,
            "root_concept_name": target_concept["name"] if target_concept else failed_concept_id,
            "root_mastery": student_masteries.get(failed_concept_id, 0.4),
            "explanation": f"Direct conceptual gap in '{target_concept['name'] if target_concept else failed_concept_id}'."
        }
