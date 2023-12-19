import pandas as pd
import numpy as np
import os

# 指定文件夹路径
folder_path = ".\Resources"

# 构建文件路径
file_path = os.path.join(folder_path, 'entry.tsv')

# 使用 Pandas 读取 .tsv 文件为 DataFrame
df = pd.read_csv(file_path, sep='\t')

# 显示 DataFrame 的前几行
# print(df.head())

# 打印列表
# print(pdb_code_list)

sw1_resids = "25-40"
sw2_resids = "56-76"

sw1_color = "#e7298a"
sw2_color = "#7570b3"
mut_color = "#d62728"
def col_list(df, col_name, unique=False):
    if unique:
        result = list(df[col_name].unique())
    else:
        result = list(df[col_name].to_list())
    return result

def queryByCode_list(df, pdb_code, col_name, unique=False):
    # 获取 pdb_code 为  的所有行
    selected_pdb = df[df['pdb_code'] == pdb_code.lower()]

    # 提取这些行中  列的值
    if unique:
        required_values_list = list(selected_pdb[col_name].unique())
    else:
        required_values_list = list(selected_pdb[col_name].tolist())

    required_values_list = ["None" if pd.isnull(x) else x for x in required_values_list]
    return required_values_list

def queryByChainId_list(df, pdb_code, chainId, col_name, unique=False):
    # 获取 pdb_code 为  的所有行
    selected_pdb = df[(df['pdb_code'] == pdb_code.lower()) & (df['chainid'] == chainId)]\
    # 提取这些行中  列的值
    if unique:
        required_values_list = list(selected_pdb[col_name].unique())
    else:
        required_values_list = list(selected_pdb[col_name].tolist())

    required_values_list = ["None" if pd.isnull(x) else x for x in required_values_list]
    return required_values_list

import re

def extract_numbers(s):
    # 使用正则表达式找到所有的数字
    numbers = re.findall(r'\d+', s)
    # 将数字字符串转换为整数
    numbers = [int(num) for num in numbers]
    return numbers


# 获取 pdb_code 列的所有内容并转换为列表
pdb_code_list = col_list(df, "pdb_code", True)

### Step 1) Imports

import streamlit as st
import py3Dmol
from stmol import showmol
st.markdown("""
    <style>
        .block-container {
            max-width: 70rem; 
        }
    </style>
""", unsafe_allow_html=True)
st.sidebar.markdown(
        """
    Search for specific PDB entries that include RAS structures
    """
    )

### Step 2) Streamlit
st.markdown("## View PDB")

st.markdown("---")


st.sidebar.title("View Settings")


pdb_code = st.sidebar.selectbox(
    "Entry", [x.upper() for x in pdb_code_list]
)
chainid = st.sidebar.selectbox("Chain", queryByCode_list(df, pdb_code, "chainid", True))

gene_class = queryByCode_list(df, pdb_code, "gene_class")[0]
mut_status = queryByCode_list(df, pdb_code, "mutation_status")[0]
general_info = {
    "Experiment Method": queryByCode_list(df, pdb_code, "method")[0] ,

    "Resolution": queryByCode_list(df, pdb_code, "resolution")[0],

    "R-Factor": queryByCode_list(df, pdb_code, "r_factor")[0] ,

    "Space Group": queryByCode_list(df, pdb_code, "crystal_form")[0] ,

    "Deposit Date": queryByCode_list(df, pdb_code, "deposit_data")[0] 
}

mole_anno = {
    "Nucleotide State":queryByCode_list(df, pdb_code, "nucleotide_class")[0],
    "Bound Protein":queryByCode_list(df, pdb_code, "protein_class")[0],
    "Inhibitor Site":queryByCode_list(df, pdb_code, "pocket_class")[0],
    "Inhibitor Chemistry":queryByCode_list(df, pdb_code, "match_class")[0],
    "Homodimer Status":queryByCode_list(df, pdb_code, "interface_class")[0]
}

sw = {
    "SW1 Conformation":queryByChainId_list(df, pdb_code, chainid, "SW1")[0],
    "SW2 Conformation":queryByChainId_list(df, pdb_code, chainid, "SW2")[0],
    "Y32 Position":queryByChainId_list(df, pdb_code, chainid, "Y32")[0],
    "Y71 Position":queryByChainId_list(df, pdb_code, chainid, "Y71")[0]
}
hl_resi_list = [32,71]
flexible_container = st.sidebar.container()



label_resi = st.sidebar.checkbox(label="Label Residues", value=True)
style = st.sidebar.selectbox('Style',['cartoon','line','cross','stick','sphere'])
surf_transp = st.sidebar.slider("Surface Transparency", min_value=0.0, max_value=1.0, value=0.0)
cartoon_trans = 1.0
cartoon_trans = st.sidebar.slider(
    "Cartoon Transparency", min_value=0.0, max_value=1.0, value=cartoon_trans
)

