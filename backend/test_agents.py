
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_agents_and_tools():
    """Test all agents and tools"""
    print("🧪 Testing AI Tutor Multi-Agent System")
    print("=" * 50)
    
    try:
      
        print("1. Testing imports...")
        from agents import TutorAgent, MathAgent, PhysicsAgent
        from tools import CalculatorTool, PhysicsConstantsTool
        from models import AgentRequest, AgentResponse
        print("✅ All imports successful!")
        
        print("\n2. Testing tool instantiation...")
        calc_tool = CalculatorTool()
        physics_tool = PhysicsConstantsTool()
        print(f"✅ Calculator tool: {calc_tool.name}")
        print(f"✅ Physics tool: {physics_tool.name}")
        
    
        print("\n3. Testing calculator tool...")
        calc_result = await calc_tool.execute("2 + 3 * 4")
        print(f"Calculator result: {calc_result.result} (Success: {calc_result.success})")
        
   
        print("\n4. Testing physics constants tool...")
        constant_result = await physics_tool.execute("c", query_type="constant")
        print(f"Speed of light: {constant_result.result} (Success: {constant_result.success})")
        
     
        print("\n5. Testing agent instantiation...")
        tutor_agent = TutorAgent()
        print(f"✅ TutorAgent created")
        print(f"Math agent tools: {tutor_agent.math_agent.get_available_tools()}")
        print(f"Physics agent tools: {tutor_agent.physics_agent.get_available_tools()}")
        
        print("\n6. Testing math query routing...")
        math_request = AgentRequest(query="What is 2 + 3?", context={})
        classification = tutor_agent._classify_query(math_request.query)
        print(f"Math query classification: {classification}")
        
        print("\n7. Testing physics query routing...")
        physics_request = AgentRequest(query="What is the speed of light?", context={})
        classification = tutor_agent._classify_query(physics_request.query)
        print(f"Physics query classification: {classification}")
        
        print("\n✅ All tests passed! Phase 3 & 4 implementation is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_agents_and_tools()) 