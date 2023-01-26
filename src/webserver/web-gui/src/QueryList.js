// Import style
import './Agent.css';
// Import React
import React from "react";


// Agent Component (gets rendered in app)
class QueryList extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      agent_id: props.agent_id,
    };
  }

  // Render the agent component ( Consists currently of a dial (AgentDial.js and agent information AgentInfo.js)
  render() {

    return (
            <div>
                {/* 
                Going to be some sort of map over each counterfactual to display their information
                Will also include a button of some sort to delete. Will have to get the socket through props
                and pass to button.
                */}
             </div>
          );
    }
}

// Allow it to be called in other functions
export default QueryList;
