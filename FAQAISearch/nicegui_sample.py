import pandas as pd
from nicegui import ui
import asyncio
import time

df_ans = pd.DataFrame([{'名前': '', 'スコア': 0}])

def table_columns(df):
    return [{'name': c, 'label': c, 'field':c} for c in df.columns]

@ui.refreshable
def create_table():
    ui.table(columns=table_columns(df_ans),
             rows=df_ans.to_dict(orient='records'),
             row_key='名前').style('width:500px; height:200px')

async def send_message():
    global df_ans, loop_elapsed, ta_query
    question = ta_query.value.strip()
    if not question:
        return
    spinner.visible = True
    df_ans = pd.DataFrame([{'名前': '', 'スコア': 0}])
    create_table.refresh()
    loop_elapsed = True
    await asyncio.sleep(5)
    df_ans = pd.DataFrame([{'名前': 'x', 'スコア': 10},
                           {'名前': 'y', 'スコア': 70}])
    create_table.reresh()
    spinner.visible = False
    loop_elapsed = False
    
async def show_elapsed_time():
    t0 = time.time()
    while loop_elapsed:
        t1 = time.time() - t0
        time_label.text = f'経過時間: {t1: .3f}sec'
        await asyncio.sleep(0.5)

def on_click():
    asyncio.create_task(send_message())
    asyncio.create_task(show_elapsed_time())
    
def build_gui():
    global ta_query, spinner, time_label
    ui.label("問い合わせ").style('font-size: 30px')
    with ui.row():
        with ui.card().style('width: 800px; padding:20px'):
            ui.label('質問')
            with ui.row().style('gap: 20px'):
                ta_query = ui.textarea().props('outlined rows=3').style('width: 400px')
                ui.button('送信', on_click=on_click).style('font-size: 18px; with: 80px; height: 50px')
                spinner = ui.spinner(size='lg', color='primary')
            spinner.visible = False
    with ui.row():
        with ui.card().style('width: 800px; padding:20px'):
            with ui.row():
                ui.label('回答')
                time_label = ui.label('').classes('text-lg text-blue-700')
                with ui.tabs() as tabs:
                    ui.tab('h', label='サマリ')
                    ui.tab('a', label='詳細')
                with ui.tab_panels(tabs, value='h').classes('w-full'):
                    with ui.tab_panel('h'):
                        create_table()
                    with ui.tab_panel('a'):
                        create_table()
        
def main():
    build_gui()
    ui.run()
    
if __name__ in {"__main__", "__mp_main__"}:
    main()