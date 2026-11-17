DRUGS_DB = {
    "Транексам": {"min_d": 10, "max_d": 15, "unit": "мг", "conc": 50},
    "Аминокапроновая кислота": {"min_d": 100, "max_d": 100, "unit": "мг", "conc": 50},
    "Gs сухая форма": {"min_d": 8, "max_d": 15, "unit": "мг", "conc": [10, 20, 30]}, 
    "Атропин": {"min_d": 0.025, "max_d": 0.025, "unit": "мг", "conc": 1},
    "Адреналин": {"min_d": 20, "max_d": 20, "unit": "мкг", "conc": 1},
    "Кордиамин": {"min_d": 0.025, "max_d": 0.04, "unit": "мл", "conc": None},
    "Димедрол (кошки)": {"min_d": 0.025, "max_d": 0.025, "unit": "мл", "conc": None},
    "Димедрол (собаки)": {"min_d": 0.05, "max_d": 0.05, "unit": "мл", "conc": None},
    "Преднизолон (2мг/кг)": {"min_d": 2, "max_d": 2, "unit": "мг", "conc": 30},
    "Преднизолон (4мг/кг)": {"min_d": 4, "max_d": 4, "unit": "мг", "conc": 30},
    "Пиро-стоп": {"min_d": 0.25, "max_d": 0.25, "unit": "мл", "conc": None},
    "Метронидазол": {"min_d": 12.5, "max_d": 12.5, "unit": "мг", "conc": 5},
    "Азитромицин": {"min_d": 8, "max_d": 8, "unit": "мг", "conc": 80},
    "Цефтриаксон": {"min_d": 50, "max_d": 50, "unit": "мг", "conc": 200}, 
    "Трамадол (кошки)": {"min_d": 2, "max_d": 4, "unit": "мг", "conc": 50},
    "Трамадол (собаки)": {"min_d": 2, "max_d": 5, "unit": "мг", "conc": 50},
    "Пропофол": {"min_d": 6, "max_d": 8, "unit": "мг", "conc": 10},
    "Реамберин": {"min_d": 6, "max_d": 8, "unit": "мл", "conc": None},
    "Gs влажная форма": {"min_d": 5, "max_d": 15, "unit": "мг", "conc": [10, 20, 30]},
    "Gs офтальмологическая": {"min_d": 10, "max_d": 20, "unit": "мг", "conc": [10, 20, 30]},
    "Gs неврологическая": {"min_d": 12, "max_d": 20, "unit": "мг", "conc": [10, 20, 30]},
    "Ронколейкин": {"min_d": 12000, "max_d": 12000, "unit": "МЕ", "conc": [50000, 100000, 200000, 250000, 500000]},
    "Адеметионин": {"min_d": 20, "max_d": 20, "unit": "мг", "conc": 80}, 
}


'''
List of medications: Tranexamic acid, Aminocaproic acid, GS-441524 (dry form), Atropine,
Adrenaline, Cordiamine, Diphenhydramine (cats), Diphenhydramine (dogs), Prednisolone (2 mg/kg), 
Prednisolone (4 mg/kg), Piro-Stop (Imidocarb), Metronidazole, Azithromycin, Ceftriaxone, 
Tramadol (cats), Tramadol (dogs), Propofol, Reamberin, GS-441524 (wet form), GS-441524 (ocular form),
GS-441524 (neurological form), Roncoleukin, Ademetionine.
'''

'''
'unit' indicates the measurement unit for the dosage. There are 4 main types:
- 'мг' (mg): dosage is specified in mg per kg, but must be converted to ml (for syringe)
- 'мл' (ml): dosage is simply multiplied by body weight
- 'мкг' (mkg): very small dosage, requires additional conversion
- 'МЕ' (IU): International Units, for biological preparations
'''