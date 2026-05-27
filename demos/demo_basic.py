"""
Basic Demo for Experience-Shaped Affective Agent (V0.8)

Demonstrates core functionality of the affective agent.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from emotion_agent import AffectiveAgent


def demo_basic_emotions():
    """Demo basic emotional state management."""
    print("=" * 60)
    print("DEMO 1: Basic Emotional State Management")
    print("=" * 60)
    
    agent = AffectiveAgent(agent_id="demo_agent")
    
    # Initial state
    state = agent.get_state()["emotional_state"]
    print(f"Initial state: {state}")
    
    # Feel joy
    agent.feel("joy")
    state = agent.get_state()["emotional_state"]
    print(f"\nAfter feeling joy: {state}")
    
    # Feel sadness
    agent.feel("sadness")
    state = agent.get_state()["emotional_state"]
    print(f"After feeling sadness: {state}")
    
    # Perceive a positive event
    agent.perceive("Received good news!", valence_delta=0.4, arousal_delta=0.3)
    state = agent.get_state()["emotional_state"]
    print(f"After perceiving good news: {state}")
    
    print("\n" + "=" * 60 + "\n")


def demo_affective_response():
    """Demo affective response generation."""
    print("=" * 60)
    print("DEMO 2: Affective Response Generation")
    print("=" * 60)
    
    agent = AffectiveAgent()
    
    # Generate responses for different emotions
    emotions = ["joy", "sadness", "anger", "fear", "surprise"]
    
    for emotion in emotions:
        agent.feel(emotion)
        response = agent.respond(context="User shares news")
        print(f"\nEmotion: {emotion.upper()}")
        print(f"Response: {response['text']}")
        print(f"Nonverbal Cues: {response['nonverbal_cues']}")
        print(f"Action Tendency: {response['action_tendency']}")
    
    print("\n" + "=" * 60 + "\n")


def demo_motivation_system():
    """Demo motivation system."""
    print("=" * 60)
    print("DEMO 3: Motivation System")
    print("=" * 60)
    
    agent = AffectiveAgent()
    
    # Add goals
    goal1_id = agent.add_goal("Complete project", "Finish the affective agent project", priority=0.9)
    goal2_id = agent.add_goal("Learn new skills", "Study affective computing", priority=0.7)
    
    print("Added goals:")
    print(f"  - {agent.get_priority_goal()['name']} (priority: {agent.get_priority_goal()['priority']})")
    
    # Update goal progress
    agent.update_goal_progress(goal1_id, 0.5)
    print(f"\nGoal progress updated: {agent.get_priority_goal()['name']} is {agent.get_priority_goal()['progress']*100}% complete")
    
    # Check statistics
    stats = agent.get_state()["motivation_statistics"]
    print(f"\nMotivation Statistics: {stats}")
    
    print("\n" + "=" * 60 + "\n")


def demo_social_interaction():
    """Demo social interaction."""
    print("=" * 60)
    print("DEMO 4: Social Interaction")
    print("=" * 60)
    
    agent = AffectiveAgent()
    
    # Add social entities
    agent.add_social_entity("user_alice", "Alice", "friend")
    agent.add_social_entity("user_bob", "Bob", "colleague")
    
    # Agent feels happy
    agent.feel("joy")
    
    # Interact with Alice (friend)
    result = agent.interact("user_alice", cue="smile")
    print("Interaction with Alice (friend):")
    print(f"  Social Response: {result['social_response']}")
    print(f"  Empathy: {result['empathy']:.3f}")
    print(f"  Cue Interpretation: {result['cue_interpretation']}")
    
    # Interact with Bob (colleague)
    result = agent.interact("user_bob", cue="handshake")
    print("\nInteraction with Bob (colleague):")
    print(f"  Social Response: {result['social_response']}")
    print(f"  Empathy: {result['empathy']:.3f}")
    
    print("\n" + "=" * 60 + "\n")


def demo_learning_adaptation():
    """Demo learning and adaptation."""
    print("=" * 60)
    print("DEMO 5: Learning and Adaptation")
    print("=" * 60)
    
    agent = AffectiveAgent()
    
    # Agent learns from experiences
    agent.feel("joy")
    agent.learn("Work presentation", "Presented well, received praise", 0.8)
    
    agent.feel("fear")
    agent.learn("Public speaking", "Nervous but successful", 0.6)
    
    agent.feel("sadness")
    agent.learn("Project failure", "Project failed due to time constraints", -0.7)
    
    # Get adaptation suggestions
    adaptation = agent.adapt()
    print(f"Adaptation Suggestion: {adaptation['suggestion']}")
    print(f"Confidence: {adaptation['confidence']:.3f}")
    
    # Check learning statistics
    stats = agent.get_state()["learning_statistics"]
    print(f"\nLearning Statistics: {stats}")
    
    print("\n" + "=" * 60 + "\n")


def demo_decision_making():
    """Demo emotion-influenced decision making."""
    print("=" * 60)
    print("DEMO 6: Decision Making with Emotional Influence")
    print("=" * 60)
    
    agent = AffectiveAgent()
    
    # Agent feels anxious (fear)
    agent.feel("fear")
    print("Agent is feeling fearful (anxious)...")
    
    # Decision options
    options = [
        {
            "name": "Play it safe",
            "description": "Choose the low-risk option",
            "expected_value": 0.6,
            "risk": 0.1,
            "emotional_impact": {"valence": 0.3}
        },
        {
            "name": "Take a chance",
            "description": "Choose the high-risk, high-reward option",
            "expected_value": 0.9,
            "risk": 0.7,
            "emotional_impact": {"valence": -0.2}
        },
        {
            "name": "Delay decision",
            "description": "Postpone the decision",
            "expected_value": 0.4,
            "risk": 0.2,
            "emotional_impact": {"valence": 0.1}
        }
    ]
    
    # Make decision
    decision = agent.decide(options, context="Career choice")
    print(f"\nChosen Option: {decision['chosen_option']['name']}")
    print(f"Confidence: {decision['confidence']:.3f}")
    print(f"Rationale: {decision['rationale']}")
    
    print("\n" + "=" * 60 + "\n")


def demo_integration():
    """Demo complete integration of all modules."""
    print("=" * 60)
    print("DEMO 7: Complete Integration")
    print("=" * 60)
    
    agent = AffectiveAgent(agent_id="integrated_agent")
    
    # Simulation of a day in the life
    events = [
        ("Wake up feeling refreshed", {"valence": 0.3, "arousal": 0.2}),
        ("Receive unexpected email about project delay", {"valence": -0.5, "arousal": 0.4}),
        ("Team meeting goes well", {"valence": 0.4, "arousal": 0.3}),
        ("Lunch with friend", {"valence": 0.5, "arousal": 0.2}),
        ("Deadline approaching", {"valence": -0.3, "arousal": 0.6}),
        ("Complete task successfully", {"valence": 0.6, "arousal": 0.4}),
        ("Evening relaxation", {"valence": 0.2, "arousal": -0.3})
    ]
    
    print("Simulating a day in the life of the affective agent:\n")
    
    for i, (event, emotion_delta) in enumerate(events, 1):
        print(f"Event {i}: {event}")
        
        # Process perception
        agent.perceive(event, 
                      valence_delta=emotion_delta["valence"],
                      arousal_delta=emotion_delta["arousal"])
        
        # Run update cycle
        update_result = agent.update()
        
        # Get response
        response = agent.respond()
        
        print(f"  Emotional State: {update_result['emotional_state']['category']}")
        print(f"  Response: {response['text']}")
        
        if update_result["regulation_applied"]:
            print(f"  (Regulation applied)")
        
        print()
    
    # Final statistics
    final_state = agent.get_state()
    print("Final Agent Statistics:")
    print(f"  Total Experiences: {final_state['memory_statistics']['total_experiences']}")
    print(f"  Learned Rules: {final_state['learning_statistics']['total_rules']}")
    print(f"  Decisions Made: {final_state['decision_statistics']['total_decisions']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo_basic_emotions()
    demo_affective_response()
    demo_motivation_system()
    demo_social_interaction()
    demo_learning_adaptation()
    demo_decision_making()
    demo_integration()
    
    print("\n✅ All demonstrations completed successfully!")
