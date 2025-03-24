import chainlit as cl
from main import TripFlow
import plotly.graph_objects as go
import json



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
      cl.Pdf(name="Trip Plan", display="inline", path="docs/trip_plan.pdf")
    ]

    await cl.Message(content="Your trip plan is ready! Here's a brief guide to help you navigate the trip in a pdf file", elements=elements).send()


# ploty map 

# read the guide.json file
    with open('guide.json', 'r') as f:
        place_data = json.load(f)

        places = place_data['places_to_visit']

    # store the places_name in a list , and the lat and lon in a list 
    places_name, places_lat, places_lon = zip(
            *[(place['place_name'], place['place_latitude'], place['place_longitude']) for place in places]
            )
        
        #breakpoint()

        
    fig = go.Figure(go.Scattermapbox(
                lat=places_lat,
                lon=places_lon,
                mode='markers',
                marker=dict(
                    size=9,
                ),
                text=places_name,
                ids=places_name,
            ))

    fig.update_layout(
            autosize=True,
            hovermode='closest',
            mapbox=dict(
                style='open-street-map',
                bearing=0,
                center=dict(
                    lat=places_lat[0],
                    lon=places_lon[0]
                ),
                pitch=0,
                zoom=9.5
            ),
            title = 'Trip Map',


        )
   # breakpoint()
    elements = [cl.Plotly(name="Trip Map", figure=fig, display="inline")]

    await cl.Message(content="Here is your trip map", elements=elements).send()

