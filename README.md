# Personalized Route Optimization with Crewai

This repository demonstrates how to build personalized travel plans using the CrewAI framework, utilizing AI agents that collaboratively generate tailored and efficient travel itineraries, with Chainlit managing the frontend interface. It specifically showcases the implementation of CrewAI Flows, illustrating how structured, event driven workflows enable the seamless chaining of multiple Crews and tasks. Through effective state management and flexible control flow, including conditional logic and branching, this project exemplifies creating sophisticated, dynamic AI workflows for personalized travel planning.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/aLArz1wMPJw/0.jpg)](https://www.youtube.com/watch?v=aLArz1wMPJw)

## Requirements

- Google API Key: [Get your Google API key](https://console.cloud.google.com/apis/credentials)  
- Serper.dev API Key: [Get your Serper.dev API key](https://serper.dev)  

## Setup

1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd tripcrew
   ```

## Installation and Configuration

1. Store your API keys in a credentials environment file:
   ```
   GOOGLE_API_KEY=your_google_api_key
   SERPER_API_KEY=your_serper_api_key
   GEMINI_MODEL=gemini/'chosen_model'
   ```

2. Install dependencies using UV package manager:
   ```bash
   uv sync
   ```

## Running the Application

To start the application:
```bash
make run_app
```
