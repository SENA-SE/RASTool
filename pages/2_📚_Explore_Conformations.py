# Importing the installed libraries
import streamlit as st
from stmol import *
import pandas as pd
import numpy as np
import os
import re
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

def queryBySW_list(df, sw1, sw2, col_name, unique=False):
    # 获取 pdb_code 为  的所有行
    selected_pdb = df[(df['SW1'] == sw1) & (df['SW2'] == sw2)]
    # 提取这些行中  列的值
    if unique:
        required_values_list = list(selected_pdb[col_name].unique())
    else:
        required_values_list = list(selected_pdb[col_name].tolist())

    required_values_list = ["None" if pd.isnull(x) else x for x in required_values_list]
    return required_values_list

def queryBySW1_list(df,  sw1, col_name, unique=False):
    # 获取 pdb_code 为  的所有行
    selected_pdb = df[ (df['SW1'] == sw1)]
    # 提取这些行中  列的值
    if unique:
        required_values_list = list(selected_pdb[col_name].unique())
    else:
        required_values_list = list(selected_pdb[col_name].tolist())

    required_values_list = ["None" if pd.isnull(x) else x for x in required_values_list]
    return required_values_list

def queryBySW2_list(df,  sw2, col_name, unique=False):
    # 获取 pdb_code 为  的所有行
    selected_pdb = df[ (df['SW2'] == sw2)]
    # 提取这些行中  列的值
    if unique:
        required_values_list = list(selected_pdb[col_name].unique())
    else:
        required_values_list = list(selected_pdb[col_name].tolist())

    required_values_list = ["None" if pd.isnull(x) else x for x in required_values_list]
    return required_values_list

st.markdown("## Explore Conformations")
st.markdown("---")
table1 = {
    'Conformation Label': ['Y71out.0P-GEF', 'Y71out.2P-SP2-A', 'Y71in.2P-SP12', 'Y71out.2P-SP2-B', 'Y71out.2P-BINDER', 'Y71in.3P-R', 'Y71in.3P-SP12-A', 'Y71out.3P-T', 'Y71in.3P-SP12-B', 'Outlier', 'Disordered', 'All'],
    'Y32out.0P-GEF': [23, None, None, None, None, None, None, None, None, None, None, 23],
    'Y32out.2P-OFF': [None, 38, 20, 20, 12, None, None, None, None, 70, 33, 193],
    'Y32in.3P-ON': [None, None, None, None, None,101, 31, 20, 12, 53, 60, 277],
    'Outlier': [29, 1, None, None, 1, 4, 1, None, None, 93, 27, 156],
    'Disordered': [None, None, None, None, None, None, None, None, None, 54, 64, 118],
    'All': [52, 39, 20, 20, 13, 105, 32, 20, 12, 270, 184, 767]
}

# 创建一个数据框
table1_df = pd.DataFrame(table1)

# 在Streamlit中显示表格
st.dataframe(table1_df,hide_index=True)
st.sidebar.markdown(
        """
    Explore RAS SW1 and SW2 conformations found in the PDB based on nucleotide state
    """
    )

# 指定文件夹路径
folder_path = ".\Resources"

# 构建文件路径
file_path = os.path.join(folder_path, 'entry.tsv')

# 使用 Pandas 读取 .tsv 文件为 DataFrame
df = pd.read_csv(file_path, sep='\t')

expander1=st.expander(f"0P Conformations (Nucleotide-Free)", expanded=True)
expander1.markdown("### 0P Conformations (Nucleotide-Free)")

left_col, right_col = expander1.columns(2)
left_col.markdown("##### SW1 Conformation (Only 1)")
con_name_1 = left_col.selectbox("Conformation Name", ["Y32out.2P-OFF"])
conf0_sw1_list= queryBySW_list(df, "Y32out.0P-GEF","Y71out.0P-GEF", "pdb_id")
pdb_id = left_col.selectbox(
    "PDB ID", [x.upper() for x in conf0_sw1_list]
)
chainid = pdb_id[-1].upper()
pdb_code = pdb_id[:4]
style_lst = list()
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
hl_resi_list = [32,71]

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

view = py3Dmol.view(query=f"pdb:{pdb_code.lower()}", width=500, height=300)

view.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst is not None:
        for style in style_lst:
            view.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid}

view.zoomTo(zoom_dict)
view.zoom()
with left_col:
     showmol(view, height=300, width=500)
