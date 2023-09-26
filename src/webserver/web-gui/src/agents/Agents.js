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

    return ( <div>
               <div className="AgentHeader">
                 <h2>Agents</h2>
                 <AddAgent agents={this.props.agents}
                           socket={this.props.socket}/>
               </div>
               <div className="Agents">
                 <Agent0  agents={this.props.agents}
                          agent={agent0}
                          socket={this.props.socket}
                          update_from_sim={this.props.update_from_sim}/>
                 {agents.map((agent) => (
                   <div class="card">
                     <Agent  agents={this.props.agents}
                             agent={agent}
                             socket={this.props.socket}
                             update_from_sim={this.props.update_from_sim}/>
                   </div>
                 ))}
               </div>
             </div>
           );
    }
}
// Allow it to be called in other functions
export default Agents;
