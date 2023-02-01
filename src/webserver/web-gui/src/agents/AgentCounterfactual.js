// Import style
import './AgentCounterfactual.css';
// Import React
import React from "react";

// Import Counterfactual stuff
import AddCounterfactual from '../counterfactual/AddCounterfactual.js'
import CounterfactualList from '../counterfactual/CounterfactualList'

// Agent Component (gets rendered in app)
class AgentCounterfactual extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    // I don't think it will have a ton of stuff in its state. It might change, but i think it should be good.
    this.state = {
    };
  }

  // Render the agent component (Wrapper to add a Counterfactual, and one to edit the Counterfactual list)
  render() {

    /* Add Counterfactual: 
          - We are passing all the info through so that we can prefil text boxes with the values here.
          - We pass counterfactuals list through so we can add one on at the very end with a button.
      Counterfactual list:
          - Map through all the queries and their information and display to the user so they can get rid of ones they no longer want.
    */
    return (
            <div>
                <AddCounterfactual agent={this.props.agent}
                          socket={this.props.socket}/>

          
                <CounterfactualList  agent={this.props.agent} 
                            socket={this.props.socket}/>
         
            </div>
          );
    }
}

// Allow it to be called in other functions
export default AgentCounterfactual;
