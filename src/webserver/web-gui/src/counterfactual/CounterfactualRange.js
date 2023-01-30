// Import React
import React from "react";

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
            <div>
              <form>
                <label>
                  Low bound {'(MIN for min possible value)'}:   
                  <input type="text" 
                    value={this.state.low_bound}
                    onChange = {(e) => {
                      this.setState({low_bound:e.target.value});
                      this.props.set_bound(e.target.value, "low");
                    }
                    }
              />
                </label>  
              </form>
              <form>
                <label>
                  High bound {'(MAX for max possible value)'}:   
                  <input type="text" 
                        value={this.state.high_bound}
                        onChange = {(e) => {
                          this.setState({high_bound:e.target.value});
                          this.props.set_bound(e.target.value, "high");
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
export default CounterfactualRange;
