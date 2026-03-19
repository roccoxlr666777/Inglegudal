import streamlit as st
import pandas as pd
import os
import random

# ==========================================
# 1. CONFIGURACIÓN Y ESTILOS
# ==========================================
st.set_page_config(page_title="Legal English Simulator", page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #1a252f !important; font-family: 'Times New Roman', serif; }
    .stButton>button { background-color: #2c3e50; color: #ffffff; font-weight: bold; border-radius: 5px; }
    .stButton>button:hover { background-color: #1a252f; color: white; border: 1px solid #f39c12; }
    .header-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 8px solid #2c3e50; box-shadow: 0px 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .legal-doc { background-color: #ffffff; padding: 30px; border: 1px solid #bdc3c7; box-shadow: 3px 3px 10px rgba(0,0,0,0.05); font-family: 'Courier New', monospace; color: #333;}
    .instruction-tag { background-color: #f1c40f; color: #000; padding: 2px 5px; border-radius: 3px; font-weight: bold; font-family: sans-serif;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CARGA DE DATOS Y BUSCADOR
# ==========================================
@st.cache_data
def cargar_vocabulario():
    if not os.path.exists('vocabulario_legal.csv'): return pd.DataFrame()
    try: return pd.read_csv('vocabulario_legal.csv', encoding='utf-8')
    except: return pd.DataFrame()

df_vocab = cargar_vocabulario()

# ==========================================
# 3. BASE DE DATOS GRAMATICAL JURÍDICA
# ==========================================
gramatica = {
    "Presente": {
        "Simple (Hechos/Leyes)": {
            "Indicativo": {"f": "Sujeto + Verbo (s/es) + Comp.", "e": "The judge dismisses the case."},
            "Interrogativo": {"f": "Do/Does + Sujeto + Verbo + Comp. + ?", "e": "Does the judge dismiss the case?"},
            "Imperativo": {"f": "Verbo base + Comp.", "e": "Dismiss the case immediately."},
            "Subjuntivo": {"f": "Sujeto1 + demand/order that + Sujeto2 + Verbo base", "e": "The lawyer demands that the witness speak the truth."}
        },
        "Continuo (Acciones en curso)": {
            "Indicativo": {"f": "Sujeto + am/is/are + Verbo(-ing) + Comp.", "e": "The jury is deliberating the verdict."},
            "Interrogativo": {"f": "Am/Is/Are + Sujeto + Verbo(-ing) + Comp. + ?", "e": "Is the jury deliberating the verdict?"}
        },
        "Perfecto (Acciones pasadas con impacto hoy)": {
            "Indicativo": {"f": "Sujeto + have/has + Participio + Comp.", "e": "The plaintiff has filed the lawsuit."},
            "Interrogativo": {"f": "Have/Has + Sujeto + Participio + Comp. + ?", "e": "Has the plaintiff filed the lawsuit?"}
        }
    },
    "Pasado": {
        "Simple (Casos cerrados)": {
            "Indicativo": {"f": "Sujeto + Verbo(Pasado) + Comp.", "e": "The defendant pleaded guilty."},
            "Interrogativo": {"f": "Did + Sujeto + Verbo base + Comp. + ?", "e": "Did the defendant plead guilty?"},
            "Subjuntivo": {"f": "If + Sujeto + Verbo(Pasado), Sujeto + would + Verbo", "e": "If the evidence were legal, we would win."}
        },
        "Continuo (Contexto de un delito/hecho)": {
            "Indicativo": {"f": "Sujeto + was/were + Verbo(-ing)", "e": "The suspect was fleeing the scene."},
            "Interrogativo": {"f": "Was/Were + Sujeto + Verbo(-ing) + ?", "e": "Was the suspect fleeing the scene?"}
        },
        "Perfecto (Precedentes)": {
            "Indicativo": {"f": "Sujeto + had + Participio", "e": "They had signed the contract before the dispute."},
            "Interrogativo": {"f": "Had + Sujeto + Participio + ?", "e": "Had they signed the contract before the dispute?"}
        }
    },
    "Futuro": {
        "Simple (Will - Sentencias/Promesas)": {
            "Indicativo": {"f": "Sujeto + will + Verbo base", "e": "The court will announce the sentence tomorrow."},
            "Interrogativo": {"f": "Will + Sujeto + Verbo base + ?", "e": "Will the court announce the sentence tomorrow?"}
        },
        "Continuo (Eventos programados)": {
            "Indicativo": {"f": "Sujeto + will be + Verbo(-ing)", "e": "The attorney will be deposing the witness at 10 AM."}
        },
        "Perfecto (Plazos legales)": {
            "Indicativo": {"f": "Sujeto + will have + Participio", "e": "By Friday, the judge will have issued the warrant."}
        }
    }
}

# ==========================================
# 4. FORMATOS LEGALES (DRAFTING)
# ==========================================
formatos = {
    "Habeas Corpus": {
        "Plantilla": """
        **IN THE [Insert Name of Court / Escribe el nombre del Tribunal]**
        
        **PETITION FOR WRIT OF HABEAS CORPUS**
        
        **TO THE HONORABLE JUDGE [Insert Judge's Name / Escribe el nombre del Juez]:**
        
        COMES NOW, [Insert Petitioner's Name / Escribe el nombre del demandante], and respectfully petitions this Court for a Writ of Habeas Corpus, and in support thereof states as follows:
        
        1. That Petitioner is unlawfully detained by [Insert Name of Authority or Police Dept / Escribe el nombre de la autoridad que lo retiene] at [Insert Location of Detention / Escribe el lugar de detención].
        2. That the detention is illegal because [Insert Legal Arguments / Escribe tus argumentos legales argumentando la violación al debido proceso].
        
        WHEREFORE, Petitioner prays that a Writ of Habeas Corpus be issued directing the Respondent to bring the Petitioner before this Court.
        """,
        "Completo": """
        **IN THE DISTRICT COURT OF PUEBLA**
        
        **PETITION FOR WRIT OF HABEAS CORPUS**
        
        **TO THE HONORABLE JUDGE JOHN DOE:**
        
        COMES NOW, Richard Roe, and respectfully petitions this Court for a Writ of Habeas Corpus, and in support thereof states as follows:
        
        1. That Petitioner is unlawfully detained by the State Police Department at the Central Holding Facility.
        2. That the detention is illegal because the Petitioner was arrested without a valid warrant and has been held for over 72 hours without being formally charged before a magistrate, violating his constitutional right to due process.
        
        WHEREFORE, Petitioner prays that a Writ of Habeas Corpus be issued directing the Respondent to bring the Petitioner before this Court to determine the legality of his detention.
        """
    },
    "Demanda Civil (Civil Lawsuit/Complaint)": {
        "Plantilla": """
        **COMPLAINT FOR BREACH OF CONTRACT**
        
        **PLAINTIFF:** [Insert Plaintiff's Name / Nombre del Actor]
        **DEFENDANT:** [Insert Defendant's Name / Nombre del Demandado]
        
        **I. JURISDICTION AND VENUE**
        [State why this court has jurisdiction / Escribe por qué este tribunal es competente].
        
        **II. STATEMENT OF FACTS**
        On or about [Insert Date / Escribe la fecha], Plaintiff and Defendant entered into a written agreement for [Describe the contract purpose / Describe el propósito del contrato].
        Defendant breached said contract by [Describe the breach / Describe el incumplimiento].
        
        **III. PRAYER FOR RELIEF**
        Plaintiff requests damages in the amount of $[Insert Amount / Escribe la cantidad] plus attorney's fees.
        """,
        "Completo": """
        **COMPLAINT FOR BREACH OF CONTRACT**
        
        **PLAINTIFF:** Acme Corp.
        **DEFENDANT:** Global Supplies Inc.
        
        **I. JURISDICTION AND VENUE**
        This court has jurisdiction because both parties reside and conduct business within this judicial district, and the damages exceed $50,000.
        
        **II. STATEMENT OF FACTS**
        On or about October 1st, 2025, Plaintiff and Defendant entered into a written agreement for the delivery of 10,000 steel pipes.
        Defendant breached said contract by failing to deliver the goods by the agreed deadline of December 1st, 2025, causing a halt in Plaintiff's construction projects.
        
        **III. PRAYER FOR RELIEF**
        Plaintiff requests compensatory damages in the amount of $150,000 plus reasonable attorney's fees and court costs.
        """
    },
    "Guión de Audiencia Penal (Criminal Hearing Script)": {
        "Plantilla": """
        **JUDGE:** Are the parties ready to proceed?
        **PROSECUTOR:** Yes, Your Honor. The State calls [Insert Witness Name / Escribe el nombre del testigo].
        **DEFENSE ATTORNEY:** Your Honor, we object. [Insert Legal Basis for Objection / Escribe la base legal de la objeción, ej. Hearsay, Relevance].
        **JUDGE:** Objection [Insert Sustained or Overruled / Escribe si la objeción procede (Sustained) o se rechaza (Overruled)].
        **PROSECUTOR:** [State your next action / Escribe tu siguiente acción procesal].
        """,
        "Completo": """
        **JUDGE:** Are the parties ready to proceed?
        **PROSECUTOR:** Yes, Your Honor. The State calls Officer Smith to the stand.
        **DEFENSE ATTORNEY:** Your Honor, we object to this witness. The prosecution failed to disclose this officer's report during the discovery phase.
        **JUDGE:** Objection sustained. The witness may not testify until the defense has had proper time to review the report.
        **PROSECUTOR:** Understood, Your Honor. We request a brief recess to provide the documents to the defense counsel.
        """
    },
    "Denuncia Penal (Criminal Complaint)": {
        "Plantilla": """
        **CRIMINAL COMPLAINT**
        
        **TO THE OFFICE OF THE PROSECUTOR / A LA FISCALÍA:**
        
        I, [Insert your name / Escribe tu nombre], residing at [Insert your address / Escribe tu dirección], under penalty of perjury, hereby file this criminal complaint against [Insert Suspect's Name / Nombre del sospechoso] for the crime of [Insert Crime, e.g., Fraud, Larceny / Escribe el delito].
        
        **STATEMENT OF FACTS:**
        On [Insert Date / Fecha], the aforementioned individual did unlawfully [Describe the criminal act / Describe el acto delictivo]. 
        
        I respectfully request that a formal investigation be opened and an arrest warrant be issued if probable cause is found.
        """,
        "Completo": """
        **CRIMINAL COMPLAINT**
        
        **TO THE OFFICE OF THE PROSECUTOR:**
        
        I, Jane Doe, residing at 123 Main Street, Puebla, under penalty of perjury, hereby file this criminal complaint against John Smith for the crime of Embezzlement.
        
        **STATEMENT OF FACTS:**
        On October 15, 2025, the aforementioned individual, while acting as the financial director of our company, did unlawfully transfer $50,000 USD from the corporate account to his personal offshore account without authorization.
        
        I respectfully request that a formal investigation be opened and an arrest warrant be issued if probable cause is found.
        """
    },
    "Habeas Data (Data Protection Request)": {
        "Plantilla": """
        **PETITION FOR HABEAS DATA / ARCO RIGHTS EXERCISE**
        
        **TO: [Insert Company or Agency Name / Nombre de la empresa o agencia]**
        
        Pursuant to the Data Protection Laws, I, [Insert your name / Tu nombre], hereby exercise my right of [Access / Rectification / Cancellation / Opposition].
        
        I request that your organization immediately [Describe the action: e.g., delete my personal data, provide a copy of my records / Describe la acción solicitada] regarding the information held under the account number [Insert Account or ID Number / Número de cuenta o ID].
        
        Failure to comply within the statutory timeframe will result in formal complaints filed before the National Data Protection Authority.
        """,
        "Completo": """
        **PETITION FOR HABEAS DATA / ARCO RIGHTS EXERCISE**
        
        **TO: Global Credit Bank**
        
        Pursuant to the Data Protection Laws, I, Richard Roe, hereby exercise my right of Cancellation.
        
        I request that your organization immediately delete all my personal and financial data regarding the information held under the account number 987654321, as my contractual relationship with your bank was terminated over five years ago.
        
        Failure to comply within the statutory timeframe will result in formal complaints filed before the National Data Protection Authority.
        """
    },
    "Carta de Cese y Desistimiento (Cease and Desist Letter)": {
        "Plantilla": """
        **CEASE AND DESIST LETTER**
        
        **VIA CERTIFIED MAIL**
        
        Dear [Insert Name of the Infringer / Nombre del infractor]:
        
        This law firm represents [Insert Client's Name / Nombre de tu cliente]. It has come to our attention that you are currently engaging in [Describe the illegal activity, e.g., trademark infringement, harassment / Describe la actividad ilícita].
        
        We hereby demand that you immediately **CEASE AND DESIST** from this activity. If you fail to comply by [Insert Deadline / Fecha límite], we will have no choice but to pursue all available legal remedies against you, including filing a lawsuit for damages and seeking a preliminary injunction.
        
        Govern yourself accordingly.
        """,
        "Completo": """
        **CEASE AND DESIST LETTER**
        
        **VIA CERTIFIED MAIL**
        
        Dear Mr. John Smith:
        
        This law firm represents Acme Corporation. It has come to our attention that you are currently engaging in trademark infringement by using our client's registered logo on your counterfeit products.
        
        We hereby demand that you immediately **CEASE AND DESIST** from this activity. If you fail to comply by Friday, October 31st, we will have no choice but to pursue all available legal remedies against you, including filing a lawsuit for damages and seeking a preliminary injunction.
        
        Govern yourself accordingly.
        """
    },
    "Sentencia Civil (Civil Judgment)": {
        "Plantilla": """
        **IN THE [Insert Court Name / Nombre del Tribunal]**
        
        **FINAL JUDGMENT**
        
        This matter came before the Court on [Insert Date of Trial / Fecha del juicio]. After considering the pleadings, evidence, and testimony presented by both Plaintiff [Insert Plaintiff's Name / Actor] and Defendant [Insert Defendant's Name / Demandado], the Court finds as follows:
        
        **IT IS HEREBY ORDERED AND ADJUDGED:**
        1. That judgment is entered in favor of the [Plaintiff/Defendant / Escribe quién gana].
        2. That the Defendant shall pay the Plaintiff the sum of $[Insert Amount / Cantidad] in compensatory damages.
        3. This case is hereby dismissed with prejudice.
        
        **SO ORDERED** this [Insert Date / Fecha de firma].
        
        ___________________________
        **HON. [Insert Judge's Name / Nombre del Juez]**
        """,
        "Completo": """
        **IN THE DISTRICT COURT OF PUEBLA**
        
        **FINAL JUDGMENT**
        
        This matter came before the Court on October 20, 2025. After considering the pleadings, evidence, and testimony presented by both Plaintiff Acme Corp. and Defendant Global Supplies Inc., the Court finds as follows:
        
        **IT IS HEREBY ORDERED AND ADJUDGED:**
        1. That judgment is entered in favor of the Plaintiff.
        2. That the Defendant shall pay the Plaintiff the sum of $150,000 USD in compensatory damages for breach of contract.
        3. This case is hereby dismissed with prejudice.
        
        **SO ORDERED** this 25th day of October, 2025.
        
        ___________________________
        **HON. JANE DOE**
        """
    }
}
# Agrega aquí Reportes, Sentencias, Cartas, etc., siguiendo el mismo formato de Diccionario.

# ==========================================
# 5. UI PRINCIPAL
# ==========================================
st.markdown("""
<div class='header-box'>
    <h1 style='margin: 0;'>⚖️ Legal English & Drafting Simulator</h1>
    <p style='margin: 0; font-size: 1.1rem; color: #555;'>Advanced Legal Lexicon, Grammar, and Document Drafting</p>
</div>
""", unsafe_allow_html=True)

tab_vocab, tab_gram, tab_drafting = st.tabs(["📚 Legal Lexicon & Search", "⚙️ Grammar & Syntax Engine", "📝 Legal Drafting (Formatos)"])

# --- PESTAÑA 1: VOCABULARIO Y BUSCADOR ---
with tab_vocab:
    st.markdown("### Searchable Legal Database (500 Words)")
    
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        busqueda = st.text_input("🔍 Buscar palabra (Inglés o Español):", "")
    with col_filter:
        if not df_vocab.empty:
            cat_list = ["Todas"] + list(df_vocab["Categoría Gramatical"].unique())
            cat_filtro = st.selectbox("Filtrar por Categoría:", cat_list)
        else: cat_filtro = "Todas"
        
    if not df_vocab.empty:
        df_mostrar = df_vocab.copy()
        if busqueda:
            df_mostrar = df_mostrar[df_mostrar.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]
        if cat_filtro != "Todas":
            df_mostrar = df_mostrar[df_mostrar["Categoría Gramatical"] == cat_filtro]
            
        st.dataframe(df_mostrar.reset_index(drop=True), use_container_width=True, height=400)
        st.caption(f"Mostrando {len(df_mostrar)} resultados.")
    else: st.error("Falta el archivo CSV.")

# --- PESTAÑA 2: GRAMÁTICA Y RETO ---
with tab_gram:
    st.markdown("### Sintaxis Jurídica (Tiempos y Modos)")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1: tiempo_gen = st.selectbox("1. Tiempo:", list(gramatica.keys()))
    with col_t2: tipo_gen = st.selectbox("2. Tipo:", list(gramatica[tiempo_gen].keys()))
    with col_t3: modo_gen = st.radio("3. Modo:", list(gramatica[tiempo_gen][tipo_gen].keys()))
    
    datos_gram = gramatica[tiempo_gen][tipo_gen][modo_gen]
    
    st.markdown(f"**Fórmula:** `{datos_gram['f']}`")
    st.success(f"**Ejemplo Legal:** {datos_gram['e']}")
    
    st.markdown("---")
    st.markdown("### 🎲 Generar Reto a partir de las Palabras")
    st.write("El sistema extraerá vocabulario de la base de datos para que construyas una oración legal en el tiempo seleccionado.")
    
    if st.button("Extraer Palabras al Azar"):
        if not df_vocab.empty:
            verbos = df_vocab[df_vocab["Categoría Gramatical"].str.contains("Verbo", case=False, na=False)]["Palabra en Inglés"].tolist()
            sustantivos = df_vocab[df_vocab["Categoría Gramatical"].str.contains("Sustantivo", case=False, na=False)]["Palabra en Inglés"].tolist()
            
            if verbos and sustantivos:
                st.info(f"**Instrucción:** Redacta una oración en **{tiempo_gen} {tipo_gen} ({modo_gen})** usando obligatoriamente estas palabras:")
                st.markdown(f"- **Sustantivos:** {random.choice(sustantivos)}, {random.choice(sustantivos)}")
                st.markdown(f"- **Verbo:** {random.choice(verbos)}")
        else: st.warning("Carga el CSV primero.")

# --- PESTAÑA 3: FORMATOS LEGALES (DRAFTING) ---
with tab_drafting:
    st.markdown("### Panel de Redacción Jurídica (Legal Drafting)")
    st.write("Selecciona el tipo de documento procesal y la modalidad de estudio.")
    
    col_doc, col_mod = st.columns([2, 1])
    with col_doc:
        doc_seleccionado = st.selectbox("Selecciona el formato legal:", list(formatos.keys()))
    with col_mod:
        modalidad = st.radio("Modalidad de Visualización:", ["Plantilla (Guiada)", "Ejemplo Completo"])
    
    st.markdown("---")
    tipo_llave = "Plantilla" if "Plantilla" in modalidad else "Completo"
    texto_mostrar = formatos[doc_seleccionado][tipo_llave]
    
    st.markdown(f"<div class='legal-doc'>{texto_mostrar}</div>", unsafe_allow_html=True)
    
    if "Plantilla" in modalidad:
        st.caption("💡 Las instrucciones entre corchetes [ ] te indican qué información procesal debes traducir o redactar en inglés.")
