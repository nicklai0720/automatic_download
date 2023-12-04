from __future__ import annotations
from typing import Iterable
import gradio as gr
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
import datetime
import calendar
import pandas as pd
from datascratch import data_export
from zipfile import ZipFile
import os

from theme_dropdown import create_theme_dropdown


class Seafoam(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.emerald,
        secondary_hue: colors.Color | str = colors.blue,
        neutral_hue: colors.Color | str = colors.blue,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            # body_background_fill="repeating-linear-gradient(45deg, *primary_200, *primary_200 10px, *primary_50 10px, "
            #                      "*primary_50 20px)",
            body_background_fill="repeating-linear-gradient(45deg, *primary_200, *primary_200 10px, "
                                 "*primary_200 10px, *primary_200 20px)",
            body_background_fill_dark="repeating-linear-gradient(45deg, *primary_800, *primary_800 10px, "
                                      "*primary_900 10px, *primary_900 20px)",
            button_primary_background_fill="linear-gradient(90deg, *primary_300, *secondary_400)",
            button_primary_background_fill_hover="linear-gradient(90deg, *primary_200, *secondary_300)",
            button_primary_text_color="white",
            button_primary_background_fill_dark="linear-gradient(90deg, *primary_600, *secondary_800)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="3px",
            block_shadow="*shadow_drop_lg",
            button_shadow="*shadow_drop_lg",
            button_large_padding="32px",
        )


def get_month_dates(year, month):
    num_days = calendar.monthrange(year, month)[1]
    dates = []
    for day in range(1, num_days + 1):
        date = datetime.date(year, month, day)
        dates.append(date)
    return dates


def replace_dict_with_zero(value):
    if isinstance(value, dict):
        return 0
    return value


def download_files_A(x):
    excel_file = pipe_A_data(x)
    excel_file.to_excel('tmp_excel_file.xlsx')
    with ZipFile("甲棟壓縮檔.zip", "w") as zipObj:
        zipObj.write('tmp_excel_file.xlsx', '甲棟.xlsx')
    os.remove('tmp_excel_file.xlsx')
    return "甲棟壓縮檔.zip", gr.File(visible=True)


def download_files_B(x):
    excel_file = pipe_B_data(x)
    excel_file.to_excel('tmp_excel_file.xlsx')
    with ZipFile("乙棟壓縮檔.zip", "w") as zipObj:
        zipObj.write('tmp_excel_file.xlsx', '乙棟.xlsx')
    os.remove('tmp_excel_file.xlsx')
    return "乙棟壓縮檔.zip", gr.File(visible=True)


def download_files_C(x):
    excel_file = pipe_C_data(x)
    excel_file.to_excel('tmp_excel_file.xlsx')
    with ZipFile("丙棟壓縮檔.zip", "w") as zipObj:
        zipObj.write('tmp_excel_file.xlsx', '丙棟.xlsx')
    os.remove('tmp_excel_file.xlsx')
    return "丙棟壓縮檔.zip", gr.File(visible=True)


