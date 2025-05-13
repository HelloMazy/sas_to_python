# app/converter.py
import re

def convert_proc_sql(sas):
    matches = re.findall(
        r"proc sql;.*?create table (\w+) as\s*select (.*?)\s*from (\w+)\s*where (.*?);.*?quit;",
        sas, re.DOTALL | re.IGNORECASE
    )
    results = []
    for table, columns, source, condition in matches:
        py_code = f"{table} = {source}[{source}[\"{condition.strip()}\"]][[{', '.join([f'{col.strip()}' for col in columns.split(',')])}]]"
        results.append(py_code)
    return "\n".join(results)

def convert_data_step(sas):
    matches = re.findall(
        r"data (\w+);\s*set (\w+);\s*if (.*?) then (\w+) = '(.*?)';\s*else (\w+) = '(.*?)';\s*run;",
        sas, re.DOTALL | re.IGNORECASE
    )
    results = []
    for new_table, source, condition, target1, val1, target2, val2 in matches:
        if target1 == target2:
            py_code = f"{source}['{target1}'] = {source}.apply(lambda row: '{val1}' if {condition} else '{val2}', axis=1)\n{new_table} = {source}"
        else:
            py_code = f"# ⚠️ Cas complexe non géré automatiquement : {target1} vs {target2}"
        results.append(py_code)
    return "\n".join(results)

def convert_input_functions(sas):
    matches = re.findall(r"(\w+)\s*=\s*input\((\w+),\s*\w+\);", sas, re.IGNORECASE)
    results = []
    for new_col, old_col in matches:
        results.append(f"df['{new_col}'] = df['{old_col}'].astype(float)")
    return "\n".join(results)

def convert_sas_to_python(sas_code):
    parts = [
        convert_proc_sql(sas_code),
        convert_data_step(sas_code),
        convert_input_functions(sas_code)
    ]
    return "\n\n".join([p for p in parts if p])
