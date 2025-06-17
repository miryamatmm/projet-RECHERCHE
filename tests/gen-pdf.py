import os
from fpdf import FPDF

# Définition des sujets de stage avec plus de contenu
sujets_de_stages = [
    ("Web Development", """Development of an e-learning platform using React and Node.js.
    This internship will involve designing and implementing a modern web application 
    for managing courses, student registration, and integrating artificial intelligence 
    to recommend personalized educational content.
    The goal is to optimize the user experience and ensure a scalable platform.
    The project will also include notifications management, an interactive quiz system,
    and an admin interface to track student progress."""),

    ("Cybersecurity", """Analysis of SQL injection attacks and database protection.
    The objective of this internship is to study the main vulnerabilities of databases 
    to SQL injection attacks, design a secure testing environment, and develop 
    advanced mitigation techniques to prevent such attacks.
    Part of the internship will also include log analysis and automated threat detection 
    using tools like Snort and Suricata."""),

    ("Artificial Intelligence", """Deep learning for medical image recognition.
    You will work on a classification model for medical images using convolutional neural networks (CNN).
    The objective is to train a model capable of detecting anomalies in MRI scans or radiographs,
    based on publicly available medical datasets. This project also includes a study of algorithmic biases.
    A comparison between different architectures such as ResNet, EfficientNet, and Vision Transformers will be conducted."""),

    ("Molecular Biology", """Study of genetic mutations in rare diseases.
    This internship aims to analyze genetic mutations responsible for rare diseases using 
    next-generation sequencing (NGS) techniques. 
    A bioinformatics approach will be used to filter and interpret genetic variations.
    You will work with genomic databases and software such as GATK and VarScan.
    Functional analysis of mutations will be performed to assess their impact on cell biology."""),

    ("Quantum Physics", """Simulation of quantum circuits with IBM Qiskit.
    This internship focuses on quantum programming and experimentation with quantum circuits 
    using the IBM Quantum Experience platform.
    You will develop quantum algorithms to solve optimization and cryptography problems.
    A part of the work will also include modeling errors in qubits and simulating the effects 
    of quantum noise and decoherence."""),

    ("Robotics", """Development of an autonomous robot for warehouse logistics.
    You will design and program a mobile robot capable of navigating and transporting objects
    while avoiding obstacles. This project will include the integration of LiDAR sensors 
    and cameras to enhance navigation and object recognition.
    A pathfinding algorithm will be implemented to optimize its movements.
    A SLAM (Simultaneous Localization and Mapping) implementation will be explored to enable 
    more precise navigation."""),

    ("Renewable Energy", """Optimization of solar panels using predictive models.
    This internship will analyze the performance of solar panels under different climate conditions 
    and use machine learning models to predict their efficiency and optimize their positioning.
    A part of the work will also include the study of innovative photovoltaic materials.
    Simulations using MATLAB or Python will be conducted to estimate energy gains."""),

    ("Applied Mathematics", """Mathematical modeling of epidemics and propagation simulation.
    You will develop epidemiological models (SIR, SEIR, etc.) to simulate the spread of diseases 
    and evaluate the effectiveness of public health measures based on historical data.
    A comparative study of vaccination strategies will be included.
    Monte Carlo techniques and advanced statistical analyses will be explored."""),

    ("Civil Engineering", """Simulation of mechanical constraints on reinforced concrete bridges.
    This internship focuses on numerical simulation of forces applied to reinforced concrete structures.
    You will use finite element analysis (FEA) software to identify weak points.
    An experimental study may be conducted on physical models.
    Advanced modeling methods such as topological optimization will also be explored."""),

    ("Signal Processing", """Detection of anomalies in EEG signals using neural networks.
    The objective of this internship is to design an artificial intelligence algorithm capable of analyzing 
    electroencephalographic signals (EEG) and automatically detecting cerebral anomalies.
    Validation on real hospital data will be conducted.
    The study will also include a comparison of EEG signal preprocessing techniques (filtering, wavelets)."""),

    ("Genetics", """Analysis of genetic mutations in hereditary diseases.
    This internship aims to identify and characterize mutations responsible for genetic diseases using 
    next-generation sequencing (NGS) techniques.
    A bioinformatics approach will be used to filter and interpret genetic variations.
    You will work with genomic databases and software such as GATK and VarScan.
    Functional analysis of mutations will be performed to assess their impact on cell biology."""),

    ("Microbiology", """Study of host-microbiota interactions in the gut.
    The objective is to characterize the impact of microbiota composition on human health.
    Metagenomic analyses will be conducted to identify dominant bacterial species and their metabolic roles.
    The influence of microbiota on certain diseases (obesity, autoimmune disorders) will be investigated.
    The study will include in vitro tests and bioinformatics analysis on metagenomic databases."""),

    ("Neuroscience", """Modeling neural networks in Alzheimer's disease.
    This project involves analyzing electrophysiological data and brain imaging to better understand 
    the mechanisms of neuronal degeneration.
    Simulations of biological neural networks will be conducted using tools like NEURON or Brian2.
    A combined approach including biochemical analyses, behavioral tests, and modeling will be used 
    to study the effects of amyloid proteins."""),

    ("Biotechnology", """Development of biosensors for detecting environmental pollutants.
    This internship will involve designing biosensors based on enzymes or fluorescent bacteria 
    to detect chemical and microbiological contaminants in water.
    Experimental validation will be conducted in the lab, using fluorescence microscopy techniques 
    to analyze results.
    Field tests will be performed to evaluate the biosensor's effectiveness."""),

    ("Cell Biology", """Analysis of the cell cycle and regulation of cell division.
    The objective is to study factors regulating cell cycle progression and their involvement in 
    diseases such as cancer.
    Fluorescence microscopy and Western blot experiments will be conducted.
    A particular focus will be placed on signaling mechanisms involved in cell cycle regulation."""),

    ("Ecology", """Impact of climate change on marine biodiversity.
    This internship will analyze the effects of temperature variations and ocean acidification 
    on coral populations and other marine organisms.
    Field data collection and predictive models will be used to estimate how marine ecosystems 
    evolve in response to climate change.
    Ecological modeling will be employed to evaluate the impact of rising temperatures on species reproduction and migration."""),

    ("Immunology", """Study of immune responses to viral infections.
    This project aims to characterize interactions between immune cells and pathogenic viruses, 
    using flow cytometry and confocal imaging approaches.
    A bioinformatics analysis of immune activation markers will be conducted.
    The study will also include mathematical modeling of immune response dynamics."""),

    ("Biochemistry", """Characterization of proteins involved in metabolic regulation.
    The objective is to study the structure and function of key enzymes in energy metabolism.
    Mass spectrometry and crystallography analyses will be performed.
    The internship will include an in-depth analysis of protein-protein interactions 
    to understand metabolic pathways."""),

    ("Genomics", """Comparison of genomes among different primate species.
    This internship aims to identify genomic differences between humans and other primates 
    to better understand the evolution of human-specific traits.
    Bioinformatics analyses of sequencing databases will be conducted.
    A part of the project will focus on identifying genome regions under accelerated natural selection."""),

    ("Physiology", """Hormonal regulation of stress and its impact on behavior.
    This project will analyze hormone levels in response to various stress factors and their 
    impact on animal behavior.
    Laboratory experiments on animal models will be conducted.
    The study will include the analysis of stress biomarkers and their correlation with specific behaviors.""")
]


# Création du dossier des PDFs
pdf_dir = "../tests/pdf/en"
os.makedirs(pdf_dir, exist_ok=True)

# Génération des PDF
for i, (titre, description) in enumerate(sujets_de_stages, 1):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Nettoyage des caractères problématiques pour éviter UnicodeEncodeError
    titre = titre.replace("’", "'").replace("é", "e").replace("–", "-")
    description = description.replace("’", "'").replace("é", "e").replace("–", "-")

    # Configuration du PDF avec une police compatible
    pdf.set_font("Helvetica", style='B', size=16)
    pdf.cell(200, 10, f"{i} : {titre}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)

    # Écriture du texte dans le PDF
    pdf.multi_cell(0, 10, description)

    # Sauvegarde du PDF
    pdf_filename = os.path.join(pdf_dir, f"internship_{i}_{titre.replace(' ', '_')}.pdf")
    pdf.output(pdf_filename)

print(f"✅ {len(sujets_de_stages)} fichiers PDF générés dans le dossier '{pdf_dir}'.")

