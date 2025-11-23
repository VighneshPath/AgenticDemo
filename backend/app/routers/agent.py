from fastapi import APIRouter, HTTPException, status

from app.models import AgentRequest, AgentResponse

from app.agents.orchestrator.agent import orchestrator_agent

router = APIRouter()

@router.post("/agent", response_model=AgentResponse)
async def call_agent(agent_request: AgentRequest):
    try:
        return AgentResponse(data = orchestrator_agent.invoke({"messages": agent_request.data})['messages'][-1].content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to call LLM: {str(e)}"
        )
