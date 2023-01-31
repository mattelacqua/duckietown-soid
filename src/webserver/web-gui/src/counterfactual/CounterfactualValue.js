// Import React
import React from "react";

// Agent Component (gets rendered in app)
class CounterfactualValue extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      value: props.default_val,
    };
    this.props.set_value(props.default_value);
  }

  // Render the agent component 
  render() {

    return (
            <div>
              <form>
                <label>
                  {this.props.label_string}:   
                  <input type="text" 
                        value={this.state.value}
                        onChange = {(e) => {
                          this.setState({value:e.target.value});
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
