import asyncio
import threading
from dotenv import load_dotenv
from fastapi import FastAPI
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from agent_framework_foundry_hosting import ResponsesHostServer
from fastapi.middleware.cors import CORSMiddleware

from agents.stockz_agent import initialize_stockz_agent


load_dotenv(override=True)

stockz_agent = initialize_stockz_agent()

session = stockz_agent.create_session()

# use responseshostserver for creating server for the stockz agent
# server = ResponsesHostServer(stockz_agent)

# use AGUI for creating server for the stockz agent
app = FastAPI(title="Stockz Agent Server")
# # Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, stockz_agent, "/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hosting agent with AG-UI and ResponsesHostServer 
# AG-UI support SSE and ResponsesHostServer support streaming responses with POST /responses
if __name__ == "__main__":
    import uvicorn
    # Run ResponsesHostServer in a background daemon thread so it doesn't block uvicorn
    # t = threading.Thread(target=server.run, daemon=True)
    # t.start()
    uvicorn.run(app, host="127.0.0.1", port=8888)