table2 = {
    'Bound Protein': ['GEF.CDC25', 'All'],
    'HRAS': [23, 23],
    'All': [23, 23]
}
table3 = {
    'Inhibitor Chemistry': ['None', 'All'],
    'HRAS': [23, 23],
    'All': [23, 23]
}
table4 = {
    'Bound Protein': ['GEF.CDC25', 'All'],
    'KRAS': [6, 6],
    'HRAS': [46, 46],
    'All': [52, 52]
}
table5 = {
    'Inhibitor Chemistry': ['SP12.Unclassified', 'Other', 'None', 'All'],
    'KRAS': [None, None, 6, 6],
    'HRAS': [1, 3, 42, 46],
    'All': [1, 3, 48, 52]
}

# 创建一个数据框
table5_df = pd.DataFrame(table5)
# 创建一个数据框
table4_df = pd.DataFrame(table4)

# 创建一个数据框
table3_df = pd.DataFrame(table3)
table2_df = pd.DataFrame(table2)

tb2_col, tb3_col = left_col.columns(2)
tb2_col.dataframe(table2_df,hide_index=True)
tb3_col.dataframe(table3_df,hide_index=True)


##0 right
conf0_sw2_list = queryBySW2_list(df, "Y71out.0P-GEF", "pdb_id")
right_col.markdown("##### SW1 Conformation (Only 1)")
con_name_2 = right_col.selectbox("Conformation Name", ["Y71out.0P-GEF"])
pdb_id_2 = right_col.selectbox(
    "PDB ID", [x.upper() for x in conf0_sw2_list]
)
chainid_2 = pdb_id_2[-1].upper()
pdb_code_2 = pdb_id_2[:4]
style_lst_2 = list()
style_lst_2.append(
        [
            {
                "chain": chainid_2,
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
hl_resi_list_2 = [32,71]

if hl_resi_list_2 is not None:
                style_lst_2.append(
                [
                    {"chain": chainid_2,
                    "resi": hl_resi_list_2,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst_2.append(
                    [
                        {"chain": chainid_2, "resi": hl_resi_list_2},
                        {"stick": {"radius": 0.2}},
                    ]
                )

view2 = py3Dmol.view(query=f"pdb:{pdb_code_2.lower()}", width=500, height=300)

view2.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view2.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view2.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst_2 is not None:
        for style in style_lst_2:
            view2.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid_2}

view2.zoomTo(zoom_dict)
view2.zoom()
with right_col:
     showmol(view2, height=300, width=500)

tb4_col, tb5_col = right_col.columns(2)
tb4_col.dataframe(table4_df,hide_index=True)
tb5_col.dataframe(table5_df,hide_index=True)
# print(len(test))



expander2=st.expander(f"1P Conformations (GDP-Bound)", expanded=True)
expander2.markdown("### 1P Conformations (GDP-Bound)")

left2_col, right2_col = expander2.columns(2)
left2_col.markdown("##### SW1 Conformation (Only 1)")
con1_name_1 = left2_col.selectbox("Conformation Name", ["Y32out.2P-OFF"], key="con1_name_1")
conf1_sw1_list= queryBySW1_list(df, con1_name_1, "pdb_id")
pdb_id_3 = left2_col.selectbox(
    "PDB ID", [x.upper() for x in conf1_sw1_list]
)
chainid_3 = pdb_id_3[-1].upper()
pdb_code_3 = pdb_id_3[:4]
style_lst_3 = list()
style_lst_3.append(
        [
            {
                "chain": chainid_3,
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
hl_resi_list_3 = [32,71]

if hl_resi_list_3 is not None:
                style_lst_3.append(
                [
                    {"chain": chainid_3,
                    "resi": hl_resi_list_3,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst_3.append(
                    [
                        {"chain": chainid_3, "resi": hl_resi_list_3},
                        {"stick": {"radius": 0.2}},
                    ]
                )
view3 = py3Dmol.view(query=f"pdb:{pdb_code_3.lower()}", width=500, height=300)

view3.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view3.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view3.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst_3 is not None:
        for style in style_lst_3:
            view3.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid_3}

view3.zoomTo(zoom_dict)
view3.zoom()

with left2_col:
     showmol(view3, height=300, width=500)


right2_col.markdown("##### SW2 Conformation (4 in total)")
con1_name_2 = right2_col.selectbox("Conformation Name", ["Y71out.2P-SP2-A","Y71in.2P-SP12","Y71out.2P-SP2-B","Y71out.2P-BINDER"], key="con1_name_2")
conf1_sw2_list = queryBySW2_list(df, con1_name_2, "pdb_id")
pdb_id_4 = right2_col.selectbox(
    "PDB ID", [x.upper() for x in conf1_sw2_list]
)
chainid_4 = pdb_id_4[-1].upper()
pdb_code_4 = pdb_id_4[:4]
style_lst_4 = list()
style_lst_4.append(
        [
            {
                "chain": chainid_4,
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
hl_resi_list_4 = [32,71]

if hl_resi_list_4 is not None:
                style_lst_4.append(
                [
                    {"chain": chainid_4,
                    "resi": hl_resi_list_4,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst_4.append(
                    [
                        {"chain": chainid_4, "resi": hl_resi_list_4},
                        {"stick": {"radius": 0.2}},
                    ]
                )
view4 = py3Dmol.view(query=f"pdb:{pdb_code_4.lower()}", width=500, height=300)

view4.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view4.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view4.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst_4 is not None:
        for style in style_lst_3:
            view4.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid_3}

view4.zoomTo(zoom_dict)
view4.zoom()

with right2_col:
     showmol(view4, height=300, width=500)



expander3=st.expander(f"2P Conformations (GDP-Bound)", expanded=True)
expander3.markdown("### 2P Conformations (GDP-Bound)")

left3_col, right3_col = expander3.columns(2)
left3_col.markdown("##### SW1 Conformation (Only 1)")
con2_name_1 = left3_col.selectbox("Conformation Name", ["Y32in.3P-ON"], key="con2_name_1")
conf2_sw1_list= queryBySW1_list(df, con2_name_1, "pdb_id")
pdb_id_4 = left3_col.selectbox(
    "PDB ID", [x.upper() for x in conf2_sw1_list]
)
chainid_4 = pdb_id_4[-1].upper()
pdb_code_4 = pdb_id_4[:4]
style_lst_4 = list()
style_lst_4.append(
        [
            {
                "chain": chainid_4,
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
hl_resi_list_4 = [32,71]

if hl_resi_list_4 is not None:
                style_lst_4.append(
                [
                    {"chain": chainid_4,
                    "resi": hl_resi_list_4,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst_4.append(
                    [
                        {"chain": chainid_4, "resi": hl_resi_list_4},
                        {"stick": {"radius": 0.2}},
                    ]
                )

view4 = py3Dmol.view(query=f"pdb:{pdb_code_4.lower()}", width=500, height=300)

view4.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view4.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view4.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst_4 is not None:
        for style in style_lst_4:
            view4.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid_4}

view4.zoomTo(zoom_dict)
view4.zoom()

with left3_col:
     showmol(view4, height=300, width=500)




right3_col.markdown("##### SW2 Conformation (4 in total)")
con2_name_2 = right3_col.selectbox("Conformation Name", ["Y71in.3P-R","Y71in.3P-SP12-A","Y71out.3P-T","Y71in.3P-SP12-B"], key="con2_name_2")
conf2_sw2_list = queryBySW2_list(df, con2_name_2, "pdb_id")
pdb_id_5 = right3_col.selectbox(
    "PDB ID", [x.upper() for x in conf2_sw2_list]
)
chainid_5 = pdb_id_5[-1].upper()
pdb_code_5 = pdb_id_5[:4]
style_lst_5 = list()
style_lst_5.append(
        [
            {
                "chain": chainid_5,
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
hl_resi_list_5 = [32,71]

if hl_resi_list_5 is not None:
                style_lst_5.append(
                [
                    {"chain": chainid_5,
                    "resi": hl_resi_list_5,
                    "elem": "C"},
                    {"stick": {"colorscheme": "amino", "radius": 0.2}},
                ]
            ) 
                style_lst_5.append(
                    [
                        {"chain": chainid_5, "resi": hl_resi_list_5},
                        {"stick": {"radius": 0.2}},
                    ]
                )
view5 = py3Dmol.view(query=f"pdb:{pdb_code_5.lower()}", width=500, height=300)

view5.setStyle(
        {
            "cartoon": {
                "style": "oval",
                "color": "lightgray",
                "thickness": 0.2,
                "opacity": 0.5
            }
        }
    )

view5.addStyle({"elem": "C", "hetflag": True},
                {"stick": {"color": "white", "radius": 0.2}})

view5.addStyle({"hetflag": True},
                    {"stick": {"radius": 0.2}})

if style_lst_5 is not None:
        for style in style_lst_3:
            view5.addStyle(
                style[0],
                style[1],
            )

    
zoom_dict = {"chain": chainid_3}

view5.zoomTo(zoom_dict)
view5.zoom()

with right3_col:
     showmol(view5, height=300, width=500)