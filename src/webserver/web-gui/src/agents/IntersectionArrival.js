// Import React
import React from "react";

// Agent Component (gets rendered in app)
class IntersectionArrival extends React.Component {

  // Construct it with state so we can keep track of relevant information
  constructor(props) {
    super(props);
    this.state = {
      value: props.agent.intersection_arrival,
    };
  }

  // Render the agent component 
  render() {

    return (
            <div>
              <form>
                <label>
                  {"Intersection Arrival"}:   
                  <input type="number" 
                        value={this.state.value}
                        onChange = {(e) => {
                          this.setState({value:e.target.value});
                          this.props.socket.emit(
                            "intersection_arrival",
                            {
                              agent_index: this.props.agent.id,
                              intersection_arrival: e.target.value,
                            });
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
export default IntersectionArrival;
