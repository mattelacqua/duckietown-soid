// Import styplesheet for App
import './Agents.css';

// Import React for components
import React from 'react'

// Import Agents since it will be rendered in appb
import Agent from './Agent.js'
import Agent0 from './Agent0.js'
import AddAgent from './AddAgent.js'

// Agent Component (gets rendered in app)
class Agents extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {};
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {

    let agent0 = this.props.agents[0];
    let agents = this.props.agents.slice(1);

    let run = (this.props.sim_state === 'run')

    return ( <div>
               <div className="Agents" style={{'pointer-events' : (run) ? 'none' : 'auto', 'opacity' : (run) ? '0.5' : '1'}}>
                 <h2>Primary Agent</h2>
                 <Agent0  agents={this.props.agents}
                          agent={agent0}
                          sim_step={this.props.sim_step}
                          env_info={this.props.env_info}
                          socket={this.props.socket}
                          update_from_sim={this.props.update_from_sim}/>
                 <div className="AgentsHeader">
                   <h2>Other Agents</h2>
                   <AddAgent agents={this.props.agents}
                             socket={this.props.socket}/>
                 </div>
                 {agents.map((agent) => (
                     <Agent  agents={this.props.agents}
                             agent={agent}
                             sim_step={this.props.sim_step}
                             socket={this.props.socket}
                             update_from_sim={this.props.update_from_sim}/>
                 ))}
               </div>
             </div>
           );
    }
}
// Allow it to be called in other functions
export default Agents;