hl_color = "red"
bb_color = "lightgrey"
lig_color = "white"


spin_on = st.sidebar.checkbox("Rotate Structure", value=True)



st.markdown(f"### PDB: [{pdb_code.upper()}](https://www.rcsb.org/structure/{pdb_code}) (Chain {chainid}) - {gene_class}({mut_status})")

left_col, right_col = st.columns(2)

left_col.markdown("##### General Information")
for col in general_info:
    left_col.markdown(f"**{col}:** {general_info[col]}")

right_col.markdown("##### Molecular Annotations")
tmpDf = pd.DataFrame(list(mole_anno.items()), columns=['Molecular Content', 'Annotation'])
# hide index
hide_table_row_index = """
        <style>
        tbody th {display:none}
        .blank {display:none}
        </style>
"""
st.markdown(hide_table_row_index, unsafe_allow_html=True)
right_col.table(tmpDf)

st_col_lst = st.columns(4)
counter = 0
for col in sw:
        if col in ["SW1 Conformation", "Y32 Position"]:
            color = sw1_color
        elif col in ["SW2 Conformation", "Y71 Position"]:
            color = sw2_color
        st_col_lst[counter].markdown(f"##### {col}")
        st_col_lst[counter].markdown(f'<span style="font-family:sans-serif;  color:{color};">{sw[col]}</span>',unsafe_allow_html=True)
        counter= counter+1

st.markdown("---")

left_check_col, middle_check_col, right_check_col = st.columns(3)
left_check_col.markdown("##### Bound Ligands")

zoom_resids = None
cartoon_trans = 1.0
surface_trans = 0.0
zoom = 1.5

lig_check_dict = dict()
bound_lig = {
    "biological_ligand":queryByCode_list(df, pdb_code, "biological_ligand")[0],
    "ion_ligand":queryByCode_list(df, pdb_code, "ion_ligand")[0],
    "pharmacological_ligand":queryByCode_list(df, pdb_code, "pharmacological_ligand")[0],
    "chemical_ligand":queryByCode_list(df, pdb_code, "chemical_ligand")[0],
    "modification_ligand":queryByCode_list(df, pdb_code, "modification_ligand")[0],
    "membrane_ligand":queryByCode_list(df, pdb_code, "membrane_ligand")[0]
}

rename_bound_lig={
    "biological_ligand":"Nucleotide",
    "ion_ligand":"Ion",
    "pharmacological_ligand":"Inhibitor",
    "chemical_ligand":"Chemical",
    "modification_ligand":"Modification",
    "membrane_ligand":"Memberane"
}

# lig_check_dict是非none列表
# resn中含逗号时分割
for key, value in bound_lig.items():
    if(value != "None"):
        lig_check_dict[key] = left_check_col.checkbox(f"{rename_bound_lig[key]}: {value}")

if len(lig_check_dict.keys()) == 0:
    left_check_col.write("No bound ligands.")

add_reslabel = lig_check_dict
reslabel_lst = list()
for lig in lig_check_dict:
    if type(lig_check_dict) == dict:
        if lig in list(lig_check_dict.keys()):
            add_reslabel = lig_check_dict[lig]
    if add_reslabel:
        reslabel_lst.append(
            [
                {
                    "chain": chainid,
                    "resn": bound_lig[lig],
                },
                {
                    "backgroundColor": "lightgray",
                    "fontColor": "black",
                    "backgroundOpacity": 0.5,
                },
            ]
        )


middle_check_col.markdown("##### Bound Proteins")

prot_check_dict = dict()
bound_proteins_lst = queryByChainId_list(df, pdb_code,chainid, "bound_protein_chainid")
for prot in bound_proteins_lst:
    if(prot != "None"):
        prot_check_dict[prot] = middle_check_col.checkbox(f"Chain {prot}")

if len(prot_check_dict.keys()) == 0:
    middle_check_col.write("No bound proteins.")

#-- 1LFD
bound_protein_contacts = queryByChainId_list(df, pdb_code, chainid, "bound_protein_contacts")[0]
display_bound_protein = False

if bound_protein_contacts != "None":
    # middle_check_col.markdown("---")
    if flexible_container.checkbox("Display Bound Protein Site"):
                display_bound_protein = True
                bound_prot = flexible_container.selectbox("Select Inhibitor Site", bound_proteins_lst)
                # 使用冒号将字符串分割为两部分，然后取第二部分
                numbers_str = bound_protein_contacts.split(":")[1]

                # 使用逗号将字符串分割为多个部分，然后将每一部分转换为整数
                numbers = [int(x) for x in numbers_str.split(",")]
                # prot_cont_dict = str_to_dict(chainid_df[bound_prot_cont_col].iloc[0], return_int=True)

                hl_resi_list = numbers
                cartoon_trans = 0.5
                surface_trans = 0.0
                zoom = 1.0

