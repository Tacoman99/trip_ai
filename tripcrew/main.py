from loguru import logger
import os
from config.config import settings
from crews import PlanCrew, ResearchCrew
from markdown_pdf import MarkdownPdf, Section
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from pypdf import PdfWriter


class TripState(BaseModel):
    # Note: 'id' field is automatically added to all states
    place_data: dict = {}
    travelers_input: str = ""
    overview: str = ""
    itinerary: str = ""


class TripFlow(Flow[TripState]):
    # intializing the flow with the travelers input
    def __init__(self, travelers_input: str):
        super().__init__() 
        self.state.travelers_input = travelers_input




    @start()
    def research_crew_start(self,):
        research_crew = ResearchCrew(
            travelers_input=self.state.travelers_input,
            model=settings.gemini_model,
            api_key=settings.gcp_key,
        )
        result = research_crew.run()

        data = result.pydantic.model_dump() 

        # converting the pydantic to a dictionary 
        self.state.place_data = data
        return data
    
    @listen(research_crew_start)
    def map_creator(self, place_data):
        # implementing map route with ploty or google maps api 
        import plotly.graph_objects as go

        #breakpoint()
        places = place_data['places_to_visit']

        # store the places_name in a list , and the lat and lon in a list 
        places_name, places_lat, places_lon = zip(
            *[(place['place_name'], place['place_latitude'], place['place_longitude']) for place in places]
            )
        
        #breakpoint()

        
        fig = go.Figure(go.Scattermap(
                lat=places_lat,
                lon=places_lon,
                mode='markers',
                marker=go.scattermap.Marker(
                    size=9
                ),
                text=places_name,
                ids=places_name,
            ))

        fig.update_layout(
            autosize=True,
            hovermode='closest',
            map=dict(
                bearing=0,
                center=dict(
                    lat=places_lat[0],
                    lon=places_lon[0]
                ),
                pitch=0,
                zoom=9.5
            ),
            title = 'San Diego Trip Map',


        )

        fig.write_image("fig1.pdf")

    
    @listen(research_crew_start)
    def plan_crew_start(self):

        plan_crew = PlanCrew(
            travelers_input=self.state.travelers_input,
            crew_output=self.state.place_data,
            model=settings.gemini_model,
            api_key=settings.gcp_key,
        )
        return plan_crew.run()
    
    @listen(plan_crew_start )
    def markdown_to_pdf(self, plan_crew_result, ):
        pdf = MarkdownPdf(toc_level=1)
        pdf.add_section(Section(plan_crew_result.raw))
        #pdf.add_section(Section(map_creator_result.raw))
        pdf.save("Itinerary.pdf")
        
        merger = PdfWriter()
        merger.append("Itinerary.pdf")
        merger.append("fig1.pdf")
        merger.write("trip_plan.pdf")
        merger.close()




if __name__ == "__main__":


    flow = TripFlow(travelers_input="I want to go to San Diego, CA for 5 days")
    result = flow.kickoff()

    logger.info(result)
