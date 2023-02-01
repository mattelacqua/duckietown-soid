// Import React
import React from "react";

import './valuetype.css'

// Agent Component (gets rendered in app)
class CounterfactualValue extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      value: props.default_val,
    };
  }

  // Render the agent component 
  render() {

    return (
            <div class = 'single-value'>
              <form>
                <label>
                  {this.props.label_string}:   
                  <input type="text" 
                        value={this.state.value}
                        onChange = {(e) => {
                          this.props.set_value(e.target.value);
                          }
                        }
                  />
                </label>  
              </form>
            </div>
          );
    }
}

// Allow it to be called in other functions
export default CounterfactualValue;