label_lst = list()
for prot in prot_check_dict:
        if prot_check_dict[prot]:
                    prot_label = f"Chain {prot}"

                    label_lst.append(
                        [
                            prot_label,
                            {
                                "backgroundColor": "lightgray",
                                "fontColor": "black",
                                "backgroundOpacity": 0.8,
                            },
                            {"chain": f"{prot}"}
                        ]
                    )


right_check_col.markdown("##### Mutation Sites")

mut_check_dict = dict()
mutation_sites_lst = queryByChainId_list(df, pdb_code,chainid, "mutation_status")

for mut in mutation_sites_lst[0].split(","):
    if mut != "WT":
        mut_check_dict[mut] = right_check_col.checkbox(f"{mut}")
        
if len(mut_check_dict.keys()) == 0:
        right_check_col.write("Not mutated.")

label_muts = list()
style_lst = list()
for mut_resid in mut_check_dict:
    if mut_check_dict[mut_resid]:
            reslabel_lst.append(
                        [
                            {"chain": chainid,
                            "resi": extract_numbers(mut_resid)},
                            {
                                "backgroundColor": "lightgray",
                                "fontColor": "black",
                                "backgroundOpacity": 0.5,
                            },
                        ]
                    )
            style_lst.append(
                [
                    {"chain": chainid,
                    "resi": extract_numbers(mut_resid),
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
            style_lst.append(
                    [
                        {"chain": chainid, "resi": extract_numbers(mut_resid)},
                        {"stick": {"radius": 0.2}},
                    ]
                )




hl_resi_list = flexible_container.multiselect(label="Displayed Residues",options=list(range(1,5000)), default=hl_resi_list)
### Step 3) Py3Dmol

width = 700
height = 700

cartoon_radius = 0.2
stick_radius = 0.2


style_lst.append(
        [
            {
                "chain": chainid,
                "invert": True,
            },
            {
                "cartoon": {
                    "color": "#1b9e77",
                    "style": "oval",
                    "thickness": 0.2,
                    "opacity": 0.75,
                }
            },
        ]
)

style_lst.append(
        [
            {
                "chain": chainid,
            },
            {
                "cartoon": {
                    "color": "white",
                    "style": "oval",
                    "thickness": 0.2,
                    "opacity": cartoon_trans,
                }
            },
        ]
    )

if hl_resi_list is not None:
                style_lst.append(
                [
                    {"chain": chainid,
                    "resi": hl_resi_list,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst.append(
                    [
                        {"chain": chainid, "resi": hl_resi_list},
                        {"stick": {"radius": 0.2}},
                    ]
                )
if display_bound_protein:
    style_lst.append(
                [
                    {
                        "chain": bound_prot,
                    },
                    {
                        "cartoon": {
                            "style": "oval",
                            "color": sw2_color,
                            "thickness": 0.2,
                            "opacity": 1,
                        }
                    },
                ]
            )
view = py3Dmol.view(query=f"pdb:{pdb_code.lower()}", width=width, height=height)



view.setStyle(
        {
            style: {
                "style": "oval",
                "color": "lightgray",
                "thickness": cartoon_radius,
                "opacity": cartoon_trans
            }
        }
    )

view.addSurface(py3Dmol.VDW, {"opacity": surf_transp, "color": bb_color},{"hetflag": False})

view.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": lig_color, "radius": stick_radius}})

view.addStyle({"hetflag": True},
                    {"stick": {"radius": stick_radius}})

if reslabel_lst is not None:
    for reslabel in reslabel_lst:
        view.addResLabels(reslabel[0], reslabel[1])
if label_lst is not None:
        for label in label_lst:
            view.addLabel(label[0], label[1], label[2])

if style_lst is not None:
        for style in style_lst:
            view.addStyle(
                style[0],
                style[1],
            )
# zoom_dict = {"chain": "A"}

# # if zoom_resids is not None:
# #     if type(zoom_resids) == dict:
# #         zoom_dict = merge_dicts([zoom_dict, zoom_resids])
# #     else:
#         # zoom_dict["resi"] = zoom_resids

# if zoom_dict is None:
#         view.zoomTo()
# else:
#         view.zoomTo(zoom_dict)

view.spin(spin_on)
for hl_resi in hl_resi_list:
    view.addStyle({"chain": chainid, "resi": hl_resi, "elem": "C"},
                    {"stick": {"color": hl_color, "radius": stick_radius}})

    view.addStyle({"chain": chainid, "resi": hl_resi},
                        {"stick": {"radius": stick_radius}})

if label_resi:
    for hl_resi in hl_resi_list:
        view.addResLabels({"chain": chainid,"resi": hl_resi},
        {"backgroundColor": "lightgray","fontColor": "black","backgroundOpacity": 0.5})

### Step 4) Stmol

showmol(view, height=height, width=width)