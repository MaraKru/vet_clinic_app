import streamlit as st
import io
import pandas as pd
from database import get_all_patients, add_patient_record, delete_patient_from_db, clear_db, init_db
from drugs import DRUGS_DB

# db setup
init_db()


# page settings
st.set_page_config(page_title="Вет Калькулятор", page_icon="🐾")
custom_css = """
<style>
.stApp { background-color: #E8F5E9; }
.stButton>button { background-color: #4CAF50; color: white; border-radius: 10px; border: none; padding: 15px 30px; font-size: 18px; width: 100%; }
.stButton>button:hover { background-color: #45a049; }
h1, h2, h3 { color: #2E7D32 !important; }
</style>
"""


st.markdown(custom_css, unsafe_allow_html=True)  # allow raw HTML

if 'last_calc' not in st.session_state:  
    st.session_state.last_calc = None
if 'last_infusion' not in st.session_state:
    st.session_state.last_infusion = None
# session_state preserves all user actions in streamlit across reruns



st.title("🐾 Вет Калькулятор")   # Vet calculator

tab1, tab2 = st.tabs(["Калькулятор", "Пациенты"])  # Calculator, Patients

with tab1:
    st.header("Расчет дозы")  # Dosage calculation
    pet_name = st.text_input("Имя животного:")  # Pet's name
    species = st.selectbox("Вид животного:", ["Кошка", "Собака"])  # Species: Cat, Dog
    weight = st.number_input("Вес (кг):", min_value=0.1, max_value=100.0, step=0.1, value=4.0)
    
    drug = st.selectbox("Препарат:", list(DRUGS_DB.keys()))  # Drug:
    drug_data = DRUGS_DB[drug]
    
    if drug_data["min_d"] != drug_data["max_d"]:
        selected_dose = st.slider(f"Доза ({drug_data['unit']}/кг):", 
                                  min_value=float(drug_data["min_d"]), 
                                  max_value=float(drug_data["max_d"]), 
                                  value=float(drug_data["min_d"]))
    else:
        selected_dose = drug_data["min_d"]
        st.info(f"Доза: {selected_dose} {drug_data['unit']}/кг")  # Dosage:

    selected_conc = None
    if isinstance(drug_data["conc"], list):
        selected_conc = st.selectbox("Выберите концентрацию в 1 мл:", drug_data["conc"])
        # select conc per 1 ml 
    else:
        selected_conc = drug_data["conc"]

    injections = st.number_input("Разделить на приемов в сутки:", min_value=1, max_value=5, value=1, step=1)
    # Doses per day:
    
    if st.button("Рассчитать дозу"):  # to calculate dosage
        total_mg = None
        if drug_data["unit"] == "мг":
            dose_ml = (weight * selected_dose) / selected_conc
            total_mg = weight * selected_dose
        elif drug_data["unit"] == "мкг":
            dose_ml = (weight * (selected_dose / 1000)) / selected_conc
            total_mg = (weight * selected_dose) / 1000
        elif drug_data["unit"] == "МЕ":
            dose_ml = (weight * selected_dose) / selected_conc
        elif drug_data["unit"] == "мл":
            dose_ml = weight * selected_dose
            
        single_dose = dose_ml / injections
        single_mg = (total_mg / injections) if total_mg is not None else None
        
        st.session_state.last_calc = {
            "name": pet_name, "species": species, "weight": weight,
            "drug": drug, "injections": injections, "dose": single_dose,
            "single_mg": single_mg
        }
        st.session_state.last_infusion = None

    if st.session_state.last_calc is not None:
        calc = st.session_state.last_calc
        st.success(f"Для {calc['name']} ({calc['species']}):")
        st.write(f"Препарат: **{calc['drug']}**")
        st.write(f"Разовая доза: **{calc['dose']:.2f} мл** (при {calc['injections']} раз/сут)") # single dose:
        
        if calc.get('single_mg') is not None:
            st.write(f"Это соответствует **{calc['single_mg']:.2f} мг** действующего вещества.")
        
        if st.button("💾 Сохранить в карточку"):   # Save to chart
            if calc['name'] == "":
                st.error("Введите имя животного!")  # Enter pet's name!
            else:
                detail_text = f"{calc['injections']} раз/сут"
                if add_patient_record(calc['name'], calc['species'], calc['drug'], calc['weight'], detail_text, calc['dose'], "injection"):
                    st.success(f"Сохранено для {calc['name']}!")  # Saved for:
                    st.session_state.last_calc = None 



    st.divider()
    with st.expander("💧 Расчет инфузии - Допамин"):  # Infusion calc - Dopamine
        st.write("Расчет скорости поступления препарата.")  # Calc drug delivery rate
        
        inf_name = st.text_input("Имя животного (инфузия):")  # Pet's name
        inf_species = st.selectbox("Вид животного (инфузия):", ["Кошка", "Собака"])  # Species: Cat, Dog
        inf_weight = st.number_input("Вес (кг):", min_value=0.1, max_value=100.0, step=0.1, value=12.0)
        
        if st.button("Рассчитать скорость ИПС"):  # Calc CRI rate
            if inf_species == "Кошка":
                min_rate, max_rate = 2, 10
            else:
                min_rate, max_rate = 1, 5
                
            min_mcg_per_min = inf_weight * min_rate
            max_mcg_per_min = inf_weight * max_rate
            
            min_ml_per_min = min_mcg_per_min / 20000
            max_ml_per_min = max_mcg_per_min / 20000
            
            st.session_state.last_infusion = {
                "name": inf_name, "species": inf_species, "weight": inf_weight,
                "min_mcg": min_mcg_per_min, "max_mcg": max_mcg_per_min,
                "min_ml": min_ml_per_min, "max_ml": max_ml_per_min
            }
            st.session_state.last_calc = None
            
        if st.session_state.last_infusion is not None:
            inf = st.session_state.last_infusion
            st.success(f"Для {inf['name']} (вес {inf['weight']} кг):")
            
            st.write(f"Скорость поступления: **{inf['min_mcg']:.1f} – {inf['max_mcg']:.1f} мкг/мин**") # infusion rate:
            st.info(f"В миллилитрах: **{inf['min_ml']:.4f} – {inf['max_ml']:.4f} мл/мин**")
            
            if st.button("💾 Сохранить в карточку (инфузия)"):  # Save to chart
                if inf['name'] == "":
                    st.error("Введите имя животного!")
                else:
                    detail_text = f"{inf['min_ml']:.4f}-{inf['max_ml']:.4f} мл/мин"
                    if add_patient_record(inf['name'], inf['species'], "Допамин", inf['weight'], detail_text, inf['max_ml'], "infusion"):
                        st.success(f"Инфузия сохранена для {inf['name']}!")
                        st.session_state.last_infusion = None