def pipe_A_data(x):
    A_class = ["HJ02", "HJ03", "HJ04", "HJ05", "HJ06", "HJ07", "HJ08", "HJ09", "HJ10", "HJ11", "HJ12",
               "HJ61", "HJ62", "HJ63", "HJ64", "HJ65", "HJ66", "HJ67", "HJ68", "HJ69", "HJ70", "HJ71",
               "HJ72", "HJ73", "HJ74"]
    year = x.split('-')[0]
    month = x.split('-')[-1]
    for i in A_class:
        en = []
        rpa = f"RPA_{i}_TIC01_RKC_READ_PV"
        en.append(rpa)
        globals()[i + "_en"] = en
    pisource = 'pi:\\10.114.134.1\\'
    for i in A_class:
        globals()[i + "_pitag"] = [pisource + element for element in globals()[i + "_en"]]

    tag = [HJ02_pitag, HJ03_pitag, HJ04_pitag, HJ05_pitag, HJ06_pitag, HJ07_pitag, HJ08_pitag, HJ09_pitag, HJ10_pitag,
           HJ11_pitag, HJ12_pitag, HJ61_pitag, HJ62_pitag, HJ63_pitag, HJ64_pitag, HJ65_pitag, HJ66_pitag, HJ67_pitag,
           HJ68_pitag, HJ69_pitag, HJ70_pitag, HJ71_pitag, HJ72_pitag, HJ73_pitag, HJ74_pitag]

    time_format = '%Y-%m-%d %H:%M:%S'

    dates = get_month_dates(int(year), int(month))

    pi_df = pd.DataFrame()

    for date in dates:
        start = datetime.datetime.combine(date, datetime.time(11, 0)) - datetime.timedelta(minutes=0)
        end = datetime.datetime.combine(date, datetime.time(11, 0))

        start_time = start.strftime(time_format)  # 注意这里使用了 strftime
        end_time = end.strftime(time_format)  # 注意这里使用了 strftime

        temp_rpa = pd.DataFrame()

        for i in tag:
            pi_data = data_export(start_time=start_time,
                                  end_time=end_time,
                                  tagpoint_list=i,
                                  time_interval='1m').iloc[-1:, :]
            temp_rpa = pd.concat([temp_rpa, pi_data], axis=1)

        new_row = pd.DataFrame(temp_rpa.values, columns=temp_rpa.columns)

        pi_df = pd.concat([pi_df, new_row], ignore_index=True)

    pi_df.index = pi_df.index + 1

    pi_df = pi_df.applymap(replace_dict_with_zero)

    pi_df = pi_df.rename(columns={'RPA_HJ02_TIC01_RKC_READ_PV': "HJ02",
                                  'RPA_HJ03_TIC01_RKC_READ_PV': "HJ03",
                                  'RPA_HJ04_TIC01_RKC_READ_PV': "HJ04",
                                  'RPA_HJ05_TIC01_RKC_READ_PV': "HJ05",
                                  'RPA_HJ06_TIC01_RKC_READ_PV': "HJ06",
                                  'RPA_HJ07_TIC01_RKC_READ_PV': "HJ07",
                                  'RPA_HJ08_TIC01_RKC_READ_PV': "HJ08",
                                  'RPA_HJ09_TIC01_RKC_READ_PV': "HJ09",
                                  'RPA_HJ10_TIC01_RKC_READ_PV': "HJ10",
                                  'RPA_HJ11_TIC01_RKC_READ_PV': "HJ11",
                                  'RPA_HJ12_TIC01_RKC_READ_PV': "HJ12",
                                  'RPA_HJ61_TIC01_RKC_READ_PV': "HJ61",
                                  'RPA_HJ62_TIC01_RKC_READ_PV': "HJ62",
                                  'RPA_HJ63_TIC01_RKC_READ_PV': "HJ63",
                                  'RPA_HJ64_TIC01_RKC_READ_PV': "HJ64",
                                  'RPA_HJ65_TIC01_RKC_READ_PV': "HJ65",
                                  'RPA_HJ66_TIC01_RKC_READ_PV': "HJ66",
                                  'RPA_HJ67_TIC01_RKC_READ_PV': "HJ67",
                                  'RPA_HJ68_TIC01_RKC_READ_PV': "HJ68",
                                  'RPA_HJ69_TIC01_RKC_READ_PV': "HJ69",
                                  'RPA_HJ70_TIC01_RKC_READ_PV': "HJ70",
                                  'RPA_HJ71_TIC01_RKC_READ_PV': "HJ71",
                                  'RPA_HJ72_TIC01_RKC_READ_PV': "HJ72",
                                  'RPA_HJ73_TIC01_RKC_READ_PV': "HJ73",
                                  'RPA_HJ74_TIC01_RKC_READ_PV': "HJ74"})
    pi_df_T = pi_df.T

    # pi_df_T.to_excel('temp_A.xlsx')

    pi_df_T.columns = pi_df_T.columns.astype(str)

    return pi_df_T


