// Import React
import React from "react";


// Agent Component (gets rendered in app)
class QueryList extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {

    const agent_id = this.props.agent.id;
    return (
            this.props.agent.counterfactuals.map((counterfactual, index) => (
              <div>
              <QueryInfo counterfactual={counterfactual}
                          color={this.props.agent.color} />

              <DeleteQuery counterfactuals={this.props.agent.counterfactuals}
                            index={index} />
             </div>
            ))
          );
    }
}

// Allow it to be called in other functions
export default QueryList;
