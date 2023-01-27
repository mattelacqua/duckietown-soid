// Import React
import React from "react";
import Operator from "./Operator.js";

// Agent Component (gets rendered in app)
class QueryRange extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  // Render the agent component 
  render() {

    return (
            <div>
              <form>
                <label>
                  Low bound:   
                  <input type="text" 
                    value={this.state.value}
                    onChange = {(e) => {
                      this.props.set_bound(e.target.value, "low");
                    }
                    }
              />
                </label>  
              </form>
              <Operator set_operator={this.props.set_operator}/>
              <form>
                <label>
                  High bound:   
                  <input type="text" 
                        defaultValue={this.props.default_val}
                        onChange = {(e) => {
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
export default QueryRange;