def pipe_B_data(x):
    B_class = ["HJ15", "HJ16", "HJ17", "HJ18", "HJ19", "HJ20", "HJ21", "HJ22", "HJ23", "HJ24", "HJ25", "HJ26", "HJ27",
               "HJ28", "HJ29", "HJ30", "HJ31"]
    year = x.split('-')[0]
    month = x.split('-')[-1]
    for i in B_class:
        en_B = []
        rpb = f"RPB_{i}_TIC01_RKC_READ_PV"
        en_B.append(rpb)
        globals()[i + "_en"] = en_B
    pisource = 'pi:\\10.114.134.1\\'
    for i in B_class:
        globals()[i + "_pitag"] = [pisource + element for element in globals()[i + "_en"]]

    tag_B = [HJ15_pitag, HJ16_pitag, HJ17_pitag, HJ18_pitag, HJ19_pitag, HJ20_pitag, HJ21_pitag, HJ22_pitag, HJ23_pitag,
             HJ24_pitag, HJ25_pitag, HJ26_pitag, HJ27_pitag, HJ28_pitag, HJ29_pitag, HJ30_pitag, HJ31_pitag]

    time_format = '%Y-%m-%d %H:%M:%S'

    dates = get_month_dates(int(year), int(month))

    pi_df_B = pd.DataFrame()

    for date in dates:
        start = datetime.datetime.combine(date, datetime.time(11, 0)) - datetime.timedelta(minutes=0)
        end = datetime.datetime.combine(date, datetime.time(11, 0))

        start_time = start.strftime(time_format)  # 注意这里使用了 strftime
        end_time = end.strftime(time_format)  # 注意这里使用了 strftime

        temp_rpb = pd.DataFrame()

        for i in tag_B:
            pi_data = data_export(start_time=start_time,
                                  end_time=end_time,
                                  tagpoint_list=i,
                                  time_interval='1m').iloc[-1:, :]
            temp_rpb = pd.concat([temp_rpb, pi_data], axis=1)

        new_row_B = pd.DataFrame(temp_rpb.values, columns=temp_rpb.columns)

        pi_df_B = pd.concat([pi_df_B, new_row_B], ignore_index=True)

    pi_df_B.index = pi_df_B.index + 1

    pi_df_B = pi_df_B.applymap(replace_dict_with_zero)

    pi_df_B = pi_df_B.rename(columns={'RPB_HJ15_TIC01_RKC_READ_PV': "HJ15",
                                      'RPB_HJ16_TIC01_RKC_READ_PV': "HJ16",
                                      'RPB_HJ17_TIC01_RKC_READ_PV': "HJ17",
                                      'RPB_HJ18_TIC01_RKC_READ_PV': "HJ18",
                                      'RPB_HJ19_TIC01_RKC_READ_PV': "HJ19",
                                      'RPB_HJ20_TIC01_RKC_READ_PV': "HJ20",
                                      'RPB_HJ21_TIC01_RKC_READ_PV': "HJ21",
                                      'RPB_HJ22_TIC01_RKC_READ_PV': "HJ22",
                                      'RPB_HJ23_TIC01_RKC_READ_PV': "HJ23",
                                      'RPB_HJ24_TIC01_RKC_READ_PV': "HJ24",
                                      'RPB_HJ25_TIC01_RKC_READ_PV': "HJ25",
                                      'RPB_HJ26_TIC01_RKC_READ_PV': "HJ26",
                                      'RPB_HJ27_TIC01_RKC_READ_PV': "HJ27",
                                      'RPB_HJ28_TIC01_RKC_READ_PV': "HJ28",
                                      'RPB_HJ29_TIC01_RKC_READ_PV': "HJ29",
                                      'RPB_HJ30_TIC01_RKC_READ_PV': "HJ30",
                                      'RPB_HJ31_TIC01_RKC_READ_PV': "HJ31"})
    pi_df_B = pi_df_B.T

    # pi_df_B.to_excel('temp_B.xlsx')

    pi_df_B.columns = pi_df_B.columns.astype(str)

    return pi_df_B


