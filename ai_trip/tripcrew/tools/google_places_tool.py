from tools.google_api import GooglePlaces
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pandas as pd


class google_places_input(BaseModel):
    """Input schema for google places tool"""

    query: str = Field(
        ...,
        description="query to search  include location to search for places using google places api",
    )
    radius: int = Field(
        50000,
        description="radius in meters to search for places using google places api",
    )
    # area: str = Field(..., description="area to search for places using google places api e.g. San Diego, CA ")


class GooglePlacesTool(BaseTool):
    name: str = "Google Places Search Tool"
    description: str = "This tool is used to search for places using Google Places API based on the query and radius"
    args_schema: Type[BaseModel] = google_places_input

    # self.area = area

    def _run(
        self,
        query: str,
        radius: int,
        # area: str,
    ) -> pd.DataFrame:
        # Initialize GooglePlaces with the provided argument
        google_places = GooglePlaces(
            # area=self.area,
            query=query,
            radius=radius,
        )

        # Fetch data
        df = google_places.fetch_places()

        # Return the DataFrame as a string or any other format you need
        # df.to_csv(output_file=f'/data/{query}_reviews.csv',index=False)

        return df

    # c


# TODO: create this tool fully so the agent can use it to find places for the trip
#       - Ensuring the agent can do queries " Mexican restuarants", "Italian restaurants","Musuems in the area" etc
#       - check for the struct array type for compression or flat structure
