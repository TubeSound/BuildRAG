from nicegui import ui
import asyncio
import time
from faq_rag_chain import rag_query


answer_text = ""

@ui.refreshable
def create_answer_box():
    text_box = ui.textarea().props('outlined rows=20').style('width: 600px')
    text_box.value = answer_text

async def send_message():
    global answer_text, loop_elapsed, ta_query
    question = ta_query.value.strip()
    if not question:
        return
    spinner.visible = True
    answer_text = ""
    create_answer_box.refresh()
    loop_elapsed = True
    #await asyncio.sleep(5)
    answer = rag_query(question)
    answer_text = answer
    print(answer)
    create_answer_box.refresh()
    spinner.visible = False
    loop_elapsed = False
    
async def show_elapsed_time():
    t0 = time.time()
    while loop_elapsed:
        t1 = time.time() - t0
        time_label.text = f'経過時間: {t1: .3f}sec'
        if t1 > 30.0:
            break
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
                    ui.tab('summary', label='サマリ')
                    ui.tab('detail', label='詳細')
                with ui.tab_panels(tabs, value='h').classes('w-full'):
                    with ui.tab_panel('summary'):
                        create_answer_box()
                    with ui.tab_panel('detail'):
                        create_answer_box()
        
def main():
    build_gui()
    ui.run()
    
if __name__ in {"__main__", "__mp_main__"}:
    main()