def pipe_C_data(x):
    C_class_1 = ["HJ84"]
    C_class_2 = ["HJ83", "HJ82", "HJ81", "HJ75", "HJ76", "HJ78", "HJ79"]
    C_class_3 = ["HJ44", "HJ45", "HJ46", "HJ47", "HJ48", "HJ49"]
    year = x.split('-')[0]
    month = x.split('-')[-1]
    for i in C_class_1:
        en = []
        rpc = f"RPC_{i}_L_TIC01_RKC_READ_PV"
        en.append(rpc)
        globals()[i + "_en"] = en

    for i in C_class_2:
        en = []
        rpc2 = f"RPC_{i}_TIC01_RKC_READ_PV"
        en.append(rpc2)
        globals()[i + "_en"] = en

    for i in C_class_3:
        en = []
        rpc4 = f"RPC_{i}_M_TIC01_RKC_READ_PV"
        en.append(rpc4)
        globals()[i + "_en"] = en

    pisource = 'pi:\\10.114.134.1\\'

    for i in C_class_1:
        globals()[i + "_pitag"] = [pisource + element for element in globals()[i + "_en"]]

    for i in C_class_2:
        globals()[i + "_pitag"] = [pisource + element for element in globals()[i + "_en"]]

    for i in C_class_3:
        globals()[i + "_pitag"] = [pisource + element for element in globals()[i + "_en"]]

    tag_C = [HJ44_pitag, HJ45_pitag, HJ46_pitag, HJ47_pitag, HJ48_pitag, HJ49_pitag, HJ75_pitag, HJ76_pitag,
             HJ78_pitag, HJ79_pitag, HJ81_pitag, HJ82_pitag, HJ83_pitag, HJ84_pitag]

    time_format = '%Y-%m-%d %H:%M:%S'

    dates = get_month_dates(int(year), int(month))

    pi_df_C = pd.DataFrame()

    for date in dates:
        start = datetime.datetime.combine(date, datetime.time(11, 0)) - datetime.timedelta(minutes=0)
        end = datetime.datetime.combine(date, datetime.time(11, 0))

        start_time = start.strftime(time_format)  # 注意这里使用了 strftime
        end_time = end.strftime(time_format)  # 注意这里使用了 strftime

        temp_rpc = pd.DataFrame()

        for i in tag_C:
            pi_data = data_export(start_time=start_time,
                                  end_time=end_time,
                                  tagpoint_list=i,
                                  time_interval='1m').iloc[-1:, :]
            temp_rpc = pd.concat([temp_rpc, pi_data], axis=1)

        new_row_C = pd.DataFrame(temp_rpc.values, columns=temp_rpc.columns)

        pi_df_C = pd.concat([pi_df_C, new_row_C], ignore_index=True)

    pi_df_C.index = pi_df_C.index + 1

    pi_df_C = pi_df_C.applymap(replace_dict_with_zero)

    pi_df_C = pi_df_C.rename(columns={'RPC_HJ44_M_TIC01_RKC_READ_PV': "HJ44",
                                      'RPC_HJ45_M_TIC01_RKC_READ_PV': "HJ45",
                                      'RPC_HJ46_M_TIC01_RKC_READ_PV': "HJ46",
                                      'RPC_HJ47_M_TIC01_RKC_READ_PV': "HJ47",
                                      'RPC_HJ48_M_TIC01_RKC_READ_PV': "HJ48",
                                      'RPC_HJ49_M_TIC01_RKC_READ_PV': "HJ49",
                                      'RPC_HJ75_TIC01_RKC_READ_PV': "HJ75",
                                      'RPC_HJ76_TIC01_RKC_READ_PV': "HJ76",
                                      'RPC_HJ78_TIC01_RKC_READ_PV': "HJ78",
                                      'RPC_HJ79_TIC01_RKC_READ_PV': "HJ79",
                                      'RPC_HJ81_TIC01_RKC_READ_PV': "HJ81",
                                      'RPC_HJ82_TIC01_RKC_READ_PV': "HJ82",
                                      'RPC_HJ83_TIC01_RKC_READ_PV': "HJ83",
                                      'RPC_HJ84_L_TIC01_RKC_READ_PV': "HJ84"})

    pi_df_C = pi_df_C.T

    # pi_df_C.to_excel('temp_C.xlsx')

    pi_df_C.columns = pi_df_C.columns.astype(str)

    return pi_df_C


