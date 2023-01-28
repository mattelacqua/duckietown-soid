// Import React
import React from "react";
import CounterfactualInfo from "./CounterfactualInfo.js"
import DeleteCounterfactual from "./DeleteCounterfactual.js"

// Agent Component (gets rendered in app)
class CounterfactualList extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the conponents
  render() {
    return (
            this.props.agent.counterfactuals.map((counterfactual, index) => (
              <div>
              <CounterfactualInfo counterfactual={counterfactual}
                          color={this.props.agent.color} />

              <DeleteCounterfactual counterfactuals={this.props.agent.counterfactuals}
                            index={index} 
                            agent_index={this.props.agent.id} 
                            socket={this.props.socket}/>
             </div>
            ))
          );
    }
}

// Allow it to be called in other functions
export default CounterfactualList;
