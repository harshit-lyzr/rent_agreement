import os

import solara
import solara.lab
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from lyzr_automata.tasks.task_literals import InputType, OutputType
import datetime as dt
from dotenv import load_dotenv

load_dotenv()
api = os.getenv("OPENAI_API_KEY")


owner = solara.reactive("Harshit")
owner_adres = solara.reactive("")
lessee = solara.reactive("Jorge")
lessee_adres = solara.reactive("")


openai_model = OpenAIModel(
            api_key=api,
            parameters={
                "model": "gpt-4-turbo-preview",
                "temperature": 0.2,
                "max_tokens": 1500,
            },
        )

def rent_agreement_generator(owner_name, lessee_name, owner_address, lessee_address, start_date, end_date):
    lawyer = Agent(
        prompt_persona=f"You are a Lawyer whp is Expert in Property Laws and Rental Laws.",
        role="Property Lawyer",
    )

    lawyer_task = Task(
        name="Rent Agreement",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=openai_model,
        agent=lawyer,
        instructions=f"""
        Draft A Rent Agreement with below Details:
        Owner Name: {owner_name}
        Lessee Name: {lessee_name}
        Owner Address: {owner_address}
        Lessee Address: {lessee_address}
        Start Date: {start_date}
        End Date: {end_date}
        """,
    )

    output = LinearSyncPipeline(
        name="Rent Agreement Generation",
        completion_message="Rent Agreement Generated!",
        tasks=[
            lawyer_task
        ],
        ).run()
    return output[0]['task_output']


@solara.component
def Page():
    result, set_result = solara.use_state("")
    start_date = solara.use_reactive(dt.date.today())
    end_date = solara.use_reactive(dt.date.today())

    with solara.AppBarTitle():
        with solara.Columns([0, 1]):
            solara.Text("Rent Agreement Generator")


    def rent_agreement():
        solution = rent_agreement_generator(owner.value, lessee.value, owner_adres.value, lessee_adres.value, start_date.value, end_date.value)
        print(solution)
        set_result(result + solution)

    with solara.Sidebar():
        solara.InputText("Enter Owner Name", value=owner,continuous_update=True)
        solara.InputText("Enter Owner Name", value=lessee, continuous_update=True)
        solara.InputText("Enter Owner Address", value=owner_adres, continuous_update=True)
        solara.InputText("Enter Lessee Address", value=lessee_adres, continuous_update=True)
        solara.lab.InputDate(start_date,label="Start Date")
        solara.lab.InputDate(end_date, label="End Date")
        solara.Button(label="Generate", on_click=rent_agreement)

    solara.Markdown(result)