def get_current_year():
    return datetime.datetime.now().year


def get_current_month():
    return datetime.datetime.now().month


def info_A():
    gr.Info("正在讀取甲棟資料，請稍後一分鐘~")


def info_B():
    gr.Info("正在讀取乙棟資料，請稍後一分鐘~")


def info_C():
    gr.Info("正在讀取丙棟資料，請稍後一分鐘~")


seafoam = Seafoam()

dropdown, js = create_theme_dropdown()

with gr.Blocks(theme=seafoam) as pi_data_C1:
    with gr.Row():
        gr.Markdown("# 南亞塑膠硬管C1下載區")
    with gr.Row():
        with gr.Column():
            gr.Markdown('## 開發者: 嘉義一廠 賴烱庭 (N000184910)')
        with gr.Column():
            toggle_dark = gr.Button(value="淺色/深色模式")
    with gr.Row():
        gr.Markdown('## 請設定年月:')

    with gr.Row():
        dt = gr.HTML(f"""<input type="month" id="month" name="month" value="{get_current_year()}-{get_current_month()}"
                                                        max="{get_current_year()}-{get_current_month()}">""")
        x = gr.Textbox(label='搜尋日期為:', value='YYYY-MM', interactive=False, visible=False)
    with gr.Row():
        with gr.Column():
            A_class = gr.Button(value='甲棟C1下載')
        with gr.Column():
            B_class = gr.Button(value='乙棟C1下載')
        with gr.Column():
            C_class = gr.Button(value='丙棟C1下載')
    with gr.Row():
        with gr.Column():
            show_result = gr.Dataframe()
        with gr.Column():
            download_result = gr.File(visible=False, label='壓縮檔下載')

    toggle_dark.click(
        None,
        js="""
                    () => {
                        document.body.classList.toggle('dark');
                        document.querySelector('gradio-app').style.backgroundColor = 'var(--color-background-primary)'
                    }
                    """,
    )

    A_class.click(info_A, None, None)

    A_class.click(pipe_A_data, inputs=x, outputs=show_result,
                  js='(x) => {return (document.getElementById("month")).value;}')

    A_class.click(download_files_A, inputs=x, outputs=[download_result, download_result],
                  js='(x) => {return (document.getElementById("month")).value;}')

    B_class.click(info_B, None, None)

    B_class.click(pipe_B_data, inputs=x, outputs=show_result,
                  js='(x) => {return (document.getElementById("month")).value;}')

    B_class.click(download_files_B, inputs=x, outputs=[download_result, download_result],
                  js='(x) => {return (document.getElementById("month")).value;}')

    C_class.click(info_C, None, None)

    C_class.click(pipe_C_data, inputs=x, outputs=show_result,
                  js='(x) => {return (document.getElementById("month")).value;}')

    C_class.click(download_files_C, inputs=x, outputs=[download_result, download_result],
                  js='(x) => {return (document.getElementById("month")).value;}')

if __name__ == "__main__":
    pi_data_C1.launch(server_name='10.114.70.170',
                      server_port=8787)

