# AI-Medicine-Safety-System

## About

This project is a hybrid AI-powered healthcare decision support system that evaluates medication safety and symptom relevance. Using a custom dataset of 50 medicines, it analyzes potential drug interactions, generates a safety score (0-100), and assesses whether selected medicines are appropriate for user-reported symptoms. The system combines RapidFuzz, deterministic logic, Ollama LLM, and Google Gemini API to deliver explainable and context-aware recommendations.

---

## Objectives

* Evaluate the safety of taking multiple medicines together.
* Identify potential drug-drug interactions using structured datasets.
* Generate a medication safety score ranging from 0 to 100.
* Assess whether selected medicines are relevant to reported symptoms.
* Improve input accuracy using fuzzy matching techniques.
* Combine rule-based and AI-driven reasoning for enhanced decision support.
* Demonstrate the use of hybrid AI architectures in healthcare applications.

---

## Domain

**Healthcare Analytics | Artificial Intelligence | Clinical Decision Support Systems**

---

## Dataset Source

A custom dataset containing information on 50 commonly used medicines was created and curated for this project.

### Dataset Includes:

* Medicine names
* Drug categories
* Primary uses and indications
* Symptom associations
* Drug-drug interaction information
* Interaction severity levels

The dataset was compiled through research from publicly available pharmaceutical references and healthcare resources. It was then cleaned, standardized, and structured to support medication safety scoring and symptom-to-medication validation.

---

## Tools & Technologies Used

### Programming & Development

* Python
* JSON
* Jupyter Notebook
* Streamlit

### Data Processing

* Pandas
* NumPy

### AI & NLP

* RapidFuzz
* Ollama
* Google Gemini API

---

## System Architecture

### Layer 1: RapidFuzz Matching Engine

* Performs fuzzy matching and entity resolution for medicine and symptom inputs.
* Handles spelling variations, naming inconsistencies, and user input errors.
* Maps user-entered values to standardized records within the medicine dataset.
* Ensures accurate downstream analysis by providing validated inputs.

### Layer 2: Deterministic Drug Safety Engine

* Analyzes drug interaction records from the custom medicine dataset.
* Calculates medication safety scores ranging from 0 to 100.
* Identifies potential drug-drug interactions and associated risks.
* Generates transparent and explainable rule-based assessments.

### Layer 3: Ollama Local LLM

* Performs local symptom and medication analysis.
* Evaluates medicine relevance against reported symptoms.
* Enhances privacy by processing healthcare queries locally.
* Provides contextual insights to support deterministic outputs.

### Layer 4: Google Gemini API

* Performs advanced validation and contextual reasoning.
* Cross-checks medication suitability using symptom and medicine information.
* Generates user-friendly explanations and recommendations.
* Produces the final AI-assisted medication safety assessment.

---

## Workflow

```text
User Input
     │
     ▼
RapidFuzz Matching Engine
     │
     ▼
Deterministic Drug Safety Engine
     │
     ▼
Ollama Local LLM
     │
     ▼
Google Gemini API
     │
     ▼
Final Safety Assessment & Recommendations
```

---

## Key Features

* Drug interaction analysis
* Medication safety scoring (0-100)
* Symptom-based medication validation
* Fuzzy medicine and symptom matching
* Explainable AI recommendations
* Hybrid AI decision-support architecture
* Local and cloud-based AI integration
* Rule-based and generative AI validation

---

## How to Use

1. Launch the Streamlit application.
2. Enter the symptom name.
3. Enter one or more medicine names.
4. Submit the query for analysis.
5. Review:

   * Medication Safety Score
   * Potential Drug Interactions
   * Symptom-Medicine Relevance
   * AI-Generated Recommendations

---

## Potential Applications

* Medication safety awareness for individuals and caregivers.
* Preliminary drug interaction assessment.
* Nursing homes and assisted-care facilities.
* Educational healthcare analytics projects.
* AI-powered healthcare decision-support systems.
* Veterinary medication screening (with appropriate datasets).

---

## Findings & Conclusion

### Findings

* Successfully developed a custom healthcare dataset containing 50 medicines and their interaction profiles.
* RapidFuzz improved medicine and symptom recognition by handling spelling variations and input inconsistencies.
* Deterministic scoring provided transparent and explainable medication safety assessments.
* Combining local and cloud-based LLMs improved contextual understanding and recommendation quality.

### Conclusion

This project demonstrates how deterministic systems and generative AI can be integrated to create a reliable healthcare decision-support solution. By combining fuzzy matching, rule-based logic, and AI reasoning, the system delivers explainable medication safety assessments while maintaining flexibility and scalability for future healthcare applications.

---

## Future Enhancements

* Expand the medicine database beyond 50 medicines.
* Integrate real-time pharmaceutical databases and APIs.
* Add support for dosage-based safety analysis.
* Develop multilingual symptom and medication support.
* Introduce patient history and personalized recommendations.
* Build interactive dashboards for healthcare analytics.

---

## Disclaimer

This project is intended for educational and research purposes only. The recommendations generated by the system should not be considered medical advice, diagnosis, or treatment recommendations. Always consult a qualified healthcare professional before making healthcare decisions.

---

## About the Author

**Nishant Gupta**

MBA in AI & Data Science with interests in Data Analytics, Artificial Intelligence, Healthcare Analytics, and Decision Support Systems.

* Email: [Guptanishant0712@gmail.com](mailto:Guptanishant0712@gmail.com)
* LinkedIn: https://www.linkedin.com/in/nishantgupta07/
