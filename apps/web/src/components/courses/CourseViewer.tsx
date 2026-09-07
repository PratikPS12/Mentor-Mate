"use client";

import React, { useState } from "react";
import { CourseItem, CourseModule, FormulaItem, WorkedExample, StudyResource } from "@/lib/api";

interface CourseViewerProps {
  course: CourseItem;
  onBack: () => void;
  onNavigateTab: (tabKey: string) => void;
}

type ModuleTab = "notes" | "video" | "formulas" | "examples" | "pitfalls" | "materials" | "quiz";

function getSubjectCalibratedModules(course: CourseItem): CourseModule[] {
  if (course.modules && course.modules.length > 0) {
    return course.modules;
  }

  const tag = (course.tag || "").toLowerCase();
  const title = (course.title || "").toLowerCase();

  // 1. Biology Course Fallback
  if (tag.includes("bio") || title.includes("bio") || title.includes("cell") || title.includes("genet") || title.includes("life")) {
    return [
      {
        id: "mod_bio_fallback_1",
        title: "Module 1: Cellular Architecture & Bioenergetics",
        duration: "1.5 hrs",
        concept_id: "concept_bio_cell",
        video_url: "https://www.youtube.com/embed/URUJD5NEXC8",
        video_title: "CrashCourse Biology: Cell Structure, Organelles & Membrane Transport",
        summary: `Comprehensive cellular organization, organelle specializations, and mitochondrial ATP synthesis for ${course.title}.`,
        detailed_notes: [
          "1. Eukaryotic vs Prokaryotic Organization: Eukaryotes feature membrane-bound organelles and a defined nucleus containing linear DNA wrapped around histone octamers. Prokaryotes lack membrane-bound organelles and possess a naked circular nucleoid.",
          "2. Fluid Mosaic Model: Cell membrane is composed of an amphipathic phospholipid bilayer with hydrophobic interior fatty acid tails and polar phosphate head groups with integrated transport proteins.",
          "3. Mitochondria & Bioenergetics: The powerhouse of the cell. Double-membrane organelle with folded cristae housing ATP Synthase complexes (F0-F1 particles) producing 36-38 ATP per glucose molecule."
        ],
        formula_note: "Respiration: C6H12O6 + 6O2 -> 6CO2 + 6H2O + 36-38 ATP synthesized via mitochondria.",
        formula_sheet: [
          {
            name: "Aerobic Cellular Respiration",
            formula: "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + 36–38 ATP",
            variables: "Glucose + Oxygen yields Carbon Dioxide + Water + Energy",
            notes: "Glycolysis (Cytoplasm) → Krebs Cycle (Mitochondrial Matrix) → ETC (Inner Membrane Cristae)."
          }
        ],
        worked_examples: [
          {
            problem: "Where is ATP synthase located in eukaryotic animal and plant cells during aerobic respiration?",
            solution_steps: [
              "Step 1: Oxidative phosphorylation depends on a proton gradient generated across the inner mitochondrial membrane.",
              "Step 2: ATP Synthase (F0-F1 particles) are embedded in the inner mitochondrial membrane (cristae).",
              "Step 3: Protons flow back into the mitochondrial matrix through ATP synthase, generating ATP."
            ],
            key_insight: "In mitochondria ATP synthase is in the inner membrane cristae; in chloroplasts it is in the thylakoid membrane."
          }
        ],
        pitfalls: [
          "Do NOT classify mitochondria or chloroplasts as part of the endomembrane system.",
          "Ribosomes are non-membrane bound structures found in both prokaryotes (70S) and eukaryotes (80S)."
        ],
        study_materials: [
          {
            title: "NCERT Biology Class 11 Chapter 8: Cell — The Unit of Life",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "Which cellular organelle synthesizes ATP via oxidative phosphorylation?",
          options: ["Mitochondria", "Ribosome", "Golgi apparatus", "Lysosome"],
          answer_index: 0,
          explanation: "Mitochondria generate ATP across the inner mitochondrial membrane during oxidative phosphorylation."
        }
      },
      {
        id: "mod_bio_fallback_2",
        title: "Module 2: Principles of Mendelian Genetics & Molecular Inheritance",
        duration: "1.6 hrs",
        concept_id: "concept_bio_genetics",
        video_url: "https://www.youtube.com/embed/Mehz7tCxjSE",
        video_title: "Khan Academy Biology: Mendelian Genetics, Monohybrid Crosses & Punnett Squares",
        summary: "Monohybrid and dihybrid crosses, Law of Segregation, Law of Independent Assortment, and Punnett square probability.",
        detailed_notes: [
          "1. Law of Segregation (Mendel's 1st Law): Allele pairs separate during gametogenesis so that each gamete carries only one allele for each gene locus.",
          "2. Law of Independent Assortment (Mendel's 2nd Law): Genes on non-homologous chromosomes assort independently into gametes.",
          "3. Standard Ratios: Monohybrid F2 phenotypic ratio = 3:1 (genotypic 1:2:1). Dihybrid F2 phenotypic ratio = 9:3:3:1."
        ],
        formula_note: "Monohybrid F2 Phenotypic Ratio = 3 Dominant : 1 Recessive. Dihybrid F2 = 9:3:3:1.",
        formula_sheet: [
          {
            name: "Mendelian Cross Ratios",
            formula: "Monohybrid: 3:1 | Dihybrid: 9:3:3:1",
            variables: "F1 Heterozygote selfing (Tt × Tt)",
            notes: "Assumes independent assortment without genetic linkage."
          }
        ],
        worked_examples: [
          {
            problem: "In a monohybrid cross between two heterozygous tall pea plants (Tt x Tt), what percentage of offspring are heterozygous tall?",
            solution_steps: [
              "Step 1: Possible genotypes from Tt x Tt are 1 TT : 2 Tt : 1 tt.",
              "Step 2: Heterozygous tall offspring are Tt.",
              "Step 3: Proportion is 2 out of 4 = 50%."
            ],
            key_insight: "Do not confuse proportion of ALL offspring (2/4 = 50%) with proportion of TALL offspring (2/3 = 66.7%)."
          }
        ],
        pitfalls: [
          "Linkage violates independent assortment if genes are close together on the same chromosome."
        ],
        study_materials: [
          {
            title: "NCERT Biology Class 12 Chapter 5: Principles of Inheritance and Variation",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "What is the expected phenotypic ratio in a standard Mendelian monohybrid cross (Tt x Tt)?",
          options: ["3 : 1", "1 : 2 : 1", "9 : 3 : 3 : 1", "1 : 1"],
          answer_index: 0,
          explanation: "Dominant to recessive phenotype ratio is 3:1."
        }
      }
    ];
  }

  // 2. Chemistry Course Fallback
  if (tag.includes("chem") || title.includes("chem") || title.includes("organic") || title.includes("iupac") || title.includes("aromatic")) {
    return [
      {
        id: "mod_chem_fallback_1",
        title: "Module 1: IUPAC Nomenclature of Functional Carbon Chains",
        duration: "1.4 hrs",
        concept_id: "concept_chem_iupac",
        video_url: "https://www.youtube.com/embed/cExhtwVT1v0",
        video_title: "Khan Academy Organic Chemistry: IUPAC Nomenclature of Functional Carbon Compounds",
        summary: `Systematic nomenclature rules, functional group hierarchy, and lowest locant numbering for ${course.title}.`,
        detailed_notes: [
          "1. IUPAC Framework: Prefix (substituents) + Root Word (longest continuous carbon chain) + Primary Suffix (saturation: -ane, -ene, -yne) + Secondary Suffix (principal functional group).",
          "2. Priority Sequence: -COOH > -SO3H > -COOR > -CONH2 > -CN > -CHO > -CO- > -OH > -NH2. The highest priority group dictates the suffix.",
          "3. Lowest Locant Rule: Number the parent chain to give the principal functional group the lowest number."
        ],
        formula_note: "Priority: -COOH > -SO3H > -COOR > -CONH2 > -CN > -CHO > -CO- > -OH > -NH2.",
        formula_sheet: [
          {
            name: "IUPAC Functional Priority",
            formula: "-COOH > -SO₃H > -COOR > -CONH₂ > -CN > -CHO > -CO- > -OH > -NH₂",
            variables: "Principal group determines parent suffix; lower groups become prefix substituents",
            notes: "Alkyl and halo groups are always substituent prefixes."
          }
        ],
        worked_examples: [
          {
            problem: "Name CH3-CH(OH)-CH2-CH3 using IUPAC rules.",
            solution_steps: [
              "Step 1: Longest chain has 4 carbons => 'butan-'.",
              "Step 2: Functional group is alcohol (-OH) => suffix '-ol'.",
              "Step 3: Number from left to give -OH the lowest locant: C2.",
              "Step 4: Combine: Butan-2-ol."
            ],
            key_insight: "Always check numbering in both directions to verify lowest locant on principal functional group."
          }
        ],
        pitfalls: [
          "Do not assume the longest continuous chain is always horizontal.",
          "Prefixes like di-, tri- are ignored when alphabetizing substituents."
        ],
        study_materials: [
          {
            title: "NCERT Chemistry Class 11 Chapter 12: Organic Chemistry Basics",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "What is the systematic IUPAC name for CH3-CH2-CH2-OH?",
          options: ["Propan-1-ol", "Ethanol", "Propan-2-ol", "Butanol"],
          answer_index: 0,
          explanation: "3-carbon parent chain with terminal -OH is Propan-1-ol."
        }
      },
      {
        id: "mod_chem_fallback_2",
        title: "Module 2: Aromatic Systems & Hückel's (4n+2) Criteria",
        duration: "1.5 hrs",
        concept_id: "concept_chem_aromatic",
        video_url: "https://www.youtube.com/embed/oDigu9YxXUg",
        video_title: "Khan Academy Organic Chemistry: Aromaticity, Benzene & Hückel's (4n+2) Rule",
        summary: "Mandatory conditions for aromatic stability: cyclic, planar, completely conjugated ring with (4n + 2) pi electrons.",
        detailed_notes: [
          "1. 4 Criteria for Aromaticity: (a) Cyclic, (b) Fully conjugated with continuous p-orbitals, (c) Geometrically planar, and (d) (4n + 2) delocalized pi electrons.",
          "2. Anti-aromaticity: Planar, cyclic, conjugated systems with 4n pi electrons (4, 8, 12) are exceptionally unstable.",
          "3. Benzene: 6 pi electrons (n=1) exhibits ~150 kJ/mol resonance energy, favoring substitution over addition."
        ],
        formula_note: "Hückel's Rule: Pi electrons = 4n + 2 (n = 0, 1, 2, 3...) for aromatic systems.",
        formula_sheet: [
          {
            name: "Hückel's Electron Count",
            formula: "Pi Electrons = 4n + 2 (where n = 0, 1, 2, 3...)",
            variables: "n = 0 (2 pi e⁻), n = 1 (6 pi e⁻: Benzene), n = 2 (10 pi e⁻: Naphthalene)",
            notes: "Applies strictly to planar, cyclic, conjugated ring systems."
          }
        ],
        worked_examples: [
          {
            problem: "Is Benzene (C6H6) aromatic?",
            solution_steps: [
              "Step 1: Benzene is a 6-membered planar ring.",
              "Step 2: All 6 carbons are sp2 hybridized, providing continuous p-orbitals.",
              "Step 3: 3 pi bonds provide 6 pi electrons. 4n + 2 = 6 => n = 1 (integer).",
              "Step 4: Conclusion: Benzene is aromatic."
            ],
            key_insight: "Resonance energy stabilizes benzene against standard electrophilic addition."
          }
        ],
        pitfalls: [
          "Non-planar rings (like cyclooctatetraene in tub shape) are non-aromatic, not anti-aromatic."
        ],
        study_materials: [
          {
            title: "NCERT Chemistry Class 11 Chapter 13: Hydrocarbons",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "Benzene (C6H6) is classified as:",
          options: ["Alkane", "Alkene", "Aromatic", "Cycloalkane"],
          answer_index: 2,
          explanation: "Benzene possesses 6 delocalized pi electrons (n=1) in a planar cyclic ring, making it aromatic."
        }
      }
    ];
  }

  // 3. Math Course Fallback
  if (tag.includes("math") || title.includes("math") || title.includes("alg") || title.includes("calc") || title.includes("quad")) {
    return [
      {
        id: "mod_math_fallback_1",
        title: "Module 1: Quadratic Equations, Discriminant & Factorization",
        duration: "1.4 hrs",
        concept_id: "concept_math_quad_roots",
        video_url: "https://www.youtube.com/embed/ZBalWWHYQVE",
        video_title: "Khan Academy Algebra: Factoring Quadratic Equations & Quadratic Formula",
        summary: `Standard quadratic form ax^2 + bx + c = 0, discriminant root character, and Vieta formulas for ${course.title}.`,
        detailed_notes: [
          "1. Standard Quadratic Equation: ax² + bx + c = 0 (a ≠ 0). Universal quadratic formula: x = (-b ± √(b² - 4ac)) / (2a).",
          "2. Discriminant Analysis (D = b² - 4ac): D > 0 (two distinct real roots), D = 0 (one repeated real root), D < 0 (conjugate complex roots).",
          "3. Vieta's Relations: Sum of roots α + β = -b/a. Product of roots α * β = c/a."
        ],
        formula_note: "Quadratic Formula: x = (-b +- sqrt(D)) / (2a), where D = b^2 - 4ac.",
        formula_sheet: [
          {
            name: "Universal Quadratic Formula",
            formula: "x = (-b ± √(b² - 4ac)) / (2a)",
            variables: "a = quadratic coefficient (≠0), b = linear coefficient, c = constant term",
            notes: "Roots are real and rational if D is a perfect square."
          }
        ],
        worked_examples: [
          {
            problem: "Find the roots of x² - 5x + 6 = 0.",
            solution_steps: [
              "Step 1: Seek two numbers whose product is 6 and sum is -5. These are -2 and -3.",
              "Step 2: Factor: (x - 2)(x - 3) = 0 => x = 2 or x = 3.",
              "Step 3: Check discriminant: D = (-5)² - 4(1)(6) = 25 - 24 = 1 > 0 (two distinct real roots)."
            ],
            key_insight: "Factoring is faster when integer roots exist; the quadratic formula is bulletproof for all coefficients."
          }
        ],
        pitfalls: [
          "Never divide both sides by x in equations like x² = 5x; doing so illegally destroys the root x = 0."
        ],
        study_materials: [
          {
            title: "NCERT Mathematics Class 10 Chapter 4: Quadratic Equations",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "What are the roots of x^2 - 5x + 6 = 0?",
          options: ["x = 2, 3", "x = -2, -3", "x = 1, 6", "x = -1, -6"],
          answer_index: 0,
          explanation: "(x-2)(x-3) = 0 yields x = 2 and x = 3."
        }
      },
      {
        id: "mod_math_fallback_2",
        title: "Module 2: Differential Calculus, Limits & Power Rules",
        duration: "1.7 hrs",
        concept_id: "concept_math_limits_derivatives",
        video_url: "https://www.youtube.com/embed/WUvTyaaNkzM",
        video_title: "3Blue1Brown: The Essence of Calculus — Derivative Intuition & Power Rule",
        summary: "Geometric interpretation of derivatives, instantaneous slope, power rule d/dx[x^n] = n*x^(n-1), and product rule.",
        detailed_notes: [
          "1. Limit Definition of Derivative: f'(x) = lim_{h->0} [f(x + h) - f(x)] / h. Measures instantaneous rate of change.",
          "2. Power Rule: d/dx [xⁿ] = n * xⁿ⁻¹. Example: d/dx [x³] = 3x².",
          "3. Product Rule: d/dx [u * v] = u'v + uv'."
        ],
        formula_note: "Power Rule: d/dx[x^n] = n*x^(n-1). Product Rule: d/dx[uv] = u'v + uv'.",
        formula_sheet: [
          {
            name: "Power Rule of Differentiation",
            formula: "d/dx [xⁿ] = n * xⁿ⁻¹",
            variables: "n = any real exponent",
            notes: "Special cases: d/dx[x] = 1, d/dx[c] = 0 (constant)."
          }
        ],
        worked_examples: [
          {
            problem: "Find the derivative of f(x) = x³ - 4x + 7.",
            solution_steps: [
              "Step 1: d/dx [x³] = 3x².",
              "Step 2: d/dx [-4x] = -4.",
              "Step 3: d/dx [7] = 0.",
              "Step 4: Combine: f'(x) = 3x² - 4."
            ],
            key_insight: "Derivative of any constant is zero."
          }
        ],
        pitfalls: [
          "d/dx[u * v] is NOT u' * v'. You must use the product rule u'v + uv'."
        ],
        study_materials: [
          {
            title: "NCERT Mathematics Class 11 Chapter 13: Limits and Derivatives",
            type: "Official NCERT Chapter",
            url: "https://ncert.nic.in/textbook.php"
          }
        ],
        practice_question: {
          q: "What is the derivative of x^3 - 4x + 7?",
          options: ["3x^2 - 4", "3x^2 - 4x", "x^2 - 4", "3x^2 + 7"],
          answer_index: 0,
          explanation: "d/dx(x^3) = 3x^2, d/dx(-4x) = -4, d/dx(7) = 0."
        }
      }
    ];
  }

  // 4. Default: Physics Course Fallback
  return [
    {
      id: "mod_phys_fallback_1",
      title: "Module 1: Kinematics & Rectilinear Motion in One Dimension",
      duration: "1.5 hrs",
      concept_id: "concept_phys_speed_dist",
      video_url: "https://www.youtube.com/embed/ZM8ECpBuQYE",
      video_title: "CrashCourse Physics: Motion in a Straight Line & Kinematics",
      summary: `Position, displacement, velocity-time relations, and uniform acceleration kinematics for ${course.title}.`,
      detailed_notes: [
        "1. Fundamentals of Rectilinear Motion: Straight-line motion defined by displacement, instantaneous velocity v = dx/dt, and acceleration a = dv/dt.",
        "2. The Three Kinematic Equations: (1) v = u + at, (2) s = ut + 0.5at², (3) v² = u² + 2as. Valid strictly under uniform acceleration.",
        "3. Graphical Analysis: Slope of position-time graph = velocity. Slope of v-t graph = acceleration. Area under v-t curve = displacement."
      ],
      formula_note: "Kinematic Equations: 1) v = u + at, 2) s = ut + 0.5at^2, 3) v^2 = u^2 + 2as.",
      formula_sheet: [
        {
          name: "Kinematic Equations (Uniform Acceleration)",
          formula: "v = u + at  |  s = ut + (1/2)at²  |  v² = u² + 2as",
          variables: "u = initial velocity, v = final velocity, a = acceleration, s = displacement, t = time",
          notes: "Strictly applicable when acceleration is constant."
        }
      ],
      worked_examples: [
        {
          problem: "A car accelerates from rest at 3 m/s² for 8 s. Calculate distance traveled.",
          solution_steps: [
            "Step 1: Given: u = 0, a = 3 m/s², t = 8 s.",
            "Step 2: Use s = ut + 0.5at².",
            "Step 3: s = 0*(8) + 0.5*(3)*(8)² = 0.5 * 3 * 64 = 96 meters."
          ],
          key_insight: "Starting from rest eliminates the 'ut' term."
        }
      ],
      pitfalls: [
        "Never apply v = u + at if acceleration is variable.",
        "Displacement is a vector; distance is a scalar total path."
      ],
      study_materials: [
        {
          title: "NCERT Physics Class 11 Chapter 3: Motion in a Straight Line",
          type: "Official NCERT Chapter",
          url: "https://ncert.nic.in/textbook.php"
        }
      ],
      practice_question: {
        q: "A vehicle starts from rest with acceleration a = 4 m/s^2. Its velocity after 5 seconds is:",
        options: ["20 m/s", "10 m/s", "40 m/s", "25 m/s"],
        answer_index: 0,
        explanation: "v = u + at = 0 + (4)(5) = 20 m/s."
      }
    },
    {
      id: "mod_phys_fallback_2",
      title: "Module 2: Universal Gravitation & Inverse Square Laws",
      duration: "1.8 hrs",
      concept_id: "concept_phys_gravitation",
      video_url: "https://www.youtube.com/embed/TRAbTlh70rg",
      video_title: "Khan Academy Physics: Newton's Law of Universal Gravitation",
      summary: "Newtonian universal gravitation, gravitational fields, surface acceleration g = GM/R^2, and orbital motion.",
      detailed_notes: [
        "1. Universal Gravitation Law: F = G*(m1*m2)/r². Inverse square law dictates doubling distance quarters gravitational force.",
        "2. Surface Gravity: g = G*M / R². On Earth's surface g ≈ 9.8 m/s².",
        "3. Orbital Velocity: v_orbit = √(G*M / r)."
      ],
      formula_note: "Newton's Gravitation: F = G*(m1*m2)/r^2.",
      formula_sheet: [
        {
          name: "Universal Law of Gravitation",
          formula: "F = G * (m₁ * m₂) / r²",
          variables: "G = 6.674×10⁻¹¹ N·m²/kg², m₁, m₂ = interacting point masses, r = center-to-center distance",
          notes: "Universal inverse-square attraction force."
        }
      ],
      worked_examples: [
        {
          problem: "If distance between two masses is doubled, how does the gravitational force change?",
          solution_steps: [
            "Step 1: F is proportional to 1/r².",
            "Step 2: New distance is 2r, so new force is proportional to 1/(2r)² = 1/(4r²).",
            "Step 3: The gravitational attraction reduces to 1/4th of its original value."
          ],
          key_insight: "Inverse square dependency causes rapid falloff with separation distance."
        }
      ],
      pitfalls: [
        "r is measured center-to-center, NOT surface-to-surface."
      ],
      study_materials: [
        {
          title: "NCERT Physics Class 11 Chapter 8: Gravitation",
          type: "Official NCERT Chapter",
          url: "https://ncert.nic.in/textbook.php"
        }
      ],
      practice_question: {
        q: "If distance between two celestial bodies is doubled, gravitational force becomes:",
        options: ["One-fourth (1/4)", "One-half (1/2)", "Double (2x)", "Four times (4x)"],
        answer_index: 0,
        explanation: "F is proportional to 1/r^2. Doubling distance makes the force 1/4."
      }
    }
  ];
}

export default function CourseViewer({ course, onBack, onNavigateTab }: CourseViewerProps) {
  const modules: CourseModule[] = getSubjectCalibratedModules(course);

  const [selectedModuleIndex, setSelectedModuleIndex] = useState(0);
  const [activeTab, setActiveTab] = useState<ModuleTab>("notes");
  const [completedModules, setCompletedModules] = useState<string[]>([]);
  const [selectedOpt, setSelectedOpt] = useState<number | null>(null);
  const [quizFeedback, setQuizFeedback] = useState<{ isCorrect: boolean; text: string } | null>(null);

  const curModule = modules[selectedModuleIndex] || modules[0];
  const progressPercent = Math.round((completedModules.length / modules.length) * 100);

  // Subject-calibrated video resolution to strictly prevent cross-subject mismatches
  const resolvedVideo = (() => {
    const tag = (course.tag || "").toLowerCase();
    const title = (course.title + " " + curModule.title).toLowerCase();

    const isNonPhysicsCourse = (
      tag.includes("bio") || tag.includes("chem") || tag.includes("math") || tag.includes("aptitude") ||
      title.includes("bio") || title.includes("chem") || title.includes("organic") || title.includes("math") || title.includes("algebra") || title.includes("calculus") || title.includes("cell") || title.includes("genetics")
    );

    // If curModule has a video_url, verify it is NOT a physics video in a non-physics course
    if (curModule.video_url && curModule.video_url.trim().length > 0) {
      const isPhysicsVideo = curModule.video_url.includes("ZM8ECpBuQYE");
      if (!(isPhysicsVideo && isNonPhysicsCourse)) {
        return {
          url: curModule.video_url,
          title: curModule.video_title || `${curModule.title} Video Lecture`
        };
      }
    }

    // Strict subject-calibrated resolution
    if (tag.includes("chem") || title.includes("chem") || title.includes("organic") || title.includes("iupac") || title.includes("aromatic")) {
      return {
        url: "https://www.youtube.com/embed/cExhtwVT1v0",
        title: "Khan Academy Organic Chemistry: IUPAC Nomenclature of Functional Carbon Compounds"
      };
    }
    if (tag.includes("bio") || title.includes("bio") || title.includes("cell") || title.includes("genet") || title.includes("life")) {
      return {
        url: "https://www.youtube.com/embed/URUJD5NEXC8",
        title: "CrashCourse Biology: Animal Cells, Organelles & Membrane Systems"
      };
    }
    if (tag.includes("math") || title.includes("math") || title.includes("alg") || title.includes("calc") || title.includes("quad") || title.includes("geometry")) {
      return {
        url: "https://www.youtube.com/embed/ZBalWWHYQVE",
        title: "Khan Academy Algebra: Factoring Quadratic Equations & Quadratic Formula"
      };
    }
    if (tag.includes("aptitude") || title.includes("aptitude") || title.includes("reasoning")) {
      return {
        url: "https://www.youtube.com/embed/3gLzHlVqJ_U",
        title: "Logical Reasoning: Syllogisms, Venn Diagrams & Statement Deductions"
      };
    }
    return {
      url: "https://www.youtube.com/embed/ZM8ECpBuQYE",
      title: "CrashCourse Physics: Motion in a Straight Line & Kinematics"
    };
  })();

  const handleCheckAnswer = () => {
    if (selectedOpt === null || !curModule.practice_question) {
      alert("Please choose an answer option first.");
      return;
    }

    const isCorrect = selectedOpt === curModule.practice_question.answer_index;
    if (isCorrect) {
      setQuizFeedback({
        isCorrect: true,
        text: `✓ Correct! ${curModule.practice_question.explanation}`,
      });
      if (!completedModules.includes(curModule.id)) {
        setCompletedModules([...completedModules, curModule.id]);
      }
    } else {
      setQuizFeedback({
        isCorrect: false,
        text: `✗ Incorrect. ${curModule.practice_question.explanation}`,
      });
    }
  };

  const handleNextModule = () => {
    if (selectedModuleIndex < modules.length - 1) {
      setSelectedModuleIndex(selectedModuleIndex + 1);
      setSelectedOpt(null);
      setQuizFeedback(null);
      setActiveTab("notes");
    }
  };

  return (
    <div className="card" style={{ padding: "24px", borderRadius: "16px", background: "#ffffff", boxShadow: "0 4px 20px rgba(0,0,0,0.06)" }}>
      {/* Top Header & Navigation */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <button className="btn secondary small" onClick={onBack} type="button">
          ← Back to All Courses
        </button>
        <span className="badge" style={{ color: "#0284c7", borderColor: "#0284c7", background: "rgba(2, 132, 199, 0.08)", fontWeight: 700 }}>
          {course.tag} • {course.track} Track • ~{course.hours} Hours
        </span>
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "16px", marginBottom: "16px" }}>
        <div style={{ maxWidth: "700px" }}>
          <h1 style={{ margin: "0 0 6px 0", fontSize: "23px", fontWeight: 800, color: "var(--text-heading)" }}>
            {course.title}
          </h1>
          <p style={{ margin: 0, fontSize: "14px", lineHeight: "1.5", color: "var(--muted)" }}>
            {course.description || "Interactive curriculum course systematically aligned with official syllabus standards."}
          </p>
        </div>
        <div style={{ minWidth: "200px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12.5px", marginBottom: "6px" }}>
            <span style={{ fontWeight: 700, color: "var(--muted)" }}>Course Completion</span>
            <span style={{ fontWeight: 800, color: "var(--accent)" }}>{progressPercent}%</span>
          </div>
          <div className="progress" style={{ height: "8px", background: "var(--border)", borderRadius: "999px", overflow: "hidden" }}>
            <div style={{ width: `${progressPercent}%`, height: "100%", background: "var(--accent)", transition: "width 0.3s ease" }}></div>
          </div>
        </div>
      </div>

      <div className="hr" style={{ margin: "16px 0 20px 0" }}></div>

      {/* Main Learning Hub Layout */}
      <div style={{ display: "grid", gridTemplateColumns: "290px 1fr", gap: "24px" }}>
        {/* Module Sidebar */}
        <div>
          <div style={{ fontWeight: 800, fontSize: "14px", marginBottom: "10px", color: "var(--text-heading)", textTransform: "uppercase", letterSpacing: "0.5px" }}>
            Course Syllabus Modules ({modules.length})
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
            {modules.map((mod, idx) => {
              const isSelected = idx === selectedModuleIndex;
              const isCompleted = completedModules.includes(mod.id);
              return (
                <div
                  key={mod.id}
                  onClick={() => {
                    setSelectedModuleIndex(idx);
                    setSelectedOpt(null);
                    setQuizFeedback(null);
                    setActiveTab("notes");
                  }}
                  style={{
                    padding: "12px 14px",
                    borderRadius: "10px",
                    cursor: "pointer",
                    background: isSelected ? "rgba(2, 132, 199, 0.12)" : "var(--card-subtle)",
                    border: isSelected ? "1.5px solid var(--accent)" : "1px solid var(--border)",
                    transition: "all 0.15s ease",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <span style={{ fontSize: "13.5px", fontWeight: isSelected ? 800 : 600, color: isSelected ? "var(--accent)" : "var(--text-heading)" }}>
                      {mod.title.split(":")[0]}
                    </span>
                    {isCompleted ? (
                      <span style={{ color: "var(--ok)", fontSize: "14px", fontWeight: 800 }}>✓ Done</span>
                    ) : (
                      <span style={{ fontSize: "11px", color: "var(--muted)" }}>{mod.duration}</span>
                    )}
                  </div>
                  <div style={{ fontSize: "12px", color: isSelected ? "var(--accent)" : "var(--muted)", marginTop: "3px", fontWeight: 500 }}>
                    {mod.title.includes(":") ? mod.title.split(":")[1].trim() : mod.title}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="card" style={{ marginTop: "18px", background: "var(--card-subtle)", padding: "14px", borderRadius: "12px", border: "1px solid var(--border)" }}>
            <div style={{ fontWeight: 800, fontSize: "13px", color: "var(--text-heading)", marginBottom: "4px" }}>
              💡 Pedagogical AI Mentor
            </div>
            <p style={{ margin: "0 0 10px 0", fontSize: "12px", color: "var(--muted)", lineHeight: "1.4" }}>
              Need conceptual clarification or a step-by-step derivation? Ask your 24/7 AI mentor.
            </p>
            <button className="btn small" onClick={() => onNavigateTab("mentor")} style={{ width: "100%", fontWeight: 700 }}>
              Ask Mentor About This 💬
            </button>
          </div>
        </div>

        {/* Right Active Module Workspace */}
        <div>
          {/* Module Title Banner */}
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "14px", flexWrap: "wrap", gap: "8px" }}>
            <div>
              <span className="badge small" style={{ marginBottom: "4px", background: "rgba(2, 132, 199, 0.12)", color: "var(--accent)", fontWeight: 700 }}>
                {curModule.duration}
              </span>
              <h2 style={{ margin: "4px 0 0 0", fontSize: "20px", fontWeight: 800, color: "var(--text-heading)" }}>
                {curModule.title}
              </h2>
            </div>
            {completedModules.includes(curModule.id) && (
              <span style={{ padding: "4px 10px", borderRadius: "999px", background: "rgba(16, 185, 129, 0.1)", color: "#059669", fontSize: "12px", fontWeight: 800 }}>
                ✓ Completed
              </span>
            )}
          </div>

          {/* Module Content Mode Tabs */}
          <div style={{ display: "flex", gap: "6px", flexWrap: "wrap", marginBottom: "18px", borderBottom: "1px solid #e2e8f0", paddingBottom: "10px" }}>
            <button
              onClick={() => setActiveTab("notes")}
              className={`btn small ${activeTab === "notes" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              📖 Concepts & Notes
            </button>
            <button
              onClick={() => setActiveTab("video")}
              className={`btn small ${activeTab === "video" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              📹 Video Lecture
            </button>
            <button
              onClick={() => setActiveTab("formulas")}
              className={`btn small ${activeTab === "formulas" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              ⚡ Formulas & Cheat-sheet
            </button>
            <button
              onClick={() => setActiveTab("examples")}
              className={`btn small ${activeTab === "examples" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              💡 Worked Examples
            </button>
            <button
              onClick={() => setActiveTab("pitfalls")}
              className={`btn small ${activeTab === "pitfalls" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              ⚠️ Common Pitfalls
            </button>
            <button
              onClick={() => setActiveTab("materials")}
              className={`btn small ${activeTab === "materials" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              📄 Study Material
            </button>
            <button
              onClick={() => setActiveTab("quiz")}
              className={`btn small ${activeTab === "quiz" ? "" : "secondary"}`}
              style={{ fontWeight: 700 }}
              type="button"
            >
              📝 Checkpoint Quiz
            </button>
          </div>

          {/* TAB 1: Concepts & Detailed Notes */}
          {activeTab === "notes" && (
            <div>
              {/* Executive Summary */}
              <div style={{ background: "rgba(2, 132, 199, 0.08)", padding: "14px 16px", borderRadius: "10px", border: "1px solid rgba(2, 132, 199, 0.25)", marginBottom: "16px" }}>
                <div style={{ fontWeight: 800, fontSize: "13px", color: "var(--accent)", marginBottom: "4px", textTransform: "uppercase" }}>
                  📌 Module Executive Summary
                </div>
                <p style={{ margin: 0, fontSize: "14px", lineHeight: "1.6", color: "var(--text)", fontWeight: 500 }}>
                  {curModule.summary}
                </p>
              </div>

              {/* Detailed Conceptual Notes */}
              <div style={{ background: "var(--card)", padding: "16px 18px", borderRadius: "10px", border: "1px solid var(--border)", marginBottom: "16px" }}>
                <h3 style={{ margin: "0 0 12px 0", fontSize: "16px", fontWeight: 800, color: "var(--text-heading)" }}>
                  📚 Theory, Principles & Systematic Derivations
                </h3>
                {curModule.detailed_notes && curModule.detailed_notes.length > 0 ? (
                  <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
                    {curModule.detailed_notes.map((note, nIdx) => (
                      <div key={nIdx} style={{ fontSize: "14px", lineHeight: "1.65", color: "var(--text)", background: "var(--card-subtle)", padding: "12px 14px", borderRadius: "8px", borderLeft: "3px solid var(--accent)" }}>
                        {note}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p style={{ fontSize: "14px", color: "var(--muted)", lineHeight: "1.6" }}>
                    {curModule.summary}
                  </p>
                )}
              </div>

              {/* Formula Callout */}
              {curModule.formula_note && (
                <div style={{ background: "rgba(99, 102, 241, 0.1)", padding: "12px 16px", borderRadius: "10px", border: "1px solid rgba(99, 102, 241, 0.25)", marginBottom: "16px" }}>
                  <div style={{ fontWeight: 800, fontSize: "12.5px", color: "var(--brand)", marginBottom: "4px" }}>
                    ⚡ Key Takeaway Equation
                  </div>
                  <div style={{ fontSize: "13.5px", color: "var(--text-heading)", fontWeight: 600 }}>
                    {curModule.formula_note}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: Video Lecture */}
          {activeTab === "video" && (
            <div style={{ background: "var(--card)", padding: "18px", borderRadius: "12px", border: "1px solid var(--border)" }}>
              <div style={{ marginBottom: "12px" }}>
                <h3 style={{ margin: "0 0 4px 0", fontSize: "17px", fontWeight: 800, color: "var(--text-heading)" }}>
                  {resolvedVideo.title}
                </h3>
                <p style={{ margin: 0, fontSize: "13px", color: "var(--muted)" }}>
                  Visual lecture walkthrough covering core definitions, graphical derivations, and intuition.
                </p>
              </div>

              {/* Video Player Container */}
              <div style={{ position: "relative", width: "100%", paddingTop: "56.25%", borderRadius: "12px", overflow: "hidden", background: "#000000", marginBottom: "14px" }}>
                <iframe
                  src={resolvedVideo.url}
                  title={resolvedVideo.title}
                  style={{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", border: "none" }}
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>

              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", fontSize: "12.5px", color: "var(--muted)" }}>
                <span>Source: Accredited Open Educational Lecture (Khan Academy / CrashCourse / NCERT)</span>
                <span style={{ fontWeight: 700, color: "var(--accent)" }}>HD Streaming • Free Access</span>
              </div>
            </div>
          )}

          {/* TAB 3: Formulas & Cheat-sheet */}
          {activeTab === "formulas" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              <div style={{ background: "rgba(2, 132, 199, 0.1)", padding: "12px 16px", borderRadius: "10px", border: "1px solid rgba(2, 132, 199, 0.25)" }}>
                <div style={{ fontWeight: 800, fontSize: "13px", color: "var(--accent)", marginBottom: "2px" }}>
                  ⚡ Master Formula Sheet
                </div>
                <div style={{ fontSize: "13px", color: "var(--text)" }}>
                  Quick reference equations, variable designations, and dimensional units required for competitive examination numericals.
                </div>
              </div>

              {curModule.formula_sheet && curModule.formula_sheet.length > 0 ? (
                curModule.formula_sheet.map((item, fIdx) => (
                  <div key={fIdx} style={{ background: "var(--card)", padding: "16px", borderRadius: "10px", border: "1px solid var(--border)" }}>
                    <div style={{ fontWeight: 800, fontSize: "15px", color: "var(--text-heading)", marginBottom: "6px" }}>
                      {item.name}
                    </div>
                    <div style={{ background: "var(--card-subtle)", padding: "10px 14px", borderRadius: "8px", fontFamily: "monospace", fontSize: "15px", fontWeight: 700, color: "var(--accent)", border: "1px solid var(--border)", marginBottom: "8px" }}>
                      {item.formula}
                    </div>
                    <div style={{ fontSize: "13px", color: "var(--text)", marginBottom: "4px" }}>
                      <strong style={{ color: "var(--text-heading)" }}>Variables: </strong>{item.variables}
                    </div>
                    {item.notes && (
                      <div style={{ fontSize: "12.5px", color: "var(--muted)", fontStyle: "italic" }}>
                        💡 Note: {item.notes}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div style={{ background: "var(--card)", padding: "16px", borderRadius: "10px", border: "1px solid var(--border)" }}>
                  <div style={{ fontFamily: "monospace", fontSize: "15px", fontWeight: 700, color: "var(--accent)" }}>
                    {curModule.formula_note}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 4: Worked Examples */}
          {activeTab === "examples" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div style={{ background: "rgba(16, 185, 129, 0.1)", padding: "12px 16px", borderRadius: "10px", border: "1px solid rgba(16, 185, 129, 0.25)" }}>
                <div style={{ fontWeight: 800, fontSize: "13px", color: "var(--ok)", marginBottom: "2px" }}>
                  💡 Step-by-Step Solved Problem Drills
                </div>
                <div style={{ fontSize: "13px", color: "var(--text)" }}>
                  Examine authentic exam-style numericals with explicit solution breakdowns and pedagogical insights.
                </div>
              </div>

              {curModule.worked_examples && curModule.worked_examples.length > 0 ? (
                curModule.worked_examples.map((ex, eIdx) => (
                  <div key={eIdx} style={{ background: "var(--card)", padding: "18px", borderRadius: "12px", border: "1px solid var(--border)" }}>
                    <div style={{ fontWeight: 800, fontSize: "14.5px", color: "var(--text-heading)", marginBottom: "10px", lineHeight: "1.5" }}>
                      Problem {eIdx + 1}: {ex.problem}
                    </div>
                    <div style={{ display: "flex", flexDirection: "column", gap: "6px", marginBottom: "12px" }}>
                      {ex.solution_steps.map((step, sIdx) => (
                        <div key={sIdx} style={{ fontSize: "13.5px", color: "var(--text)", lineHeight: "1.5", background: "var(--card-subtle)", padding: "8px 12px", borderRadius: "6px" }}>
                          {step}
                        </div>
                      ))}
                    </div>
                    {ex.key_insight && (
                      <div style={{ background: "rgba(245, 158, 11, 0.12)", padding: "10px 14px", borderRadius: "8px", borderLeft: "3px solid var(--warn)", fontSize: "13px", color: "var(--text-heading)" }}>
                        <strong>🎯 Key Insight: </strong>{ex.key_insight}
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <p style={{ fontSize: "14px", color: "var(--muted)" }}>
                  No standalone worked examples for this module. Review the practice questions below.
                </p>
              )}
            </div>
          )}

          {/* TAB 5: Common Pitfalls */}
          {activeTab === "pitfalls" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              <div style={{ background: "rgba(239, 68, 68, 0.08)", padding: "14px 16px", borderRadius: "10px", border: "1px solid rgba(239, 68, 68, 0.25)" }}>
                <div style={{ fontWeight: 800, fontSize: "13.5px", color: "var(--danger)", marginBottom: "2px" }}>
                  ⚠️ Critical Examination Pitfalls & Common Student Traps
                </div>
                <div style={{ fontSize: "13px", color: "var(--text)" }}>
                  These common misconceptions account for over 70% of negative markings in entrance tests. Study them to protect your score!
                </div>
              </div>

              {curModule.pitfalls && curModule.pitfalls.length > 0 ? (
                curModule.pitfalls.map((pitfall, pIdx) => (
                  <div key={pIdx} style={{ background: "var(--card)", padding: "14px 16px", borderRadius: "10px", border: "1px solid var(--border)", borderLeft: "4px solid var(--danger)" }}>
                    <div style={{ fontSize: "13.5px", color: "var(--text)", lineHeight: "1.6", fontWeight: 500 }}>
                      ❌ {pitfall}
                    </div>
                  </div>
                ))
              ) : (
                <div style={{ background: "var(--card)", padding: "14px 16px", borderRadius: "10px", border: "1px solid var(--border)", fontSize: "13.5px", color: "var(--muted)" }}>
                  Always check unit conversions and coordinate directions before finalizing your answer.
                </div>
              )}
            </div>
          )}

          {/* TAB 6: Study Materials & Reference Chapters */}
          {activeTab === "materials" && (
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              <div style={{ background: "var(--card-subtle)", padding: "12px 16px", borderRadius: "10px", border: "1px solid var(--border)" }}>
                <div style={{ fontWeight: 800, fontSize: "13px", color: "var(--text-heading)", marginBottom: "2px" }}>
                  📄 Authentic Study Materials & Textbook Chapters
                </div>
                <div style={{ fontSize: "13px", color: "var(--muted)" }}>
                  Accredited syllabus references, official NCERT digital portals, and open-source college textbooks.
                </div>
              </div>

              {curModule.study_materials && curModule.study_materials.length > 0 ? (
                curModule.study_materials.map((mat, mIdx) => (
                  <div key={mIdx} style={{ background: "var(--card)", padding: "16px", borderRadius: "10px", border: "1px solid var(--border)", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
                    <div>
                      <span className="badge small" style={{ marginBottom: "4px" }}>{mat.type}</span>
                      <div style={{ fontWeight: 700, fontSize: "14.5px", color: "var(--text-heading)" }}>
                        {mat.title}
                      </div>
                    </div>
                    <a
                      href={mat.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn small secondary"
                      style={{ fontWeight: 700, textDecoration: "none" }}
                    >
                      Open Resource ↗
                    </a>
                  </div>
                ))
              ) : (
                <div style={{ background: "var(--card)", padding: "16px", borderRadius: "10px", border: "1px solid var(--border)" }}>
                  <a href="https://ncert.nic.in/textbook.php" target="_blank" rel="noopener noreferrer" className="btn small secondary">
                    NCERT Official Textbook Repository ↗
                  </a>
                </div>
              )}
            </div>
          )}

          {/* TAB 7: Checkpoint Quiz */}
          {activeTab === "quiz" && (
            <div className="card" style={{ background: "var(--card)", padding: "20px", borderRadius: "12px", border: "1px solid var(--border)" }}>
              <div style={{ fontWeight: 800, fontSize: "14px", color: "var(--text-heading)", marginBottom: "10px" }}>
                📝 Check Your Understanding — Interactive Checkpoint
              </div>

              {curModule.practice_question ? (
                <div>
                  <div style={{ fontSize: "15px", fontWeight: 600, color: "var(--text-heading)", marginBottom: "14px", lineHeight: "1.5" }}>
                    {curModule.practice_question.q}
                  </div>

                  <div style={{ display: "grid", gap: "10px", marginBottom: "16px" }}>
                    {curModule.practice_question.options.map((opt, oIdx) => (
                      <label
                        key={oIdx}
                        style={{
                          display: "flex",
                          alignItems: "center",
                          gap: "12px",
                          padding: "10px 14px",
                          borderRadius: "8px",
                          background: selectedOpt === oIdx ? "rgba(2, 132, 199, 0.12)" : "var(--card-subtle)",
                          border: selectedOpt === oIdx ? "1.5px solid var(--accent)" : "1px solid var(--border)",
                          cursor: "pointer",
                          fontSize: "14px",
                          transition: "all 0.1s ease",
                        }}
                      >
                        <input
                          type="radio"
                          name={`modQ_${curModule.id}`}
                          value={oIdx}
                          checked={selectedOpt === oIdx}
                          onChange={() => setSelectedOpt(oIdx)}
                        />
                        <span style={{ color: selectedOpt === oIdx ? "var(--accent)" : "var(--text)", fontWeight: selectedOpt === oIdx ? 700 : 400 }}>
                          {opt}
                        </span>
                      </label>
                    ))}
                  </div>

                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    <button
                      className="btn small"
                      onClick={handleCheckAnswer}
                      disabled={selectedOpt === null}
                      type="button"
                    >
                      Verify Answer ✓
                    </button>

                    {selectedModuleIndex < modules.length - 1 && (
                      <button className="btn small secondary" onClick={handleNextModule} type="button">
                        Next Module →
                      </button>
                    )}
                  </div>

                  {quizFeedback && (
                    <div
                      style={{
                        marginTop: "14px",
                        padding: "12px 16px",
                        borderRadius: "8px",
                        fontSize: "13.5px",
                        background: quizFeedback.isCorrect ? "rgba(16, 185, 129, 0.12)" : "rgba(239, 68, 68, 0.12)",
                        border: `1px solid ${quizFeedback.isCorrect ? "var(--ok)" : "var(--danger)"}`,
                        color: quizFeedback.isCorrect ? "var(--ok)" : "var(--danger)",
                        lineHeight: "1.5",
                      }}
                    >
                      {quizFeedback.text}
                    </div>
                  )}
                </div>
              ) : (
                <p style={{ color: "var(--muted)" }}>No checkpoint question available for this module.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
