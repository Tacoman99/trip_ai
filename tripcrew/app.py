import chainlit as cl
from main import TripFlow


@cl.on_chat_start
async def on_chat_start():
    await cl.Message(
        content=f"""
        Welcome to the trip crew! I'm here to help you plan your next adventure. 
        How can I assist you today?
        """
    ).send()


@cl.on_message
async def main(message: cl.Message):

    # Makes crew function async due to how long it takes to run
    trip_flow = TripFlow(message.content)
    da_message = await cl.make_async(trip_flow.kickoff)()

        # Sending a pdf with the local file path
    elements = [
      cl.Pdf(name="Trip Plan", display="inline", path="trip_plan.pdf")
    ]

    await cl.Message(content="Your trip plan is ready! Here's a brief guide to help you navigate the trip in a pdf file", elements=elements).send()