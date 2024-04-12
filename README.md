# Mars Tourism

The Mars Tourism project aims to facilitate trip planning to Mars by utilizing NASA and SpaceX APIs. It provides users with information about available launchpads, rockets, and potential hazards such as asteroids during the planned travel dates, issuing warnings when necessary.

## Usage

1. **Clone Repository**: Clone the project repository and navigate to the project folder.

2. **Agent Integration**:
   - Copy the provided agents and paste them into the Agentverse Blank agent template, along with their respective booking protocol files if available.

3. **Service Group Creation**: Create a service group consisting of all three agents.

4. **Task Assignment**:
   - Assign the SpaceTrip agent as the main task.
   - Assign the rest of the agents as sub-tasks.

5. **Agent Descriptions**:
   - Each agent should have a specific description provided as follows:

   5.1 **SpaceTrip Agent**: This agent handles the main task of trip planning to Mars. It interacts with the user to gather trip details and utilizes NASA and SpaceX APIs to provide relevant information and warnings.

   5.2 **Launchpad Agent**: This agent specializes in retrieving information about available launchpads for Mars missions. It communicates with relevant APIs to ensure compatibility with the planned trip.

   5.3 **Asteroid Hazard Agent**: This agent focuses on identifying potential hazards such as asteroids during the planned travel dates. It utilizes data from NASA and other sources to assess risks and issue warnings as necessary.

6. **DeltaV Integration**: Connect DeltaV to the created service for seamless interaction and task execution.

7. **User Interaction**:
   - Prompt the system with a related request such as "Book me a trip to Mars".
