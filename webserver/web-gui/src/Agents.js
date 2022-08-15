// Import styplesheet for App
import './Agents.css';

// Import React for components
import React from 'react'

// Import Agents since it will be rendered in appb
import Agent from './Agent.js'


// Agent Component (gets rendered in app)
class Agents extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agents: props.agents,
    };
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ 
      agents: nextProps.agents,
    });
  }
  

 
  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
                  this.state.agents.map((agent) => ( 
                    /* Render an Agent component, with props: agent_id, cur_angle, cur_pos, color */
                    <Agent agent_id={agent.agent_id} 
                           cur_angle={agent.cur_angle}
                           cur_pos={agent.cur_pos}
                           color={agent.color} 
                           lights={agent.lights} />
                    ))
          );
    }
}

// Allow it to be called in other functions
export default Agents;