with tab2:
    st.header("Мои пациенты")  # My patients
    df_patients, df_prescriptions = get_all_patients()
    
    if df_patients.empty:
        st.info("В базе пока нет пациентов.")  # No patients in the db yet
    else:
        total_patients = len(df_patients)
        if total_patients >= 30:
            st.warning(f"⚠️ В базе уже {total_patients} животных. Чтобы список не стал слишком длинным, рекомендуем удалять вылеченных пациентов (не забудьте перед этим сохранить историю в Excel).")
            # db has X patients. To keep the list short, delete discharged pets (export to Excel first)
        
        col_exp, col_clear = st.columns(2)
        with col_exp:
            export_df = pd.merge(
                df_prescriptions, 
                df_patients[['id', 'name', 'species']], 
                left_on='patient_id', 
                right_on='id', 
                suffixes=('_record', '_patient')
            )
            export_df = export_df[['name', 'species', 'drug', 'weight', 'detail', 'dose', 'type']]
            export_df.columns = ['Имя', 'Вид', 'Препарат', 'Вес (кг)', 'Кратность/Объем', 'Доза', 'Тип']

            buffer = io.BytesIO() # in-memory file 
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False, sheet_name='Назначения')
            
            st.download_button(
                label="📥 Скачать в Excel",
                data=buffer.getvalue(),
                file_name="vet_history.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col_clear:
            if st.button("🗑️ Очистить базу", use_container_width=True):  # Clear db
                clear_db()
                st.rerun()

        for _, patient in df_patients.iterrows():
            patient_records = df_prescriptions[df_prescriptions['patient_id'] == patient['id']]
            
            with st.expander(f"🐾 {patient['name']} ({patient['species']})"):
                for _, record in patient_records.iterrows():
                    if record["type"] == "injection":
                        st.write(f"💊 **{record['drug']}**: {record['dose']:.2f} мл ({record['detail']})")
                    else:
                        st.write(f"💧 **{record['drug']} (инфузия)**: {record['detail']}")
                    st.caption(f"Вес: {record['weight']} кг")
                
                st.divider()
                if st.button(f"❌ Удалить {patient['name']}", key=f"del_{patient['id']}"):
                    delete_patient_from_db(patient['name'])
                    st.rerun()