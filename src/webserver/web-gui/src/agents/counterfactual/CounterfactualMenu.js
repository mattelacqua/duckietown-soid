// Import React for components
import React from 'react'

// Import Counterfactual stuff
import ModelChoice from './ModelChoice.js'
import Queries from './Queries.js'
import AddCounterfactual from './AddCounterfactual.js';
import CounterfactualList from './CounterfactualList.js'

// CSS stuff
import './Counterfactuals.css'


// Agent Component (gets rendered in app)
class CounterfactualMenu extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {};
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {
    return (
      <div>
        { /* Get the Model we are using */}
        <ModelChoice  agent={this.props.agents[0]} 
                      socket={this.props.socket} 
          />

        { /* Buttons for the output */}
        <Queries  socket={this.props.socket} 
                  update_from_sim={this.props.update_from_sim}
                  env_info={this.props.env_info}
          />

        { /* Map the adding counterfactuals for each agent and the list of their stuff */}

        { /* Map the adding counterfactuals for each agent and the list of their stuff */}
        <div className="Counterfactuals">
          {this.props.agents.map((agent) => ( 
          <div>
            <p> Agent {agent.id}: </p>
            <AddCounterfactual  agent={agent} 
                                socket={this.props.socket} 
              />
            <CounterfactualList agent={agent}  
                                socket={this.props.socket} 
              />
          </div>
          ))}
        </div>
      </div>
    );
  }
}
// Allow it to be called in other functions
export default CounterfactualMenu;

