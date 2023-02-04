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
    };
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
      this.props.agents.map((agent) => ( 
      /* Render an Agent component, with props: agent_id, cur_angle, cur_pos, color */
      <div class = 'Modify-Wrap'> 
      <Agent  agent={agent} 
              socket={this.props.socket} 
              update_from_sim={this.props.update_from_sim}/>

        </div>
      ))
    );
  }
}
// Allow it to be called in other functions
export default Agents;

