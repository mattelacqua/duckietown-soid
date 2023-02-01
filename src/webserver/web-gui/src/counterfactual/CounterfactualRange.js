// Import React
import React from "react";

import './valuetype.css'

// Agent Component (gets rendered in app)
class CounterfactualRange extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      low_bound: props.default_val,
      high_bound: props.default_val,
    };
  }

  // Render the agent component 
  render() {

    return (
            <div class = 'value-style'>
              <form>
                <label>
                  Low bound {'(MIN for min possible value)'}:   
                  <input type="text" 
                    value={this.state.low_bound}
                    onChange = {(e) => {
                      this.props.set_bound(e.target.value, "low");
                    }
                    }
              />
                </label>  
              </form>
              <div class = 'value-top'>
              <form>
                <label>
                  High bound {'(MAX for max possible value)'}:   
                  <input type="text" 
                        value={this.state.high_bound}
                        onChange = {(e) => {
                          this.props.set_bound(e.target.value, "high");
                        }
                        }
                  />
                </label>  
              </form>
              </div>
            </div>
          );
    }
}

// Allow it to be called in other functions
export default CounterfactualRange;
