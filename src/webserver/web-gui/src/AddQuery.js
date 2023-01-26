// Import style
import './Agent.css';
// Import React
import React from "react";


// Agent Component (gets rendered in app)
class AddQuery extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    // State of this should model the counterfactuals format of the json blob. We will likely need to add more elements to this.
    // I can help with that once I have these dumb agents trained.
    /*
      i.e. {
        is_forward_step: false, 
        is_angle: false, 
        is_signal_choice: false, 
        is_value:
        is_range:
        range:
          {
            gte: false
            lte: false
            etc...
          }
        etc...
      }
    */
    this.state = {
      agent_id: props.agent_id,
    };
  }


  // Render the agent component 
  render() {

    // There may be several renders here based on conditionals on the state, and what values of state are true.
    // You may have to build more components as well like 'text boxes' or call out to Angle Dial or things like that.
    // I can do some of that or help you learn how. Just reach out and lmk
    // Will end with a button to add the query.
    return (
            <div>
                {/* Render */}
             </div>
          );
    }
}

// Allow it to be called in other functions
export default AddQuery;
